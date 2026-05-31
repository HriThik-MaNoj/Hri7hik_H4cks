#!/usr/bin/env bash
###############################################################################
# Obsidian → Hugo Workflow (v3.0)
#
# Writer-first CLI:
#   ./scripts/workflow.sh             → interactive menu (no args = help)
#   ./scripts/workflow.sh serve       → convert + watch + dev server
#   ./scripts/workflow.sh new         → interactive title + template picker
#
# Speed wins over v2:
#   - Converter has its own SHA-1 cache → unchanged files never re-process
#   - Watcher debounces inotify bursts (Obsidian autosaves are spammy)
#   - Hugo dev server keeps fast-render ON (drop --disableFastRender)
#   - Single dispatch table; no duplicated dependency checks
###############################################################################

set -euo pipefail

# Resolve project root regardless of CWD.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

# ─── Colors ───────────────────────────────────────────────────────────────────
RED=$'\033[0;31m';  GREEN=$'\033[0;32m'; YELLOW=$'\033[1;33m'
BLUE=$'\033[0;34m'; CYAN=$'\033[0;36m';  DIM=$'\033[2m'
BOLD=$'\033[1m';    NC=$'\033[0m'

# ─── Config (env-overridable) ─────────────────────────────────────────────────
HUGO_PORT="${HUGO_PORT:-1313}"
HUGO_BIND="${HUGO_BIND:-0.0.0.0}"
DEBOUNCE_MS="${DEBOUNCE_MS:-400}"
OBSIDIAN_DIR="obsidian-vault/posts"
ATTACH_DIR="obsidian-vault/attachments"
CONTENT_DIR="content/posts"
TEMPLATES_DIR="obsidian-templates"
CONVERTER="scripts/obsidian_to_hugo_converter.py"
WATCHER_PID=""

# ─── Logging ──────────────────────────────────────────────────────────────────
log_info()    { printf '%s[INFO]%s %s\n'  "$BLUE"   "$NC" "$*"; }
log_success() { printf '%s[ OK ]%s %s\n'  "$GREEN"  "$NC" "$*"; }
log_warning() { printf '%s[WARN]%s %s\n'  "$YELLOW" "$NC" "$*"; }
log_error()   { printf '%s[ERR ]%s %s\n'  "$RED"    "$NC" "$*" >&2; }
log_header()  {
    printf '\n%s========================================%s\n' "$CYAN" "$NC"
    printf '%s%s%s%s\n' "$CYAN" "$BOLD" "$*" "$NC"
    printf '%s========================================%s\n' "$CYAN" "$NC"
}

# ─── Cleanup ──────────────────────────────────────────────────────────────────
cleanup() {
    if [ -n "$WATCHER_PID" ] && kill -0 "$WATCHER_PID" 2>/dev/null; then
        pkill -P "$WATCHER_PID" 2>/dev/null || true
        kill "$WATCHER_PID" 2>/dev/null || true
        wait "$WATCHER_PID" 2>/dev/null || true
    fi
}
trap cleanup EXIT INT TERM

# ─── Dependency check (Kali PEP-668 aware) ────────────────────────────────────
check_dependencies() {
    local errors=0

    command -v python3 >/dev/null 2>&1 || { log_error "python3 not installed"; errors=$((errors+1)); }
    command -v hugo    >/dev/null 2>&1 || { log_error "hugo not installed (https://gohugo.io/)"; errors=$((errors+1)); }

    if ! python3 -c "import yaml, PIL" 2>/dev/null; then
        log_warning "Missing Python packages (pyyaml, Pillow)"
        if [ -n "${VIRTUAL_ENV:-}" ]; then
            log_info "Installing into active venv: $VIRTUAL_ENV"
            pip install -q -r requirements.txt && log_success "Packages installed"
        else
            log_error "No active venv. Kali blocks system pip. Run:"
            printf '    python3 -m venv venv\n    source venv/bin/activate\n    pip install -r requirements.txt\n'
            errors=$((errors+1))
        fi
    fi

    [ "$errors" -eq 0 ] || exit 1
}

# ─── Port helpers ─────────────────────────────────────────────────────────────
port_in_use() {
    if command -v lsof >/dev/null 2>&1; then
        lsof -i ":$1" -sTCP:LISTEN -t >/dev/null 2>&1
    elif command -v ss >/dev/null 2>&1; then
        ss -ltn "sport = :$1" 2>/dev/null | grep -q LISTEN
    else
        return 1
    fi
}

find_free_port() {
    local p=$1
    while port_in_use "$p" && [ "$p" -lt 1400 ]; do p=$((p+1)); done
    echo "$p"
}

kill_port() {
    local pids
    pids=$(lsof -ti ":$1" -sTCP:LISTEN 2>/dev/null || true)
    if [ -n "$pids" ]; then
        log_warning "Killing PID(s) on port $1: $pids"
        echo "$pids" | xargs -r kill -9 2>/dev/null || true
        sleep 0.3
    fi
}

# ─── Setup ────────────────────────────────────────────────────────────────────
setup_directories() {
    mkdir -p "$OBSIDIAN_DIR" "$ATTACH_DIR" static/images "$CONTENT_DIR"
}

# ─── Conversion ───────────────────────────────────────────────────────────────
run_converter() {
    local extra=()
    [ "${FORCE_CONVERT:-0}" = "1" ] && extra+=(--force)
    [ "${VERBOSE:-0}" = "1" ]      && extra+=(-v)
    python3 "$CONVERTER" \
        --source ./obsidian-vault \
        --output ./content/posts \
        "${extra[@]}"
}

convert_notes() {
    log_header "Convert Obsidian → Hugo"
    if [ ! -d "$OBSIDIAN_DIR" ] || [ -z "$(ls -A "$OBSIDIAN_DIR" 2>/dev/null)" ]; then
        log_warning "No notes in $OBSIDIAN_DIR/"
        log_info "Scaffold one: $0 new"
        return 0
    fi
    run_converter
}

# ─── Debounced watcher ────────────────────────────────────────────────────────
# Obsidian saves trigger 3-5 inotify events in quick succession. Coalesce them
# by draining the pipe for $DEBOUNCE_MS after the first event before running
# the converter — turns a "burst storm" into a single fast incremental run.
start_watcher() {
    if ! command -v inotifywait >/dev/null 2>&1; then
        log_warning "inotifywait missing — Hugo will still hot-reload content/"
        log_info "Install: sudo apt install inotify-tools"
        return
    fi

    mkdir -p "$OBSIDIAN_DIR" "$ATTACH_DIR"
    local debounce_s
    debounce_s=$(awk -v ms="$DEBOUNCE_MS" 'BEGIN { printf "%.3f", ms/1000 }')

    (
        inotifywait -m -q -r -e modify,create,move,delete \
            --format '%w%f' "$OBSIDIAN_DIR" "$ATTACH_DIR" 2>/dev/null |
        while IFS= read -r changed; do
            case "$changed" in
                *.md|*.png|*.jpg|*.jpeg|*.gif|*.svg|*.webp) ;;
                *) continue ;;
            esac
            # Drain any further events arriving within the debounce window.
            while IFS= read -r -t "$debounce_s" _; do :; done
            printf '%s[watch]%s %s\n' "$DIM" "$NC" "reconverting…"
            python3 "$CONVERTER" \
                --source ./obsidian-vault \
                --output ./content/posts 2>&1 | tail -3
        done
    ) &
    WATCHER_PID=$!
    log_success "Watcher running (PID $WATCHER_PID, ${DEBOUNCE_MS}ms debounce)"
}

# ─── Serve ────────────────────────────────────────────────────────────────────
serve_site() {
    log_header "Hugo Dev Server"

    if port_in_use "$HUGO_PORT"; then
        if [ "${KILL_PORT:-0}" = "1" ]; then
            kill_port "$HUGO_PORT"
        else
            local alt
            alt=$(find_free_port "$((HUGO_PORT + 1))")
            log_warning "Port $HUGO_PORT busy → using $alt (or: KILL_PORT=1 $0 serve)"
            HUGO_PORT=$alt
        fi
    fi

    start_watcher

    log_info "Server: ${BOLD}http://localhost:$HUGO_PORT${NC}"
    log_info "Stop:   Ctrl+C"

    local args=(
        --buildDrafts --buildExpired --buildFuture
        --bind "$HUGO_BIND"
        --port "$HUGO_PORT"
        --renderToMemory
        --gc
        --noHTTPCache
    )
    [ -f "config-development.toml" ] && args+=(--config "hugo.toml,config-development.toml")
    hugo server "${args[@]}"
}

# ─── Production build ─────────────────────────────────────────────────────────
build_site() {
    log_header "Production Build"
    local start end
    start=$(date +%s)
    hugo --minify --gc --buildExpired --buildFuture
    end=$(date +%s)
    log_success "Built in $((end - start))s"

    if [ -d public ]; then
        local size pages
        size=$(du -sh public | cut -f1)
        pages=$(find public -name '*.html' | wc -l)
        log_info "Output: ${BOLD}$size${NC} | HTML pages: ${BOLD}$pages${NC}"
    fi
}

# ─── Slugify (POSIX-safe) ─────────────────────────────────────────────────────
slugify() {
    printf '%s' "$1" | tr '[:upper:]' '[:lower:]' \
        | sed -E 's/[^a-z0-9]+/-/g; s/^-+|-+$//g'
}

# ─── List templates as a bash array ───────────────────────────────────────────
list_templates() {
    [ -d "$TEMPLATES_DIR" ] || return 0
    find "$TEMPLATES_DIR" -maxdepth 1 -name '*.md' -printf '%f\n' \
        | sed 's/\.md$//' | sort
}

# ─── Pick a template (fzf > numbered prompt > sane default) ───────────────────
pick_template() {
    local templates choice i=1
    mapfile -t templates < <(list_templates)

    if [ ${#templates[@]} -eq 0 ]; then
        echo "default"
        return
    fi

    if command -v fzf >/dev/null 2>&1 && [ -t 0 ]; then
        choice=$(printf '%s\n' "${templates[@]}" \
            | fzf --prompt='Template ▶ ' --height=10 --reverse \
                  --header='↑↓ to choose, Enter to pick' || true)
        [ -n "$choice" ] && { echo "$choice"; return; }
    fi

    printf '%sTemplates:%s\n' "$BOLD" "$NC" >&2
    for t in "${templates[@]}"; do
        printf '  %d) %s\n' "$i" "$t" >&2
        i=$((i+1))
    done
    local sel
    read -r -p "Choose [1-${#templates[@]}] (default 1): " sel </dev/tty
    sel="${sel:-1}"
    if ! [[ "$sel" =~ ^[0-9]+$ ]] || [ "$sel" -lt 1 ] || [ "$sel" -gt "${#templates[@]}" ]; then
        log_error "Invalid choice: $sel"
        exit 1
    fi
    echo "${templates[$((sel-1))]}"
}

# ─── New post ─────────────────────────────────────────────────────────────────
new_post() {
    local title="${1:-}" kind="${2:-}"

    if [ -z "$title" ]; then
        if [ -t 0 ]; then
            read -r -p "Post title: " title </dev/tty
        else
            log_error "Usage: $0 new \"Post Title\" [template]"
            exit 1
        fi
    fi
    [ -z "$title" ] && { log_error "Title required"; exit 1; }

    if [ -z "$kind" ]; then
        kind=$(pick_template)
    fi

    local slug template target now_iso
    slug=$(slugify "$title")
    [ -z "$slug" ] && { log_error "Title produced empty slug"; exit 1; }

    template="$TEMPLATES_DIR/$kind.md"
    target="$OBSIDIAN_DIR/$slug.md"
    now_iso=$(date -u +%Y-%m-%dT%H:%M:%SZ)

    [ -e "$target" ] && { log_error "Already exists: $target"; exit 1; }
    mkdir -p "$OBSIDIAN_DIR"

    # Escape double quotes for safe YAML embedding.
    local esc_title="${title//\"/\\\"}"

    {
        printf '%s\n' '---'
        printf 'title: "%s"\n' "$esc_title"
        printf 'date: %s\n'    "$now_iso"
        printf 'draft: true\n'
        printf 'categories: []\n'
        printf 'tags: []\n'
        printf 'description: ""\n'
        printf '%s\n\n' '---'
        if [ -f "$template" ]; then
            cat "$template"
        else
            log_warning "Template '$kind' not found → blank post"
            printf '# %s\n\nWrite here.\n' "$esc_title"
        fi
    } > "$target"

    log_success "Created: $target"
    [ -f "$template" ] && log_info  "Template: $kind"
    log_info  "Edit in Obsidian, then: $0 serve"
}

# ─── Publish (pick a draft via fzf if no slug given) ──────────────────────────
publish_post() {
    local slug="${1:-}"

    if [ -z "$slug" ]; then
        local drafts
        mapfile -t drafts < <(grep -l '^draft: true' "$OBSIDIAN_DIR"/*.md 2>/dev/null \
                              | sed "s|$OBSIDIAN_DIR/||; s|\.md$||" || true)
        if [ ${#drafts[@]} -eq 0 ]; then
            log_info "No drafts to publish."
            return 0
        fi
        if command -v fzf >/dev/null 2>&1 && [ -t 0 ]; then
            slug=$(printf '%s\n' "${drafts[@]}" \
                   | fzf --prompt='Publish ▶ ' --height=10 --reverse || true)
        else
            log_info "Drafts:"
            printf '  - %s\n' "${drafts[@]}"
            read -r -p "Slug: " slug </dev/tty
        fi
    fi
    [ -z "$slug" ] && { log_error "No slug selected"; exit 1; }

    local file="$OBSIDIAN_DIR/${slug%.md}.md"
    [ -f "$file" ] || { log_error "Not found: $file"; exit 1; }

    if grep -q '^draft: true' "$file"; then
        sed -i 's/^draft: true/draft: false/' "$file"
        log_success "Published: $file"
        FORCE_CONVERT=1 run_converter
    else
        log_info "Already published."
    fi
}

# ─── Stats ────────────────────────────────────────────────────────────────────
stats() {
    log_header "Blog Stats"
    local total=0 drafts=0 published=0 words=0

    if [ -d "$OBSIDIAN_DIR" ]; then
        total=$(find "$OBSIDIAN_DIR" -maxdepth 1 -name '*.md' | wc -l)
        drafts=$( (grep -l '^draft: true' "$OBSIDIAN_DIR"/*.md 2>/dev/null || true) | wc -l)
        published=$((total - drafts))
        # Single concatenated read instead of one cat per file.
        if [ "$total" -gt 0 ]; then
            words=$(cat "$OBSIDIAN_DIR"/*.md 2>/dev/null | wc -w)
        fi
    fi

    printf '  %-12s %s\n' "Posts:" "$total ($published published, $drafts drafts)"
    printf '  %-12s %s\n' "Words:" "$words"
    [ -d public ]        && printf '  %-12s %s\n' "Site size:" "$(du -sh public | cut -f1)"
    [ -d static/images ] && printf '  %-12s %s\n' "Images:"    "$(find static/images -type f | wc -l) ($(du -sh static/images 2>/dev/null | cut -f1))"
}

# ─── Watch (no Hugo) ──────────────────────────────────────────────────────────
watch_mode() {
    log_header "Watch Mode (no server)"
    convert_notes

    command -v inotifywait >/dev/null 2>&1 || {
        log_error "inotifywait required (sudo apt install inotify-tools)"
        exit 1
    }

    log_info "Watching $OBSIDIAN_DIR/ + $ATTACH_DIR/ … Ctrl+C to stop"
    local debounce_s
    debounce_s=$(awk -v ms="$DEBOUNCE_MS" 'BEGIN { printf "%.3f", ms/1000 }')

    inotifywait -m -q -r -e modify,create,move,delete \
        --format '%w%f' "$OBSIDIAN_DIR" "$ATTACH_DIR" |
    while IFS= read -r changed; do
        case "$changed" in
            *.md|*.png|*.jpg|*.jpeg|*.gif|*.svg|*.webp) ;;
            *) continue ;;
        esac
        while IFS= read -r -t "$debounce_s" _; do :; done
        printf '%s[watch]%s %s\n' "$DIM" "$NC" "$changed"
        run_converter
    done
}

# ─── Clean ────────────────────────────────────────────────────────────────────
clean() {
    log_header "Clean Generated Files"
    log_warning "Will delete:"
    printf '  - content/posts/*\n  - static/images/*\n  - public/\n  - resources/\n  - .cache/o2h/\n'

    if [ "${FORCE:-0}" != "1" ]; then
        local ans
        read -r -p "Continue? [y/N] " ans </dev/tty
        case "$ans" in [yY]|[yY][eE][sS]) ;; *) log_info "Aborted"; exit 0 ;; esac
    fi

    rm -rf content/posts/* static/images/* public resources .cache/o2h 2>/dev/null || true
    log_success "Cleaned"
}

# ─── Help ─────────────────────────────────────────────────────────────────────
show_help() {
    local kinds
    kinds=$(list_templates | tr '\n' '|' | sed 's/|$//')
    cat <<EOF
${BOLD}Hri7hik H4cks — Obsidian → Hugo Workflow${NC}

${CYAN}USAGE${NC}
    $0 <command> [args]

${CYAN}WRITER COMMANDS${NC}
    ${BOLD}new${NC} ["title"] [template]   Scaffold a post (interactive if no args)
    ${BOLD}serve${NC}                       Convert + watch + dev server (default)
    ${BOLD}publish${NC} [slug]              Flip draft→published (interactive if no slug)

${CYAN}MAINTENANCE${NC}
    ${BOLD}convert${NC}                     One-shot incremental conversion
    ${BOLD}watch${NC}                       Watch + auto-convert (no server)
    ${BOLD}build${NC}                       Production build (minified) + stats
    ${BOLD}stats${NC}                       Post / word / size counts
    ${BOLD}clean${NC}                       Wipe generated content (FORCE=1 skips prompt)
    ${BOLD}clean-cache${NC}                 Drop converter SHA-1 cache
    ${BOLD}setup${NC}                       Create directory structure
    ${BOLD}check${NC}                       Verify dependencies

${CYAN}TEMPLATES${NC}    ${kinds:-(none — add .md files to $TEMPLATES_DIR/)}

${CYAN}ENV OVERRIDES${NC}
    HUGO_PORT=1313         Server port
    HUGO_BIND=0.0.0.0      Bind address
    KILL_PORT=1            Auto-kill conflicting process on HUGO_PORT
    FORCE_CONVERT=1        Bypass converter cache
    VERBOSE=1              Debug logging in converter
    FORCE=1                Skip 'clean' confirmation
    DEBOUNCE_MS=400        Watcher debounce window

${CYAN}EXAMPLES${NC}
    $0 new                                # interactive: prompts for title + template
    $0 new "SQL Injection Walkthrough" ctf-walkthrough
    $0 serve                              # default writer workflow
    HUGO_PORT=4000 $0 serve               # custom port
    $0 publish                            # fzf picker over current drafts
    FORCE=1 $0 clean && $0 build

EOF
}

# ─── Dispatch ─────────────────────────────────────────────────────────────────
main() {
    case "${1:-help}" in
        new)            shift; new_post "$@" ;;
        serve)          check_dependencies; setup_directories; convert_notes; serve_site ;;
        publish)        shift; check_dependencies; publish_post "$@" ;;
        convert)        check_dependencies; setup_directories; convert_notes ;;
        watch)          check_dependencies; setup_directories; watch_mode ;;
        build)          check_dependencies; FORCE_CONVERT=1 convert_notes; build_site ;;
        stats)          stats ;;
        clean)          clean ;;
        clean-cache)    python3 "$CONVERTER" --clean-cache ;;
        setup)          check_dependencies; setup_directories; log_success "Setup complete" ;;
        check)          check_dependencies ;;
        help|-h|--help) show_help ;;
        *)              log_error "Unknown command: $1"; show_help; exit 1 ;;
    esac
}

main "$@"
