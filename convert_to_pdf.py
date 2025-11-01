#!/usr/bin/env python3
"""
Convert Markdown Guide to PDF
Converts the NEW_BLOG_CREATION_GUIDE.md to a beautifully formatted PDF
"""

import markdown
import weasyprint
import os
import sys

def convert_markdown_to_pdf(markdown_file, output_pdf):
    """Convert markdown file to PDF with custom styling."""

    # Read markdown file
    with open(markdown_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    # Convert markdown to HTML
    md = markdown.Markdown(extensions=[
        'markdown.extensions.toc',
        'markdown.extensions.tables',
        'markdown.extensions.fenced_code',
        'markdown.extensions.codehilite'
    ])

    html_content = md.convert(markdown_content)

    # Create complete HTML document with CSS
    html_document = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Blog Creation Guide</title>
    <style>
        @page {{
            size: A4;
            margin: 2cm;
            @bottom-center {{
                content: "Blog Creation Guide - Page " counter(page);
                font-size: 10pt;
                color: #666;
            }}
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 100%;
        }}

        h1 {{
            color: #2c3e50;
            font-size: 2.5em;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-top: 30px;
            page-break-before: always;
        }}

        h1:first-of-type {{
            page-break-before: avoid;
            border-bottom: 3px solid #e74c3c;
            color: #e74c3c;
        }}

        h2 {{
            color: #2980b9;
            font-size: 1.8em;
            margin-top: 30px;
            border-bottom: 2px solid #3498db;
            padding-bottom: 5px;
        }}

        h3 {{
            color: #16a085;
            font-size: 1.4em;
            margin-top: 25px;
        }}

        h4 {{
            color: #27ae60;
            font-size: 1.2em;
            margin-top: 20px;
        }}

        h5 {{
            color: #8e44ad;
            font-size: 1.1em;
            margin-top: 15px;
        }}

        p {{
            margin: 10px 0;
            text-align: justify;
        }}

        ul, ol {{
            margin: 10px 0;
            padding-left: 30px;
        }}

        li {{
            margin: 5px 0;
        }}

        code {{
            background-color: #f5f5f5;
            padding: 2px 5px;
            border-radius: 3px;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 0.9em;
        }}

        pre {{
            background-color: #2c3e50;
            color: #ecf0f1;
            padding: 20px;
            border-radius: 5px;
            overflow-x: auto;
            page-break-inside: avoid;
        }}

        pre code {{
            background-color: transparent;
            padding: 0;
            color: #ecf0f1;
        }}

        blockquote {{
            border-left: 4px solid #3498db;
            margin: 20px 0;
            padding: 10px 20px;
            background-color: #ecf0f1;
            font-style: italic;
        }}

        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
            page-break-inside: avoid;
        }}

        table, th, td {{
            border: 1px solid #bdc3c7;
        }}

        th {{
            background-color: #3498db;
            color: white;
            padding: 12px;
            text-align: left;
        }}

        td {{
            padding: 10px;
        }}

        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}

        .page-break {{
            page-break-before: always;
        }}

        strong {{
            color: #2c3e50;
        }}

        em {{
            color: #7f8c8d;
        }}

        hr {{
            border: none;
            border-top: 2px solid #bdc3c7;
            margin: 30px 0;
        }}

        .toc {{
            background-color: #ecf0f1;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }}

        .toc ul {{
            list-style-type: none;
            padding-left: 0;
        }}

        .toc li {{
            margin: 8px 0;
        }}

        /* Syntax highlighting */
        .highlight .k {{ color: #ff6b6b; font-weight: bold; }}
        .highlight .s {{ color: #51cf66; }}
        .highlight .n {{ color: #f8f9fa; }}
        .highlight .o {{ color: #ffd43b; }}
        .highlight .c {{ color: #868e96; font-style: italic; }}
    </style>
</head>
<body>
    {html_content}
</body>
</html>
    """

    # Convert HTML to PDF
    print(f"Converting {markdown_file} to {output_pdf}...")
    weasyprint.HTML(string=html_document).write_pdf(output_pdf)
    print(f"✅ PDF created successfully: {output_pdf}")

def main():
    markdown_file = "NEW_BLOG_CREATION_GUIDE.md"
    output_pdf = "NEW_BLOG_CREATION_GUIDE.pdf"

    # Check if markdown file exists
    if not os.path.exists(markdown_file):
        print(f"❌ Error: {markdown_file} not found!")
        sys.exit(1)

    # Convert to PDF
    try:
        convert_markdown_to_pdf(markdown_file, output_pdf)
        print("\n🎉 Conversion complete!")
        print(f"📄 PDF saved as: {output_pdf}")

        # Show file size
        file_size = os.path.getsize(output_pdf)
        print(f"📊 File size: {file_size / 1024:.2f} KB")

    except Exception as e:
        print(f"❌ Error during conversion: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
