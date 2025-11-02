#!/bin/bash

###############################################################################
# Obsidian to Hugo Blog Workflow Automation
# ==========================================
# This script automates the entire process of converting Obsidian notes to Hugo
# blog posts, including image handling, serving the site, and building for prod.
###############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo ""
    echo -e "${CYAN}========================================${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${CYAN}========================================${NC}"
    echo ""
}

# Check dependencies
check_dependencies() {
    print_header "Checking Dependencies"

    # Check for Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed"
        exit 1
    fi
    print_success "Python 3 found: $(python3 --version)"

    # Check for Hugo
    if ! command -v hugo &> /dev/null; then
        print_warning "Hugo is not installed. Install from https://gohugo.io/"
        exit 1
    fi
    print_success "Hugo found: $(hugo version)"

    # Check for required Python packages
    print_status "Checking Python packages..."
    python3 -c "import yaml, frontmatter, PIL" 2>/dev/null || {
        print_error "Missing required Python packages. Installing..."
        pip3 install pyyaml python-frontmatter Pillow
    }
    print_success "All Python packages available"
}

# Setup directory structure
setup_directories() {
    print_header "Setting Up Directory Structure"

    # Create directories if they don't exist
    mkdir -p obsidian-vault/posts
    mkdir -p obsidian-vault/attachments
    mkdir -p static/images

    print_success "Directory structure ready"
}

# Convert Obsidian to Hugo
convert_notes() {
    print_header "Converting Obsidian Notes to Hugo Posts"

    if [ ! -d "obsidian-vault/posts" ] || [ -z "$(ls -A obsidian-vault/posts 2>/dev/null)" ]; then
        print_warning "No Obsidian notes found in obsidian-vault/posts/"
        print_status "Please create your Obsidian notes in the obsidian-vault/posts/ directory"
        return 0
    fi

    print_status "Running conversion..."
    python3 scripts/obsidian_to_hugo_converter.py --source ./obsidian-vault --output ./content/posts

    if [ $? -eq 0 ]; then
        print_success "Conversion completed successfully"
    else
        print_error "Conversion failed"
        exit 1
    fi
}

# Serve Hugo site locally
serve_site() {
    print_header "Starting Hugo Development Server"

    print_status "Hugo server will start on http://localhost:1313"
    print_status "Press Ctrl+C to stop the server"
    print_status "Using development config with localhost URLs"
    echo ""

    hugo server --config hugo.toml,config-development.toml --buildDrafts --buildExpired --buildFuture --disableFastRender --bind 0.0.0.0 --port 1313
}

# Build site for production
build_site() {
    print_header "Building Site for Production"

    print_status "Building site (including future posts)..."
    hugo --minify --buildExpired --buildFuture

    if [ $? -eq 0 ]; then
        print_success "Site built successfully in public/"
    else
        print_error "Build failed"
        exit 1
    fi
}

# Watch mode - convert on changes
watch_mode() {
    print_header "Watch Mode - Auto Convert on Changes"

    print_status "Watching obsidian-vault/posts/ for changes..."
    print_status "Press Ctrl+C to stop"
    echo ""

    # Use inotifywait if available, otherwise use simple polling
    if command -v inotifywait &> /dev/null; then
        inotifywait -m -r -e modify,create,move --format '%w%f %e' obsidian-vault/posts/ |
        while read file event; do
            if [[ "$file" == *.md ]]; then
                print_status "Change detected: $file"
                convert_notes
                print_success "Auto-converted successfully"
            fi
        done
    else
        print_warning "inotifywait not found. Using simple polling (less efficient)"
        while true; do
            convert_notes
            sleep 5
        done
    fi
}

# Clean generated files
clean() {
    print_header "Cleaning Generated Files"

    print_status "Removing generated content..."
    rm -rf content/posts/*
    rm -rf static/images/*

    print_success "Cleaned successfully"
}

# Show help
show_help() {
    cat << EOF
Obsidian to Hugo Blog Workflow

Usage: $0 [COMMAND]

Commands:
    convert    Convert Obsidian notes to Hugo posts
    serve      Start Hugo development server (http://localhost:1313)
    build      Build site for production
    watch      Watch for changes and auto-convert
    clean      Remove generated content
    setup      Setup directory structure
    check      Check dependencies
    help       Show this help message

Examples:
    $0 setup                # Initial setup
    $0 convert              # Convert notes
    $0 serve                # Start dev server
    $0 watch                # Watch for changes
    $0 build                # Build for production

Workflow:
    1. Run '$0 setup' initially
    2. Create your Obsidian notes in obsidian-vault/posts/
    3. Run '$0 convert' to convert to Hugo format
    4. Run '$0 serve' to preview your blog
    5. When ready, run '$0 build' to create production build

EOF
}

# Main script logic
main() {
    case "${1:-help}" in
        convert)
            check_dependencies
            setup_directories
            convert_notes
            ;;
        serve)
            check_dependencies
            convert_notes
            serve_site
            ;;
        build)
            check_dependencies
            convert_notes
            build_site
            ;;
        watch)
            check_dependencies
            setup_directories
            watch_mode
            ;;
        clean)
            clean
            ;;
        setup)
            check_dependencies
            setup_directories
            ;;
        check)
            check_dependencies
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "Unknown command: $1"
            show_help
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
