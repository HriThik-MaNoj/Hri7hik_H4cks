#!/usr/bin/env python3
"""
obsidian_to_hugo_converter.py
=============================
Fast, incremental Obsidian → Hugo converter.

Design goals
------------
- Idempotent: same input ⇒ identical output, byte-for-byte.
- Incremental: skip files whose source SHA-1 matches the last successful run.
- Parallel: thread pool for IO + Pillow (PIL releases the GIL during encode).
- Pre-compiled regex: every pattern compiled once at module load.
- Single read: source bytes are read exactly once and reused for hash + body.
- Defensive: malformed YAML, missing images, and empty configs degrade
  gracefully with a logged warning rather than aborting the whole run.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import re
import shutil
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import yaml
from PIL import Image


# ─── Logging ──────────────────────────────────────────────────────────────────

class _Color:
    R = "\033[0;31m"; G = "\033[0;32m"; Y = "\033[1;33m"
    B = "\033[0;34m"; C = "\033[0;36m"; D = "\033[2m"; X = "\033[0m"


class _Fmt(logging.Formatter):
    LVL = {
        "DEBUG":   f"{_Color.D}[dbg ]{_Color.X}",
        "INFO":    f"{_Color.B}[INFO]{_Color.X}",
        "WARNING": f"{_Color.Y}[WARN]{_Color.X}",
        "ERROR":   f"{_Color.R}[ERR ]{_Color.X}",
    }
    OK = f"{_Color.G}[ OK ]{_Color.X}"

    def format(self, rec: logging.LogRecord) -> str:
        prefix = self.OK if getattr(rec, "ok", False) else self.LVL.get(rec.levelname, rec.levelname)
        return f"{prefix} {rec.getMessage()}"


def _setup_logging(verbose: bool) -> None:
    h = logging.StreamHandler(sys.stderr)
    h.setFormatter(_Fmt())
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        handlers=[h],
        force=True,
    )


log = logging.getLogger("o2h")


def _ok(msg: str) -> None:
    log.info(msg, extra={"ok": True})


# ─── Pre-compiled patterns (compile once, reuse forever) ──────────────────────

_RE_FRONTMATTER = re.compile(r"^---\s*\n(.*?\n)---\s*\n?", re.DOTALL)
_RE_WIKILINK    = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")
_RE_CALLOUT     = re.compile(r"^> \[!(\w+)\][ \t]*([^\n]*)\n((?:^>.*\n?)*)", re.MULTILINE)
_RE_CODEBLOCK   = re.compile(r"```([\w+\-]*)\n(.*?)```", re.DOTALL)
_RE_IMAGE       = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)\)")
_RE_DIFFICULTY  = re.compile(r"\bdifficulty[:\s\"']+(beginner|intermediate|advanced)\b", re.IGNORECASE)
_RE_PLATFORMS   = re.compile(r"\b(hackthebox|tryhackme|picoctf|vulnhub|overthewire)\b", re.IGNORECASE)
# Tools: matched ONLY inside fenced code blocks → drastically fewer false positives.
_RE_TOOL = re.compile(
    r"\b(nmap|netcat|wireshark|burp(?:suite)?|sqlmap|metasploit|msfvenom|john|hashcat|"
    r"gobuster|dirb|dirbuster|nikto|nessus|openvas|hydra|aircrack-ng|responder|impacket|"
    r"crackmapexec|bloodhound|ffuf|wfuzz|enum4linux|smbclient|smbmap|rpcclient|"
    r"evil-winrm|chisel|ligolo|mimikatz)\b",
    re.IGNORECASE,
)
_RE_MD_NOISE = re.compile(r"[*_`#\[\]()]+")
_RE_MULTISPACE = re.compile(r"\s+")

CALLOUT_MAP: dict[str, tuple[str, str]] = {
    "note":     ("callout-info",    "📝"),
    "info":     ("callout-info",    "ℹ️"),
    "tip":      ("callout-success", "💡"),
    "success":  ("callout-success", "✅"),
    "warning":  ("callout-warning", "⚠️"),
    "danger":   ("callout-danger",  "🚨"),
    "question": ("callout-info",    "❓"),
    "abstract": ("callout-info",    "📄"),
    "example":  ("callout-success", "📌"),
}

DEFAULT_CONFIG: dict[str, Any] = {
    "obsidian_vault":               "./obsidian-vault",
    "hugo_content":                 "./content/posts",
    "hugo_static":                  "./static/images",
    "obsidian_attachments_folder":  "attachments",
    "auto_copy_images":             True,
    "optimize_images":              True,
    "image_max_width":              1200,
    "image_quality":                85,
    "create_missing_frontmatter":   True,
    "default_draft":                False,
    "default_categories":           ["General"],
    "auto_extract_tools":           True,
    "auto_extract_platforms":       True,
    "auto_extract_difficulty":      True,
    "generate_description":         True,
    "cache_dir":                    ".cache/o2h",
    "max_workers":                  0,   # 0 = auto (cpu_count, capped at job count)
}


# ─── Config loader ────────────────────────────────────────────────────────────

def load_config(path: str | Path) -> dict[str, Any]:
    cfg = DEFAULT_CONFIG.copy()
    p = Path(path)
    if p.is_file():
        try:
            with p.open("r", encoding="utf-8") as f:
                user = yaml.safe_load(f) or {}
            if isinstance(user, dict):
                cfg.update(user)
            else:
                log.warning(f"{p} did not parse to a mapping — ignoring")
        except yaml.YAMLError as e:
            log.warning(f"Bad YAML in {p}: {e} — using defaults")
    return cfg


# ─── Incremental cache (SHA-1 manifest) ───────────────────────────────────────

@dataclass
class Cache:
    path: Path
    entries: dict[str, str] = field(default_factory=dict)

    @classmethod
    def load(cls, cache_file: Path) -> "Cache":
        if cache_file.is_file():
            try:
                return cls(path=cache_file, entries=json.loads(cache_file.read_text()))
            except (json.JSONDecodeError, OSError) as e:
                log.debug(f"cache load failed ({e}) — fresh start")
        return cls(path=cache_file)

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        # Compact JSON keeps the manifest tiny on disk.
        self.path.write_text(json.dumps(self.entries, separators=(",", ":")))

    def is_unchanged(self, key: str, digest: str) -> bool:
        return self.entries.get(key) == digest


def _sha1(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()


# ─── Converter core ───────────────────────────────────────────────────────────

class Converter:
    """Stateless transforms + a thread-safe image dedup cache."""

    def __init__(self, config: dict[str, Any]):
        self.cfg = config
        self.attach_name = config["obsidian_attachments_folder"]
        self.image_dest_root = Path(config["hugo_static"]).resolve()
        self._images_done: dict[Path, str] = {}
        self._images_lock = threading.Lock()

    # ─── Front matter ────────────────────────────────────────────────────────

    @staticmethod
    def _split_frontmatter(text: str) -> tuple[dict, str]:
        m = _RE_FRONTMATTER.match(text)
        if not m:
            return {}, text
        try:
            fm = yaml.safe_load(m.group(1)) or {}
        except yaml.YAMLError as e:
            log.warning(f"Malformed front matter — keeping body, dropping fm: {e}")
            return {}, text[m.end():]
        return fm if isinstance(fm, dict) else {}, text[m.end():]

    @staticmethod
    def _title_from_filename(stem: str) -> str:
        return " ".join(w.capitalize() for w in stem.replace("_", " ").replace("-", " ").split())

    def _fill_frontmatter(self, fm: dict, src: Path, body: str) -> dict:
        if not self.cfg["create_missing_frontmatter"]:
            return dict(fm)

        fm = dict(fm)
        fm.setdefault("title", self._title_from_filename(src.stem))

        if "date" not in fm:
            ts = src.stat().st_mtime
            fm["date"] = datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        fm.setdefault("draft", self.cfg["default_draft"])
        fm.setdefault("categories", list(self.cfg["default_categories"]))

        if self.cfg["auto_extract_difficulty"] and "difficulties" not in fm:
            m = _RE_DIFFICULTY.search(body)
            if m:
                fm["difficulties"] = [m.group(1).lower()]

        if self.cfg["auto_extract_platforms"] and "platforms" not in fm:
            plats = {p.lower() for p in _RE_PLATFORMS.findall(body)}
            if plats:
                fm["platforms"] = sorted(plats)

        if self.cfg["auto_extract_tools"] and "tools" not in fm:
            # Tools harvested ONLY from inside fenced code → no prose noise.
            tools: set[str] = set()
            for cb in _RE_CODEBLOCK.finditer(body):
                tools.update(t.lower() for t in _RE_TOOL.findall(cb.group(2)))
            if tools:
                fm["tools"] = sorted(tools)

        if self.cfg["generate_description"] and "description" not in fm:
            for para in body.split("\n\n"):
                p = para.strip()
                if not p or p.startswith(("#", "<", ">", "```", "---")):
                    continue
                cleaned = _RE_MULTISPACE.sub(" ", _RE_MD_NOISE.sub("", p)).strip()
                if cleaned:
                    fm["description"] = cleaned[:157] + "..." if len(cleaned) > 160 else cleaned
                    break

        return fm

    # ─── Inline transforms ───────────────────────────────────────────────────

    @staticmethod
    def _wikilink_repl(m: re.Match) -> str:
        target = m.group(1).strip()
        label = (m.group(2) or target).strip()
        slug = _RE_MULTISPACE.sub("-", target).lower().replace("_", "-")
        return f"[{label}](/posts/{slug}/)"

    @classmethod
    def transform_wikilinks(cls, text: str) -> str:
        return _RE_WIKILINK.sub(cls._wikilink_repl, text)

    @staticmethod
    def _callout_repl(m: re.Match) -> str:
        kind = m.group(1).lower()
        title = (m.group(2) or "").strip()
        body = m.group(3)
        cls, icon = CALLOUT_MAP.get(kind, ("callout-info", "📄"))
        if not title:
            title = f"{icon} {kind.capitalize()}"
        # Strip the leading "> " from each continuation line.
        lines = [
            ln[2:] if ln.startswith("> ") else (ln[1:].lstrip() if ln.startswith(">") else ln)
            for ln in body.splitlines()
        ]
        inner = "\n".join(lines).rstrip()
        return (
            f'<div class="callout {cls}">\n'
            f'<div class="callout-title">{title}</div>\n\n'
            f"{inner}\n"
            f"</div>"
        )

    @classmethod
    def transform_callouts(cls, text: str) -> str:
        return _RE_CALLOUT.sub(cls._callout_repl, text)

    @staticmethod
    def add_copy_markers(text: str) -> str:
        return _RE_CODEBLOCK.sub(
            lambda m: f"```{m.group(1)}\n{m.group(2)}```\n\n<!-- COPY_BUTTON -->",
            text,
        )

    # ─── Images ──────────────────────────────────────────────────────────────

    def transform_images(self, text: str, src_dir: Path) -> str:
        if not self.cfg["auto_copy_images"]:
            return text

        attach = self.attach_name

        def repl(m: re.Match) -> str:
            alt, ref = m.group(1), m.group(2)
            if ref.startswith(("http://", "https://", "/")):
                return m.group(0)

            tail = ref[len(attach) + 1:] if ref.startswith(attach + "/") else ref
            for cand in (
                src_dir / ref,
                src_dir / attach / tail,
                src_dir.parent / attach / tail,
            ):
                if cand.is_file():
                    name = self._copy_image(cand.resolve())
                    return f"![{alt}](/images/{name})"

            log.warning(f"Image not found: {ref} (relative to {src_dir})")
            return m.group(0)

        return _RE_IMAGE.sub(repl, text)

    def _copy_image(self, src: Path) -> str:
        # Fast path: already handled in this run.
        with self._images_lock:
            cached = self._images_done.get(src)
            if cached is not None:
                return cached

        # Heavy work outside the lock; mtime gate makes duplicate work harmless.
        self.image_dest_root.mkdir(parents=True, exist_ok=True)
        dest = self.image_dest_root / src.name
        if (not dest.exists()) or src.stat().st_mtime > dest.stat().st_mtime:
            ext = src.suffix.lower()
            if self.cfg["optimize_images"] and ext in {".jpg", ".jpeg", ".png"}:
                self._optimize_image(src, dest)
            else:
                shutil.copy2(src, dest)
            log.debug(f"image: {src.name} → {dest.name}")

        with self._images_lock:
            self._images_done[src] = dest.name
        return dest.name

    def _optimize_image(self, src: Path, dest: Path) -> None:
        try:
            with Image.open(src) as img:
                ext = src.suffix.lower()

                # Resize only when wider than the configured cap.
                mw = int(self.cfg["image_max_width"])
                if img.width > mw:
                    h = round(img.height * mw / img.width)
                    img = img.resize((mw, h), Image.Resampling.LANCZOS)

                if ext in (".jpg", ".jpeg"):
                    if img.mode != "RGB":
                        img = img.convert("RGB")
                    img.save(dest, "JPEG", quality=int(self.cfg["image_quality"]), optimize=True)
                else:
                    # Preserve transparency for PNGs — never silently re-encode as JPEG.
                    img.save(dest, "PNG", optimize=True)
        except Exception as e:
            log.warning(f"Optimize failed ({src.name}): {e} — copying raw")
            shutil.copy2(src, dest)

    # ─── Front matter writer (Hugo-friendly inline arrays) ───────────────────

    @staticmethod
    def _yaml_scalar(v: Any) -> str:
        if isinstance(v, bool):
            return "true" if v else "false"
        if isinstance(v, (int, float)):
            return str(v)
        s = str(v).replace("\\", "\\\\").replace('"', '\\"')
        return f'"{s}"'

    def _kv(self, k: str, v: Any) -> str:
        if isinstance(v, list):
            inner = ", ".join(self._yaml_scalar(x) for x in v)
            return f"{k}: [{inner}]"
        return f"{k}: {self._yaml_scalar(v)}"

    _PRIMARY = ("title", "date", "draft", "description",
                "categories", "tags", "difficulties", "platforms", "tools")

    def render_frontmatter(self, fm: dict) -> str:
        seen: set[str] = set()
        lines: list[str] = []
        for k in self._PRIMARY:
            if k in fm:
                lines.append(self._kv(k, fm[k]))
                seen.add(k)
        for k, v in fm.items():
            if k not in seen:
                lines.append(self._kv(k, v))
        return "\n".join(lines)

    # ─── Per-file pipeline ───────────────────────────────────────────────────

    def convert_text(self, src: Path, raw: str) -> str:
        fm, body = self._split_frontmatter(raw)
        body = self.transform_wikilinks(body)
        body = self.transform_callouts(body)
        body = self.add_copy_markers(body)
        body = self.transform_images(body, src.parent)
        fm = self._fill_frontmatter(fm, src, body)
        return f"---\n{self.render_frontmatter(fm)}\n---\n\n{body.lstrip()}"


# ─── Driver ───────────────────────────────────────────────────────────────────

def _iter_markdown(root: Path) -> Iterable[Path]:
    for p in root.rglob("*.md"):
        rel = p.relative_to(root)
        if any(part.startswith(".") for part in rel.parts):
            continue
        yield p


def _output_path(src: Path, src_root: Path, out_root: Path) -> Path:
    rel = src.relative_to(src_root)
    # obsidian-vault/posts/foo.md  →  content/posts/foo.md  (drop the redundant 'posts/').
    if rel.parts and rel.parts[0] == "posts":
        rel = Path(*rel.parts[1:])
    return out_root / rel


def _convert_one(c: Converter, src: Path, dest: Path, raw: str) -> None:
    out = c.convert_text(src, raw)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(out, encoding="utf-8")


def run(source: Path, output: Path, config_path: Path,
        force: bool = False, verbose: bool = False) -> int:
    _setup_logging(verbose)

    if not source.is_dir():
        log.error(f"Source not found: {source}")
        return 2

    cfg = load_config(config_path)
    cache_file = Path(cfg["cache_dir"]) / "manifest.json"
    cache = Cache.load(cache_file)

    files = list(_iter_markdown(source))
    if not files:
        log.warning(f"No .md found in {source}")
        return 0

    converter = Converter(cfg)

    # ── Plan: read each source once, hash, decide skip vs. convert. ───────────
    pending: list[tuple[Path, Path, str]] = []
    new_cache: dict[str, str] = {}
    skipped = 0

    for src in files:
        try:
            data = src.read_bytes()
        except OSError as e:
            log.error(f"read {src}: {e}")
            continue
        digest = _sha1(data)
        rel_key = str(src.relative_to(source))
        new_cache[rel_key] = digest
        dest = _output_path(src, source, output)

        if (not force) and dest.exists() and cache.is_unchanged(rel_key, digest):
            skipped += 1
            continue

        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as e:
            log.error(f"decode {src}: {e}")
            continue

        pending.append((src, dest, text))

    if not pending:
        _ok(f"Up-to-date ({skipped} files cached)")
        cache.entries = new_cache
        cache.save()
        return 0

    workers_cfg = int(cfg.get("max_workers") or 0)
    workers = workers_cfg if workers_cfg > 0 else (os.cpu_count() or 4)
    workers = max(1, min(workers, len(pending)))

    log.info(f"Converting {len(pending)} files ({skipped} cached) — {workers} worker(s)")

    t0 = datetime.now()
    errors = 0

    if workers == 1:
        for src, dest, raw in pending:
            try:
                _convert_one(converter, src, dest, raw)
            except Exception as e:
                log.error(f"{src.name}: {e}")
                errors += 1
    else:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = {
                pool.submit(_convert_one, converter, s, d, r): s
                for s, d, r in pending
            }
            for fut in as_completed(futures):
                src = futures[fut]
                try:
                    fut.result()
                except Exception as e:
                    log.error(f"{src.name}: {e}")
                    errors += 1

    cache.entries = new_cache
    cache.save()

    ms = int((datetime.now() - t0).total_seconds() * 1000)
    if errors:
        log.error(f"{errors} file(s) failed")
    _ok(f"Converted {len(pending) - errors}/{len(pending)} in {ms}ms")
    return 1 if errors else 0


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser(
        prog="o2h",
        description="Obsidian → Hugo converter (fast, incremental, parallel)",
    )
    ap.add_argument("--source", default="./obsidian-vault",
                    help="Source vault root (default: ./obsidian-vault)")
    ap.add_argument("--output", default="./content/posts",
                    help="Hugo content/posts dir (default: ./content/posts)")
    ap.add_argument("--config", default="scripts/config.yaml",
                    help="Path to config.yaml")
    ap.add_argument("--force", action="store_true",
                    help="Bypass cache; reconvert every file")
    ap.add_argument("--clean-cache", action="store_true",
                    help="Delete the conversion cache, then exit")
    ap.add_argument("-v", "--verbose", action="store_true",
                    help="Debug logging")
    args = ap.parse_args()

    _setup_logging(args.verbose)

    if args.clean_cache:
        cfg = load_config(Path(args.config))
        p = Path(cfg["cache_dir"]) / "manifest.json"
        if p.exists():
            p.unlink()
            _ok(f"Cache cleared: {p}")
        else:
            log.info("No cache to clear.")
        return 0

    return run(
        Path(args.source),
        Path(args.output),
        Path(args.config),
        force=args.force,
        verbose=args.verbose,
    )


if __name__ == "__main__":
    sys.exit(main())
