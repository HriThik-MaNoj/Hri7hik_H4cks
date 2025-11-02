#!/usr/bin/env python3
"""
Obsidian to Hugo Converter
===========================
Converts Obsidian-flavored markdown to Hugo-compatible markdown with automated image handling,
syntax conversion, and front matter generation.
"""

import os
import re
import yaml
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import frontmatter
from PIL import Image
import argparse


class ObsidianToHugoConverter:
    """Converts Obsidian markdown to Hugo-compatible markdown."""

    def __init__(self, config_path: str = "scripts/config.yaml"):
        """Initialize the converter with configuration."""
        self.config = self.load_config(config_path)
        self.processed_images = set()

    def load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file."""
        default_config = {
            "obsidian_vault": "./obsidian-vault",
            "hugo_content": "./content/posts",
            "hugo_static": "./static/images",
            "auto_copy_images": True,
            "optimize_images": True,
            "image_max_width": 1200,
            "image_quality": 85,
            "create_missing_frontmatter": True,
            "default_draft": False,
            "default_categories": ["General"],
            "obsidian_attachments_folder": "attachments",
            "image_storage_strategy": "by-post"
        }

        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                user_config = yaml.safe_load(f)
                default_config.update(user_config)

        return default_config

    def process_file(self, obsidian_file: Path, output_file: Path) -> None:
        """Process a single Obsidian markdown file and convert it to Hugo format."""
        print(f"Converting: {obsidian_file} -> {output_file}")

        # Read the Obsidian markdown file
        with open(obsidian_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Handle front matter
        content, front_matter = self.extract_and_process_frontmatter(content, obsidian_file)

        # Convert Obsidian-specific syntax to Hugo-compatible syntax
        content = self.convert_wikilinks_to_links(content)
        content = self.convert_callouts(content)
        content = self.add_copy_buttons_to_codeblocks(content)

        # Process images
        content = self.process_images_in_content(content, obsidian_file.parent)

        # Write the converted content
        self.write_converted_file(output_file, content, front_matter)

    def extract_and_process_frontmatter(self, content: str, file_path: Path) -> tuple:
        """Extract and process front matter from markdown."""
        # Check if file already has front matter
        if content.startswith('---'):
            # Split existing front matter and content
            parts = content.split('---', 2)
            if len(parts) >= 3:
                existing_frontmatter = yaml.safe_load(parts[1])
                content = parts[2]
            else:
                existing_frontmatter = {}
        else:
            existing_frontmatter = {}

        # Generate front matter if needed
        front_matter = self.generate_frontmatter(file_path, existing_frontmatter)

        return content, front_matter

    def generate_frontmatter(self, file_path: Path, existing_frontmatter: Dict) -> Dict:
        """Generate Hugo front matter from filename and content."""
        if not self.config["create_missing_frontmatter"] and existing_frontmatter:
            return existing_frontmatter

        front_matter = existing_frontmatter.copy() if existing_frontmatter else {}

        # Generate title from filename if not present
        if 'title' not in front_matter:
            front_matter['title'] = self.title_from_filename(file_path.stem)

        # Generate date from file creation if not present
        if 'date' not in front_matter:
            try:
                timestamp = file_path.stat().st_ctime
                front_matter['date'] = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%dT%H:%M:%S%z')
            except:
                front_matter['date'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')

        # Set draft status
        if 'draft' not in front_matter:
            front_matter['draft'] = self.config["default_draft"]

        # Add default categories if none exist
        if 'categories' not in front_matter:
            front_matter['categories'] = self.config["default_categories"]

        # Extract metadata from content
        self.extract_metadata_from_content(front_matter, file_path.read_text(encoding='utf-8'))

        return front_matter

    def title_from_filename(self, filename: str) -> str:
        """Convert filename to title case."""
        # Replace underscores and hyphens with spaces
        title = filename.replace('_', ' ').replace('-', ' ')
        # Title case
        title = ' '.join(word.capitalize() for word in title.split())
        return title

    def extract_metadata_from_content(self, front_matter: Dict, content: str) -> None:
        """Extract metadata from content (difficulty, platforms, tools, etc.)."""
        # Extract difficulty level from content
        difficulty_match = re.search(r' difficulty["\s:]+(beginner|intermediate|advanced)', content, re.IGNORECASE)
        if difficulty_match and 'difficulties' not in front_matter:
            front_matter['difficulties'] = [difficulty_match.group(1).lower()]

        # Extract platforms mentioned
        platforms = set()
        platform_keywords = ['hackthebox', 'tryhackme', 'picoctf', 'vulnhub', 'overthewire']
        for keyword in platform_keywords:
            if keyword.lower() in content.lower():
                platforms.add(keyword)
        if platforms and 'platforms' not in front_matter:
            front_matter['platforms'] = list(platforms)

        # Extract tools mentioned
        tools = set()
        tool_patterns = [
            r'\b(nmap|netcat|nc|telnet|ssh|wireshark|burp|burpsuite|sqlmap|metasploit|msfvenom|john|hashcat|gobuster|dirb|dirbuster|nikto|nessus|openvas)\b',
            r'\b(git|docker|docker-compose|kubectl|helm|ansible|terraform|jenkins|github|gitlab)\b',
            r'\b(python|python3|bash|sh|powershell|cmd|java|node|npm|yarn)\b'
        ]
        for pattern in tool_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                tools.add(match.lower())
        if tools and 'tools' not in front_matter:
            front_matter['tools'] = list(tools)

        # Generate description from first paragraph
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        if paragraphs and 'description' not in front_matter:
            first_para = paragraphs[0].strip()
            # Remove markdown formatting
            first_para = re.sub(r'[*_`#\[\]()]+', '', first_para)
            # Truncate to 160 characters
            if len(first_para) > 160:
                first_para = first_para[:157] + '...'
            front_matter['description'] = first_para

    def convert_wikilinks_to_links(self, content: str) -> str:
        """Convert Obsidian [[wikilinks]] to standard markdown links."""
        # Pattern: [[link]] or [[link|text]]
        pattern = r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]'
        def replace_wikilink(match):
            link_text = match.group(1).strip()
            display_text = match.group(2).strip() if match.group(2) else link_text
            # Convert to kebab-case for Hugo
            hugo_link = link_text.lower().replace(' ', '-').replace('_', '-')
            return f'[{display_text}](/{hugo_link})'
        return re.sub(pattern, replace_wikilink, content)

    def convert_callouts(self, content: str) -> str:
        """Convert Obsidian callout syntax to HTML callout divs."""
        # Obsidian callout syntax: > [!note] Title
        # Convert to: <div class="callout callout-info"><div class="callout-title">📋 Title</div>content</div>

        callout_types = {
            'note': ('callout-info', '📝'),
            'info': ('callout-info', 'ℹ️'),
            'tip': ('callout-success', '💡'),
            'success': ('callout-success', '✅'),
            'warning': ('callout-warning', '⚠️'),
            'danger': ('callout-danger', '🚨'),
            'question': ('callout-info', '❓'),
            'abstract': ('callout-info', '📄'),
            'example': ('callout-success', '📌'),
        }

        # Pattern for Obsidian callouts
        pattern = r'> \[!(\w+)\]\s*([^\n]+)?\n((?:>.*\n)*)'

        def replace_callout(match):
            callout_type = match.group(1).lower()
            callout_title = match.group(2).strip() if match.group(2) else ''
            callout_content = match.group(3)

            if callout_type in callout_types:
                css_class, icon = callout_types[callout_type]
            else:
                css_class, icon = 'callout-info', '📄'

            if not callout_title:
                callout_title = icon + ' ' + callout_type.capitalize()

            # Clean the content (remove > prefixes)
            callout_content = '\n'.join(line[2:] if line.startswith('> ') else line for line in callout_content.split('\n'))

            return f'<div class="callout {css_class}">\n<div class="callout-title">{callout_title}</div>\n{callout_content}\n</div>'

        return re.sub(pattern, replace_callout, content)

    def add_copy_buttons_to_codeblocks(self, content: str) -> str:
        """Add copy button markers to code blocks."""
        # This is a marker - the actual JavaScript will handle the copy buttons
        # Pattern: ```lang\ncode\n```
        pattern = r'(```)(\w+)?\n(.*?)(```)'

        def replace_codeblock(match):
            lang = match.group(2) if match.group(2) else ''
            code = match.group(3)

            # Add marker for copy button
            return f'{match.group(1)}{lang}\n{code}\n{match.group(4)}\n\n<!-- COPY_BUTTON -->'

        return re.sub(pattern, replace_codeblock, content, flags=re.DOTALL)

    def process_images_in_content(self, content: str, source_dir: Path) -> str:
        """Process images in content - copy them and update references."""
        if not self.config["auto_copy_images"]:
            return content

        # Pattern: ![alt](image.jpg) or ![alt](attachments/image.jpg)
        image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'

        def replace_image(match):
            alt_text = match.group(1)
            image_path = match.group(2)

            # Skip if already absolute URL or external link
            if image_path.startswith(('http://', 'https://', '/')):
                return match.group(0)

            # Handle Obsidian attachments folder
            if image_path.startswith('attachments/'):
                image_path = image_path[12:]  # Remove 'attachments/'

            # Find the image file
            full_image_path = source_dir / image_path
            if not full_image_path.exists():
                # Try in attachments folder
                full_image_path = source_dir / self.config["obsidian_attachments_folder"] / image_path
                if not full_image_path.exists():
                    print(f"Warning: Image not found: {image_path}")
                    return match.group(0)

            # Copy and optimize image
            hugo_image_path = self.copy_and_optimize_image(full_image_path)

            # Return updated reference
            return f'![{alt_text}](/images/{hugo_image_path})'

        return re.sub(image_pattern, replace_image, content)

    def copy_and_optimize_image(self, source_image_path: Path) -> str:
        """Copy and optimize image for Hugo static folder."""
        # Generate destination filename
        dest_filename = source_image_path.name
        dest_path = Path(self.config["hugo_static"]) / dest_filename

        # Handle duplicate filenames
        counter = 1
        original_dest = dest_path
        while dest_path.exists() and dest_path not in self.processed_images:
            stem = source_image_path.stem
            suffix = source_image_path.suffix
            dest_filename = f"{stem}_{counter}{suffix}"
            dest_path = Path(self.config["hugo_static"]) / dest_filename
            counter += 1

        self.processed_images.add(dest_path)

        # Copy file if not already processed
        if not dest_path.exists() or source_image_path.stat().st_mtime > dest_path.stat().st_mtime:
            # Create directory if needed
            dest_path.parent.mkdir(parents=True, exist_ok=True)

            # Optimize if enabled
            if self.config["optimize_images"] and source_image_path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                self.optimize_image(source_image_path, dest_path)
            else:
                shutil.copy2(source_image_path, dest_path)

            print(f"  Image processed: {source_image_path.name} -> {dest_filename}")

        return dest_filename

    def optimize_image(self, source: Path, dest: Path) -> None:
        """Optimize image size and quality."""
        try:
            with Image.open(source) as img:
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background

                # Resize if too large
                max_width = self.config["image_max_width"]
                if img.width > max_width:
                    ratio = max_width / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

                # Save with quality setting
                img.save(dest, 'JPEG', quality=self.config["image_quality"], optimize=True)
        except Exception as e:
            print(f"Warning: Could not optimize {source.name}: {e}")
            shutil.copy2(source, dest)

    def write_converted_file(self, output_path: Path, content: str, front_matter: Dict) -> None:
        """Write the converted markdown file with front matter."""
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Manually format front matter for Hugo compatibility
        # Use inline array syntax: key: ["value1", "value2"]
        lines = []
        for key, value in front_matter.items():
            if isinstance(value, list):
                # Format list as inline array with quoted values
                formatted_values = [f'"{v}"' if isinstance(v, str) else str(v) for v in value]
                lines.append(f'{key}: [{", ".join(formatted_values)}]')
            elif isinstance(value, bool):
                # Format boolean properly
                lines.append(f'{key}: {str(value).lower()}')
            else:
                # Format string/number with quotes
                lines.append(f'{key}: "{value}"')

        front_matter_yaml = '\n'.join(lines)

        # Write file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('---\n')
            f.write(front_matter_yaml)
            f.write('\n---\n\n')
            f.write(content)

    def process_directory(self, source_dir: str, output_dir: str) -> None:
        """Process all markdown files in a directory."""
        source_path = Path(source_dir)
        output_path = Path(output_dir)

        # Find all markdown files
        markdown_files = list(source_path.rglob("*.md"))

        print(f"\nFound {len(markdown_files)} markdown files to convert\n")

        for obsidian_file in markdown_files:
            # Generate output filename (preserve directory structure)
            rel_path = obsidian_file.relative_to(source_path)

            # Skip files in certain directories
            if any(part.startswith('.') for part in rel_path.parts):
                continue

            # Remove 'posts' subdirectory from path if it exists
            # obsidian-vault/posts/*.md should go to content/posts/*.md (not content/posts/posts/*.md)
            if len(rel_path.parts) > 0 and rel_path.parts[0] == 'posts':
                rel_path = Path(*rel_path.parts[1:])

            output_file = output_path / rel_path

            try:
                self.process_file(obsidian_file, output_file)
            except Exception as e:
                print(f"Error processing {obsidian_file}: {e}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Convert Obsidian markdown to Hugo format')
    parser.add_argument('--source', default='./obsidian-vault',
                        help='Source Obsidian vault directory (default: ./obsidian-vault)')
    parser.add_argument('--output', default='./content/posts',
                        help='Output Hugo content directory (default: ./content/posts)')
    parser.add_argument('--config', default='scripts/config.yaml',
                        help='Configuration file path (default: scripts/config.yaml)')
    parser.add_argument('--watch', action='store_true',
                        help='Watch for changes and convert automatically')

    args = parser.parse_args()

    converter = ObsidianToHugoConverter(args.config)

    if args.watch:
        print("Watch mode not implemented yet. Coming soon!")
    else:
        converter.process_directory(args.source, args.output)
        print("\n✅ Conversion complete!")


if __name__ == "__main__":
    main()
