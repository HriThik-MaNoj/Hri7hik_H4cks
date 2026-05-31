#!/usr/bin/env python3
"""
Build the Writer's Guide PDF from the markdown source.
Uses python-markdown + weasyprint with a print-optimized stylesheet.
"""

import sys
from pathlib import Path
import markdown
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

ROOT = Path(__file__).resolve().parent.parent
MD_PATH = ROOT / "docs" / "WRITERS_GUIDE.md"
PDF_PATH = ROOT / "docs" / "WRITERS_GUIDE.pdf"

PRINT_CSS = """
@page {
    size: A4;
    margin: 18mm 16mm 22mm 16mm;
    @bottom-center {
        content: "Hri7hik H4cks  —  Writer's Guide  —  page " counter(page) " / " counter(pages);
        font-family: 'Inter', sans-serif;
        font-size: 9pt;
        color: #6b7280;
    }
    @top-right {
        content: string(chapter);
        font-family: 'Inter', sans-serif;
        font-size: 9pt;
        color: #6b7280;
    }
}

@page :first {
    @bottom-center { content: ""; }
    @top-right { content: ""; }
}

* { box-sizing: border-box; }

html { font-size: 10.5pt; }

body {
    font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif;
    color: #111827;
    line-height: 1.55;
    margin: 0;
}

/* Cover-style first H1 */
h1 {
    font-size: 26pt;
    color: #0f172a;
    border-bottom: 3px solid #06b6d4;
    padding-bottom: 8pt;
    margin: 0 0 16pt 0;
    page-break-after: avoid;
    string-set: chapter content();
}

h1:not(:first-of-type) {
    font-size: 20pt;
    margin-top: 26pt;
    border-bottom: 2px solid #06b6d4;
    padding-bottom: 5pt;
    page-break-before: always;
}

h2 {
    font-size: 15pt;
    color: #0f172a;
    margin-top: 18pt;
    margin-bottom: 8pt;
    page-break-after: avoid;
    border-left: 4px solid #06b6d4;
    padding-left: 10pt;
}

h3 {
    font-size: 12pt;
    color: #1f2937;
    margin-top: 12pt;
    margin-bottom: 5pt;
    page-break-after: avoid;
}

h4 {
    font-size: 10.5pt;
    color: #374151;
    margin-top: 10pt;
    margin-bottom: 4pt;
    page-break-after: avoid;
}

p {
    margin: 0 0 8pt 0;
    text-align: left;
    orphans: 3;
    widows: 3;
}

strong { color: #0f172a; }

em { color: #475569; }

/* Inline code */
code {
    font-family: 'JetBrains Mono', 'Consolas', 'Courier New', monospace;
    font-size: 9.2pt;
    background: #f1f5f9;
    color: #0f172a;
    padding: 1pt 4pt;
    border-radius: 3pt;
    border: 1px solid #e2e8f0;
    word-wrap: break-word;
}

/* Code blocks */
pre {
    font-family: 'JetBrains Mono', 'Consolas', 'Courier New', monospace;
    font-size: 8.8pt;
    line-height: 1.45;
    background: #0f172a;
    color: #e2e8f0;
    padding: 9pt 12pt;
    border-radius: 5pt;
    margin: 8pt 0;
    border-left: 3px solid #06b6d4;
    overflow-wrap: break-word;
    word-wrap: break-word;
    white-space: pre-wrap;
    page-break-inside: avoid;
}

pre code {
    background: transparent;
    color: inherit;
    border: none;
    padding: 0;
    font-size: inherit;
}

/* Lists */
ul, ol {
    margin: 4pt 0 8pt 0;
    padding-left: 22pt;
}

li {
    margin: 2pt 0;
}

li > p { margin: 0 0 3pt 0; }

/* Tables */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 8pt 0 12pt 0;
    font-size: 9.5pt;
    page-break-inside: avoid;
}

th {
    background: #0f172a;
    color: #f1f5f9;
    text-align: left;
    padding: 6pt 8pt;
    font-weight: 600;
    border: 1px solid #1e293b;
}

td {
    padding: 5pt 8pt;
    border: 1px solid #cbd5e1;
    vertical-align: top;
}

tr:nth-child(even) td { background: #f8fafc; }

/* Blockquotes (used for tip callouts in markdown) */
blockquote {
    background: #fef3c7;
    border-left: 4px solid #f59e0b;
    margin: 10pt 0;
    padding: 8pt 12pt;
    color: #78350f;
    border-radius: 0 4pt 4pt 0;
    page-break-inside: avoid;
}

blockquote p { margin: 0; }

blockquote strong { color: #78350f; }

/* Links */
a {
    color: #0891b2;
    text-decoration: none;
    word-break: break-word;
}

/* Horizontal rule */
hr {
    border: none;
    border-top: 1px solid #cbd5e1;
    margin: 14pt 0;
}

/* Cover block (the title + subtitle at very top of guide) */
body > h1:first-child + p > strong {
    display: block;
    font-size: 13pt;
    color: #06b6d4;
    margin-bottom: 14pt;
    font-weight: 500;
}

/* Make the very first paragraph after the title look like a subtitle */
body > h1:first-child + p {
    font-size: 13pt;
    color: #06b6d4;
    font-weight: 500;
    margin-bottom: 22pt;
}

/* Avoid orphan headers */
h1, h2, h3, h4 { page-break-after: avoid; }
"""


def main():
    if not MD_PATH.exists():
        print(f"ERROR: {MD_PATH} not found", file=sys.stderr)
        sys.exit(1)

    md_text = MD_PATH.read_text(encoding="utf-8")

    md = markdown.Markdown(extensions=[
        "extra",          # tables, fenced code, footnotes, etc.
        "sane_lists",
        "smarty",
        "toc",
        "codehilite",
    ], extension_configs={
        "codehilite": {
            "css_class": "codehilite",
            "guess_lang": False,
        },
    })

    html_body = md.convert(md_text)

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Hri7hik H4cks — Writer's Guide</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
</head>
<body>
{html_body}
</body>
</html>
"""

    font_config = FontConfiguration()
    css = CSS(string=PRINT_CSS, font_config=font_config)

    print(f"Rendering {MD_PATH.name} -> {PDF_PATH.name} ...")
    HTML(string=full_html, base_url=str(ROOT)).write_pdf(
        target=str(PDF_PATH),
        stylesheets=[css],
        font_config=font_config,
    )

    size_kb = PDF_PATH.stat().st_size / 1024
    print(f"Done. {PDF_PATH} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
