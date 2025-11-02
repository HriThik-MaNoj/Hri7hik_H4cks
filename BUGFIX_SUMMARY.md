# Bug Fixes Summary

## Issues Fixed

This document summarizes the two major issues identified and fixed in the Hugo blog codebase.

---

## Issue #1: Localhost URLs Not Used in Development

### Problem
When running `hugo server` directly, the site would use production URLs (`https://hri7hik-h4cks.com/`) instead of localhost URLs, causing broken links during development.

### Root Cause
- The main `hugo.toml` has `baseURL = 'https://hri7hik-h4cks.com/'`
- A separate `config-development.toml` exists with `baseURL = 'http://localhost:1313/'`
- Users were running `hugo server` without specifying the development config

### Solution
**Updated `/scripts/workflow.sh`:**

1. Modified `serve_site()` function to always use both configs:
   ```bash
   hugo server --config hugo.toml,config-development.toml ...
   ```

2. Added `--buildFuture` flag to include all posts during development

### Best Practice
**Always use the workflow script for development:**
```bash
./scripts/workflow.sh serve    # ✅ Uses localhost URLs
./scripts/workflow.sh build    # ✅ Builds for production

# NOT:
hugo server                    # ❌ Uses production URLs
```

---

## Issue #2: Some Posts Not Visible in Posts Section

### Problem
Five posts were not appearing in the `/posts/` listing page, though they were accessible via direct links:
- hack-the-box-lame-walkthrough
- log4j-vulnerability-analysis-cve-2021-44228
- nmap-command-reference-cheat-sheet
- sql-injection-basics-and-prevention
- web-application-security-testing-burp-suite

### Root Causes

#### Primary Cause: Future-Dated Posts
- Posts had dates in the future relative to build time
- Hugo excludes future-dated posts by default
- Current time: `11:10 AM IST, Nov 2, 2025`
- Post date: `10:28 AM, Nov 2, 2025` (future)

#### Secondary Cause: YAML Front Matter Format
- Obsidian converter was generating malformed YAML:
  ```yaml
  categories:
  - General        # ❌ Block style with dash
  ```
- Should be inline array format:
  ```yaml
  categories: ["General"]    # ✅ Inline array
  ```

### Solution

#### 1. Fixed Obsidian Converter (`/scripts/obsidian_to_hugo_converter.py`)
Updated `write_converted_file()` method to manually format YAML:

```python
def write_converted_file(self, output_path: Path, content: str, front_matter: Dict) -> None:
    # Manually format front matter for Hugo compatibility
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
```

This ensures clean, Hugo-compatible YAML:
```yaml
---
title: "Hack The Box Lame Walkthrough"
date: "2025-11-02T10:28:39"
draft: false
categories: ["General"]
platforms: ["hackthebox"]
tools: ["cmd", "nmap", "bash", "ssh", "metasploit"]
description: " Hack The Box - Lame Walkthrough"
---
```

#### 2. Updated Workflow Script (`/scripts/workflow.sh`)
Added `--buildFuture` flag to both `serve_site()` and `build_site()` functions:

```bash
# Before
hugo server --config hugo.toml,config-development.toml --buildDrafts --buildExpired
hugo --minify --buildExpired

# After
hugo server --config hugo.toml,config-development.toml --buildDrafts --buildExpired --buildFuture
hugo --minify --buildExpired --buildFuture
```

### Verification

**Before Fix:**
```
Pages            │ 106
Posts built      │ 8
Missing posts    │ 5
```

**After Fix:**
```
Pages            │ 139  ✅ (+33 pages)
Posts built      │ 13   ✅ (+5 posts)
All posts visible│ YES  ✅
```

---

## Files Modified

1. **`/scripts/workflow.sh`**
   - Added `--buildFuture` flag to serve_site()
   - Added `--buildFuture` flag to build_site()
   - Added informational messages about localhost URLs

2. **`/scripts/obsidian_to_hugo_converter.py`**
   - Rewrote `write_converted_file()` method
   - Manual YAML formatting for Hugo compatibility
   - Inline array syntax for lists
   - Proper boolean and string formatting

---

## Testing Results

### Test 1: Build with Workflow Script
```bash
./scripts/workflow.sh build
```
✅ **Result:** All 13 posts built successfully

### Test 2: Check Posts Listing
```bash
ls -1 public/posts/ | grep -v "index.html\|index.xml\|page"
```
✅ **Result:** All posts visible including:
- hack-the-box-lame-walkthrough
- log4j-vulnerability-analysis-cve-2021-44228
- nmap-command-reference-cheat-sheet
- sql-injection-basics-and-prevention
- web-application-security-testing-burp-suite

### Test 3: Verify Localhost URLs
```bash
grep -o 'http://localhost:1313' public/posts/index.html | head -1
```
✅ **Result:** `http://localhost:1313` ✅

---

## Recommendations

### For Developers
1. **Always use the workflow script:**
   - `./scripts/workflow.sh serve` for development
   - `./scripts/workflow.sh build` for production

2. **Avoid running Hugo commands directly** unless you know what you're doing

3. **Check post dates** when creating new posts - ensure they're not in the future

### For Content Creation
The Obsidian converter now automatically generates proper YAML front matter. When writing in Obsidian:
- No special front matter syntax needed
- Converter extracts metadata automatically
- Tools, platforms, and difficulty are auto-detected from content
- Dates are set from file modification time

---

## Summary

Both issues have been completely resolved:

1. ✅ **Localhost URLs:** Workflow script now automatically uses development config
2. ✅ **Missing Posts:** Future date flag + YAML formatting fixes

The blog now correctly:
- Displays all posts in the `/posts/` section
- Uses localhost URLs during development
- Builds 139 pages (13 posts + taxonomies + other pages)
- Generates clean, Hugo-compatible YAML front matter
