# Localhost Development Fix

## Problem
When running `hugo server`, clicking on blog posts or pagination links would redirect to `hri7hik-h4cks.com` instead of staying on `localhost:1313`.

## Root Cause
Hugo generates absolute URLs using the `baseURL` from `hugo.toml`:
- Production config: `baseURL = 'https://hri7hik-h4cks.com/'`
- This causes all links to point to the production domain

## Solution
Created a development configuration file (`config-development.toml`) that overrides the baseURL for local development:

### Files Created
1. **`config-development.toml`** - Development config with `baseURL = 'http://localhost:1313/'`

### Files Modified
1. **`scripts/workflow.sh`** - Updated to use dev config:
   ```bash
   hugo server --config hugo.toml,config-development.toml ...
   ```

## How to Use

### Start Development Server
```bash
./scripts/workflow.sh serve
```

### Visit Your Blog
Open browser to: **http://localhost:1313/posts/**

All links now correctly point to localhost!

## Production Build
For production builds, the script automatically uses `hugo.toml` (with the correct domain):
```bash
./scripts/workflow.sh build
```

This generates the production site with the correct domain URLs.

## Verification
Test that links work correctly:
```bash
# All URLs now use localhost in dev mode
curl -s http://localhost:1313/posts/ | grep -o 'href="[^"]*"' | grep "posts/"
```

Expected output:
- `href="http://localhost:1313/posts/hack-the-box-lame-walkthrough/"`
- `href="http://localhost:1313/posts/page/2/"`
- etc. (not `https://hri7hik-h4cks.com/...`)

## Summary
✅ **Problem**: Links redirected to production domain in dev mode
✅ **Solution**: Use dev config with localhost baseURL
✅ **Result**: All links now stay on localhost for development

---
*This ensures smooth local development without manually changing hugo.toml*
