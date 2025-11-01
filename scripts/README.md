# Automation Scripts

This directory contains automation scripts for the Obsidian to Hugo blog framework.

## Files

### `obsidian_to_hugo_converter.py`
Main Python script that converts Obsidian-flavored markdown to Hugo-compatible format.

**Features:**
- Converts [[wikilinks]] to standard markdown links
- Transforms Obsidian callouts to HTML callout boxes
- Automatically copies and optimizes images
- Generates front matter from filename and content
- Extracts metadata (tools, platforms, difficulty)

**Usage:**
```bash
python3 obsidian_to_hugo_converter.py
python3 obsidian_to_hugo_converter.py --source ./my-vault --output ./content
python3 obsidian_to_hugo_converter.py --config ./custom-config.yaml
```

### `workflow.sh`
Bash script that orchestrates the entire workflow.

**Usage:**
```bash
./workflow.sh setup       # Setup directories and dependencies
./workflow.sh convert     # Convert Obsidian notes to Hugo
./workflow.sh serve       # Start Hugo development server
./workflow.sh watch       # Watch for changes and auto-convert
./workflow.sh build       # Build site for production
./workflow.sh clean       # Remove generated content
./workflow.sh check       # Check dependencies
```

### `config.yaml`
Configuration file for the converter.

**Settings:**
- Source and destination paths
- Image handling options
- Front matter generation settings
- Auto-extraction preferences

## Dependencies

Install Python dependencies:
```bash
pip3 install -r requirements.txt
```

Required packages:
- `pyyaml` - YAML parsing
- `python-frontmatter` - Front matter handling
- `Pillow` - Image processing

## Quick Start

```bash
# Setup
./workflow.sh setup

# Convert notes
./workflow.sh convert

# Preview
./workflow.sh serve
```

See the full documentation in `../docs/OBSIDIAN_TO_HUGO_FRAMEWORK.md` for detailed usage instructions.
