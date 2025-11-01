# Obsidian to Hugo Blog Framework

A comprehensive automation framework for creating cybersecurity blogs at lightning speed using Obsidian for writing and Hugo for publishing.

## 🎯 Overview

This framework provides a complete workflow for:
- **Writing** blog posts in Obsidian with structured templates
- **Automatically converting** Obsidian markdown to Hugo-compatible format
- **Managing images** with automatic optimization and copying
- **Adding interactive features** like copy buttons on code blocks
- **Publishing** with one command

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install Python dependencies
pip3 install -r requirements.txt

# Make workflow script executable (already done)
chmod +x scripts/workflow.sh

# Setup directory structure
./scripts/workflow.sh setup
```

### 2. Create Your First Post

```bash
# Copy an Obsidian template
cp obsidian-templates/ctf-walkthrough.md obsidian-vault/posts/my-first-ctf.md

# Edit the file in Obsidian
# Then convert to Hugo format
./scripts/workflow.sh convert

# Preview your blog
./scripts/workflow.sh serve
```

Visit `http://localhost:1313` to see your blog!

## 📁 Framework Structure

```
obsidian-to-hugo-framework/
├── scripts/                          # Automation scripts
│   ├── obsidian_to_hugo_converter.py    # Main conversion engine
│   ├── config.yaml                     # Configuration file
│   └── workflow.sh                     # Automation workflow
│
├── obsidian-vault/                    # Your Obsidian vault (write here!)
│   ├── posts/                           # Your blog post markdown files
│   └── attachments/                     # Images and attachments
│
├── obsidian-templates/               # Template library
│   ├── ctf-walkthrough.md                # CTF writeup template
│   ├── tutorial.md                      # Tutorial template
│   ├── security-analysis.md             # Research/analysis template
│   └── quick-reference.md               # Quick reference template
│
├── layouts/shortcodes/              # Hugo shortcodes
│   ├── code.html                         # Enhanced code blocks
│   ├── terminal.html                     # Terminal blocks
│   ├── tool.html                         # Tool badges
│   ├── difficulty.html                   # Difficulty badges
│   ├── callout.html                      # Callout boxes
│   └── image.html                        # Image wrappers
│
├── assets/                          # Static assets
│   ├── css/
│   │   └── custom.css                     # Enhanced cybersecurity theme
│   └── js/
│       └── copy-buttons.js               # Copy button functionality
│
├── content/posts/                   # Generated Hugo content (auto-generated)
├── static/images/                   # Processed images (auto-generated)
└── docs/
    └── OBSIDIAN_TO_HUGO_FRAMEWORK.md    # This documentation
```

## 📝 Writing in Obsidian

### Creating a New Post

1. **Choose a template:**
   ```bash
   # For CTF writeups
   cp obsidian-templates/ctf-walkthrough.md obsidian-vault/posts/my-ctf-writeup.md

   # For tutorials
   cp obsidian-templates/tutorial.md obsidian-vault/posts/my-tutorial.md

   # For security analysis
   cp obsidian-templates/security-analysis.md obsidian-vault/posts/my-analysis.md
   ```

2. **Write in Obsidian:**
   - Open the file in Obsidian
   - Fill in the template placeholders (like `{{CTF Name}}`, `{{Target IP}}`, etc.)
   - Add images using Obsidian's image embedding: `![alt text](image.png)`
   - Create links between notes using `[[wikilinks]]`

### Obsidian-Specific Features

#### Wikilinks
Use Obsidian's double-bracket links: `[[Note Title]]`

The converter automatically converts these to Hugo-compatible links.

#### Callouts
Use Obsidian callout syntax:

```
> [!info] Information
> Your content here

> [!tip] Tip
> Helpful tip

> [!warning] Warning
> Important warning

> [!success] Success
> Success message
```

These convert to styled HTML callout boxes.

#### Code Blocks
Standard markdown code blocks:

```bash
nmap -sC -sV 10.10.10.10
```

Copy buttons are automatically added by the JavaScript!

#### Images
Embed images normally in Obsidian:

```
![Alt text](image.png)
```

Images are automatically:
- Copied to `static/images/`
- Optimized for web
- References updated

## 🎨 Interactive Features

### Copy Buttons
All code blocks automatically get copy buttons. Just hover over a code block to see them!

### Terminal Blocks
Use the terminal shortcode for better terminal styling:

```
{{< terminal command="nmap -sC -sV 10.10.10.10" >}}
nmap scan results here
{{< /terminal >}}
```

### Tool Badges
Highlight tools used:

```
{{< tool "nmap" >}} {{< tool "burp suite" >}} {{< tool "metasploit" >}}
```

### Difficulty Badges
Add difficulty indicators:

```
{{< difficulty level="beginner" label="Beginner Level" >}}

{{< difficulty level="intermediate" >}}

{{< difficulty level="advanced" label="Expert Level" >}}
```

### Callouts
Use Hugo shortcodes for enhanced callouts:

```
{{< callout type="info" title="Important Information" >}}
This is an important callout box with custom styling!
{{< /callout >}}

{{< callout type="warning" >}}
This is a warning without a custom title
{{< /callout >}}

{{< callout type="success" title="✅ Success!" >}}
You did it! This is a success message.
{{< /callout >}}

{{< callout type="danger" >}}
This is a danger callout
{{< /callout >}}

{{< callout type="tip" title="💡 Pro Tip" >}}
Here's a pro tip for you!
{{< /callout >}}

{{< callout type="example" title="📌 Example" >}}
This is an example callout
{{< /callout >}}

{{< callout type="question" title="❓ FAQ" >}}
This is a question callout
{{< /callout >}}

{{< callout type="abstract" title="📄 Summary" >}}
This is an abstract/summary callout
{{< /callout >}}

{{< callout type="note" title="📝 Note" >}}
This is a note callout
{{< /callout >}}
```

### Enhanced Code Blocks
Use the code shortcode for titled code blocks:

```
{{< code language="bash" title="Initial Port Scan" >}}
nmap -sC -sV 10.10.10.10
{{< /code >}}

{{< code language="python" title="Python Exploit" >}}
import socket
# Your exploit code here
{{< /code >}}

{{< code language="javascript" title="JavaScript Payload" >}}
// Your JS code here
{{< /code >}}

{{< code language="sql" title="SQL Injection Query" >}}
SELECT * FROM users WHERE id=1 OR 1=1;
{{< /code >}}

{{< code language="json" title="API Request JSON" >}}
{
  "key": "value",
  "number": 42
}
{{< /code >}}

{{< code language="html" title="HTML Template" >}}
<html>
  <body>Hello World</body>
</html>
{{< /code >}}

{{< code language="powershell" title="PowerShell Command" >}}
Get-Process | Where-Object {$_.CPU -gt 100}
{{< /code >}}

{{< code language="yaml" title="YAML Config" >}}
key: value
nested:
  key: value
{{< /code >}}

{{< code language="java" title="Java Code" >}}
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello World");
    }
}
{{< /code >}}

{{< code language="cpp" title="C++ Program" >}}
#include <iostream>
int main() {
    std::cout << "Hello World" << std::endl;
    return 0;
}
{{< /code >}}

{{< code language="csharp" title="C# Code" >}}
using System;

class Program {
    static void Main() {
        Console.WriteLine("Hello World");
    }
}
{{< /code >}}

{{< code language="php" title="PHP Script" >}}
<?php
echo "Hello World";
?>
{{< /code >}}

{{< code language="ruby" title="Ruby Script" >}}
puts "Hello World"
{{< /code >}}

{{< code language="go" title="Go Program" >}}
package main

import "fmt"

func main() {
    fmt.Println("Hello World")
}
{{< /code >}}

{{< code language="rust" title="Rust Program" >}}
fn main() {
    println!("Hello World");
}
{{< /code >}}

{{< code language="typescript" title="TypeScript Code" >}}
const message: string = "Hello World";
console.log(message);
{{< /code >}}

{{< code language="xml" title="XML Document" >}}
<?xml version="1.0"?>
<root>
  <element>value</element>
</root>
{{< /code >}}

{{< code language="css" title="CSS Styles" >}}
body {
    background-color: #000;
    color: #0f0;
}
{{< /code >}}

{{< code language="sh" title="Shell Script" >}}
#!/bin/bash
echo "Hello World"
{{< /code >}}

{{< code language="dockerfile" title="Dockerfile" >}}
FROM ubuntu:20.04
RUN echo "Hello World"
{{< /code >}}

{{< code language="nginx" title="Nginx Config" >}}
server {
    listen 80;
    server_name example.com;
    location / {
        root /var/www/html;
    }
}
{{< /code >}}

{{< code language="apache" title="Apache Config" >}}
<VirtualHost *:80>
    ServerName example.com
    DocumentRoot /var/www/html
</VirtualHost>
{{< /code >}}

{{< code language="regex" title="Regular Expression" >}}
^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$
{{< /code >}}

{{< code language="ini" title="INI File" >}}
[section]
key=value
key2=value2
{{< /code >}}

{{< code language="bat" title="Batch File" >}}
@echo off
echo Hello World
pause
{{< /code >}}

{{< code language="ps1" title="PowerShell Script" >}}
#Requires -Version 3.0

Write-Host "Hello World"
{{< /code >}}

{{< code language="swift" title="Swift Code" >}}
print("Hello World")
{{< /code >}}

{{< code language="kotlin" title="Kotlin Code" >}}
fun main() {
    println("Hello World")
}
{{< /code >}}

{{< code language="scala" title="Scala Code" >}}
object Main extends App {
  println("Hello World")
}
{{< /code >}}

{{< code language="r" title="R Script" >}}
print("Hello World")
{{< /code >}}

{{< code language="matlab" title="MATLAB Code" >}}
disp('Hello World')
{{< /code >}}

{{< code language="julia" title="Julia Code" >}}
println("Hello World")
{{< /code >}}

{{< code language="perl" title="Perl Script" >}}
print "Hello World\n";
{{< /code >}}

{{< code language="lua" title="Lua Script" >}}
print("Hello World")
{{< /code >}}

{{< code language="elixir" title="Elixir Module" >}}
IO.puts "Hello World"
{{< /code >}}

{{< code language="erlang" title="Erlang Module" >}}
-module(hello).
-export([world/0]).

world() ->
    io:format("Hello World~n").
{{< /code >}}

{{< code language="clojure" title="Clojure Code" >}}
(println "Hello World")
{{< /code >}}

{{< code language="fsharp" title="F# Script" >}}
printfn "Hello World"
{{< /code >}}

{{< code language="haskell" title="Haskell Program" >}}
main = putStrLn "Hello World"
{{< /code >}}

{{< code language="ocaml" title="OCaml Code" >}}
print_endline "Hello World"
{{< /code >}}

{{< code language="dart" title="Dart Code" >}}
void main() {
  print('Hello World');
}
{{< /code >}}

{{< code language="vim" title="Vim Script" >}}
:echo "Hello World"
{{< /code >}}

{{< code language="awk" title="AWK Script" >}}
BEGIN { print "Hello World" }
{{< /code >}}

{{< code language="sed" title="Sed Script" >}}
s/old/new/g
{{< /code >}}

{{< code language="makefile" title="Makefile" >}}
all:
    echo "Hello World"
{{< /code >}}

{{< code language="cmake" title="CMakeLists.txt" >}}
cmake_minimum_required(VERSION 3.0)
project(HelloWorld)
{{< /code >}}

{{< code language="objectivec" title="Objective-C Code" >}}
#import <Foundation/Foundation.h>

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        NSLog(@"Hello World");
    }
    return 0;
}
{{< /code >}}

{{< code language="kotlin" title="Kotlin Multiplatform" >}}
expect fun println(message: Any?)
{{< /code >}}

General markdown code blocks also work:

```bash
nmap -sC -sV 10.10.10.10
```

Both get automatic copy buttons!

### Enhanced Images

Use the image shortcode for advanced image features:

```
{{< image src="/images/screenshot.png" alt="Network Diagram" caption="Network topology showing target machine" width="80%" >}}
```

## 🔧 Configuration

Edit `scripts/config.yaml` to customize behavior:

```yaml
# Paths
obsidian_vault: "./obsidian-vault"
hugo_content: "./content/posts"
hugo_static: "./static/images"

# Image handling
auto_copy_images: true
optimize_images: true
image_max_width: 1200
image_quality: 85

# Front matter
default_categories: ["General"]
default_draft: false
generate_description: true

# Auto-extraction
auto_extract_tools: true
auto_extract_platforms: true
auto_extract_difficulty: true
```

## 🛠️ Available Commands

### Workflow Commands

```bash
# Setup initial environment
./scripts/workflow.sh setup

# Convert Obsidian notes to Hugo
./scripts/workflow.sh convert

# Start development server
./scripts/workflow.sh serve

# Watch for changes (auto-convert)
./scripts/workflow.sh watch

# Build for production
./scripts/workflow.sh build

# Clean generated content
./scripts/workflow.sh clean

# Check dependencies
./scripts/workflow.sh check
```

### Python Converter Commands

```bash
# Basic conversion
python3 scripts/obsidian_to_hugo_converter.py

# Specify custom paths
python3 scripts/obsidian_to_hugo_converter.py \
    --source ./my-obsidian-vault \
    --output ./content/posts

# Use custom config
python3 scripts/obsidian_to_hugo_converter.py \
    --config ./my-config.yaml
```

## 📚 Template Guide

### CTF Walkthrough Template

Best for detailed CTF writeups with:
- Structured sections (Recon, Initial Access, PrivEsc, Flag)
- Difficulty badges
- Tool highlighting
- Callouts for tips and warnings
- Comprehensive summary

**Placeholders:**
- `{{CTF Name}}` - Name of the CTF
- `{{Machine Name}}` - Target machine name
- `{{Platform Name}}` - HTB, TryHackMe, etc.
- `{{Difficulty Level}}` - beginner/intermediate/advanced
- `{{Target IP}}` - Target IP address

### Tutorial Template

For educational content:
- Step-by-step guides
- Prerequisites checklist
- Best practices sections
- Common mistakes
- Troubleshooting guide

**Placeholders:**
- `{{Tutorial Title}}` - Name of tutorial
- `{{Category}}` - Category (Networking, Web App Sec, etc.)
- `{{Difficulty Level}}` - Difficulty
- `{{Prerequisites}}` - What users should know
- `{{Time Estimate}}` - How long it takes

### Security Analysis Template

For research and analysis:
- Technical findings
- IoCs (Indicators of Compromise)
- Detection rules
- Timeline of events
- Recommendations

### Quick Reference Template

For cheat sheets and command references:
- Command syntax
- Quick tips
- Common pitfalls
- Useful resources

## 🎨 Customization

### Adding New Shortcodes

Create new shortcodes in `layouts/shortcodes/`:

```html
<!-- layouts/shortcodes/my-shortcode.html -->
<div class="my-custom-element">
  {{ .Inner }}
</div>
```

Use in markdown:
```
{{< my-shortcode >}}
Content here
{{< /my-shortcode >}}
```

### Customizing CSS

Edit `assets/css/custom.css` to:
- Change color scheme
- Modify component styles
- Add new CSS classes

### Adding New Taxonomies

Edit `hugo.toml` and add to templates:

```toml
[taxonomies]
  tag = "tags"
  category = "categories"
  difficulty = "difficulties"
  platform = "platforms"
  tool = "tools"
  your_custom = "your_custom_plural"
```

### Creating Custom Templates

Create new templates in `obsidian-templates/` following existing patterns.

## 🔍 Best Practices

### Writing Effective CTF Writeups

1. **Start with overview** - Target, difficulty, objectives
2. **Document everything** - All commands and outputs
3. **Explain your thinking** - Why you tried each approach
4. **Include failures** - What didn't work and why
5. **Add lessons learned** - Key takeaways
6. **Cite resources** - Links to tools and references

### Image Management

1. **Use descriptive filenames** - `nmap-scan-results.png` not `img1.png`
2. **Optimize before adding** - Keep images under 500KB if possible
3. **Add captions** - Explain what the image shows
4. **Reference in text** - Don't rely on images alone

### Code Examples

1. **Use appropriate language** - Enables syntax highlighting
2. **Add comments** - Explain what each section does
3. **Include expected output** - Show what users should see
4. **Test everything** - Ensure commands actually work

## 🐛 Troubleshooting

### Images Not Showing

**Problem:** Images appear broken in the generated blog

**Solution:**
1. Check image path in Obsidian note
2. Ensure image is in `attachments/` or same folder
3. Verify image file exists
4. Run converter again: `./scripts/workflow.sh convert`

### Conversion Errors

**Problem:** Python script fails during conversion

**Solution:**
1. Check Python dependencies: `pip3 install -r requirements.txt`
2. Validate YAML syntax in front matter
3. Check for special characters in filenames
4. Review error message for specific issue

### Hugo Build Errors

**Problem:** Hugo fails to build the site

**Solution:**
1. Check front matter syntax (use YAML, not JSON)
2. Verify all referenced images exist
3. Check for HTML syntax errors
4. Run `hugo --verbose` for detailed errors

### Copy Buttons Not Working

**Problem:** No copy buttons on code blocks

**Solution:**
1. Ensure `copy-buttons.js` is loaded (check page source)
2. Check browser console for JavaScript errors
3. Verify CSS has `.copy-button` styles
4. Clear browser cache and reload

## 📖 Hugo Features

### Table of Contents

Hugo automatically generates TOC from headings. Control with:

```yaml
showtoc: true  # In hugo.toml params
```

### Reading Time & Word Count

Automatically calculated and displayed:

```yaml
showReadingTime: true
showWordCount: true
```

### Taxonomies

Posts can be categorized with:

```yaml
categories: ["CTF", "HackTheBox"]
tags: ["network", "enumeration"]
difficulties: ["beginner"]
platforms: ["HackTheBox"]
tools: ["nmap", "netcat"]
```

### Draft Mode

Keep posts private while writing:

```yaml
draft: true  # Not published
draft: false # Published
```

## 🚀 Deployment

### Local Development

```bash
./scripts/workflow.sh serve
```

Then visit `http://localhost:1313`

### Build for Production

```bash
./scripts/workflow.sh build
```

Deploy the `public/` folder to:
- **Netlify** - Connect GitHub repo
- **Vercel** - Import Hugo project
- **GitHub Pages** - Use GitHub Actions
- **Traditional hosting** - Upload `public/` via FTP

### GitHub Actions Example

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy Hugo Site

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
        with:
          submodules: recursive

      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v2
        with:
          hugo-version: 'latest'

      - name: Setup Pages
        id: pages
        uses: actions/configure-pages@v2

      - name: Build with Hugo
        run: |
          hugo --gc --minify --baseURL "${{ steps.pages.outputs.base_url }}/"

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v1
        with:
          path: ./public
```

## 📝 Example Workflow

Here's a complete example of creating a new CTF writeup:

```bash
# 1. Copy template
cp obsidian-templates/ctf-walkthrough.md obsidian-vault/posts/hackthebox-meow.md

# 2. Edit in Obsidian
# - Replace {{CTF Name}} with "HackTheBox"
# - Replace {{Machine Name}} with "Meow"
# - Add content, images, code examples
# - Link to other notes with [[wikilinks]]

# 3. Convert to Hugo
./scripts/workflow.sh convert

# 4. Preview
./scripts/workflow.sh serve

# 5. Build when ready
./scripts/workflow.sh build
```

## 🎓 Learning Resources

### Obsidian Resources
- [Obsidian Official Documentation](https://help.obsidian.md/)
- [Obsidian Templates Guide](https://help.obsidian.md/Plugins/Templates)
- [Markdown Guide](https://www.markdownguide.org/)

### Hugo Resources
- [Hugo Documentation](https://gohugo.io/documentation/)
- [Hugo Shortcodes](https://gohugo.io/content-management/shortcodes/)
- [Hugo Themes](https://themes.gohugo.io/)

### Cybersecurity Resources
- [HackTheBox](https://www.hackthebox.eu/)
- [TryHackMe](https://tryhackme.com/)
- [OWASP](https://owasp.org/)
- [MITRE ATT&CK](https://attack.mitre.org/)

## 🤝 Contributing

To extend this framework:

1. **Add new shortcodes** - Create in `layouts/shortcodes/`
2. **Extend converter** - Modify `scripts/obsidian_to_hugo_converter.py`
3. **Create templates** - Add to `obsidian-templates/`
4. **Enhance styling** - Edit `assets/css/custom.css`

## 📄 License

This framework is provided as-is for educational and personal use.

## 🆘 Support

If you encounter issues:

1. Check this documentation
2. Review the troubleshooting section
3. Check GitHub issues
4. Create a new issue with:
   - Error messages
   - Configuration
   - Steps to reproduce
   - Expected vs actual behavior

## 🎉 Credits

Created for fast cybersecurity blog generation using:
- **Obsidian** - Note-taking and writing
- **Hugo** - Static site generation
- **PaperMod** - Hugo theme
- **Python** - Automation scripts

---

**Happy Blogging! 🚀**

For more information, visit the project repository or check the inline code comments.
