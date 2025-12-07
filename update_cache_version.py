#!/usr/bin/env python3
"""
Cache Version Updater
Updates version numbers in all HTML files to force browser cache refresh
Usage: python update_cache_version.py [version_number]
"""

import os
import re
import sys
from pathlib import Path

# Get new version from command line or use default
new_version = sys.argv[1] if len(sys.argv) > 1 else '1.0.1'

# Update version.js
version_js_path = Path(__file__).parent / 'version.js'
version_js_content = f"""// Version number - Update this whenever you make changes to force cache refresh
window.SITE_VERSION = '{new_version}';
"""
version_js_path.write_text(version_js_content, encoding='utf-8')
print(f"✓ Updated version.js to {new_version}")

# HTML files to update
html_files = [
    'index.html',
    'about-us/index.html',
    'exhibition/index.html',
    'experience/index.html',
    'faq/index.html',
    'media/index.html',
    'our-sponsors/index.html',
    'speakers/index.html',
    'travel-info/index.html',
    'contact-us/index.html',
    'terms-conditions/index.html',
    'privacy-policy/index.html',
    'events/index.html',
    'pre-register/index.html',
    'tickets/index.html'
]

base_dir = Path(__file__).parent

for html_file in html_files:
    file_path = base_dir / html_file
    
    if not file_path.exists():
        print(f"⚠ Skipping {html_file} (not found)")
        continue
    
    content = file_path.read_text(encoding='utf-8')
    original_content = content
    updated = False
    
    # Determine if it's root or subdirectory
    is_root = html_file == 'index.html'
    version_path = 'version.js' if is_root else '../version.js'
    css_path_prefix = '' if is_root else '../'
    js_path_prefix = '' if is_root else '../'
    
    # Add cache-control meta tags if not present
    if 'Cache-Control' not in content:
        content = re.sub(
            r'(<meta name="theme-color"[^>]*>)',
            r'''<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    \1''',
            content,
            count=1
        )
        updated = True
    
    # Add version.js script if not present
    if 'version.js' not in content:
        content = re.sub(
            r'(<title>[^<]+</title>)',
            f'\\1\n    <script src="{version_path}?v={new_version}"></script>',
            content,
            count=1
        )
        updated = True
    
    # Update CSS file versions
    content = re.sub(
        r'href=["\']([^"\']*\.css)(\?v=[\d.]+)?["\']',
        lambda m: f'href="{m.group(1)}?v={new_version}"' if not m.group(1).startswith('http') else m.group(0),
        content
    )
    
    # Update JS file versions (except version.js which is handled separately)
    content = re.sub(
        r'src=["\']([^"\']*\.js)(\?v=[\d.]+)?["\']',
        lambda m: f'src="{m.group(1)}?v={new_version}"' if 'version.js' not in m.group(1) and not m.group(1).startswith('http') else m.group(0),
        content
    )
    
    # Update version.js specifically
    content = re.sub(
        r'src=["\']([^"\']*version\.js)(\?v=[\d.]+)?["\']',
        f'src="\\1?v={new_version}"',
        content
    )
    
    if content != original_content:
        file_path.write_text(content, encoding='utf-8')
        print(f"✓ Updated {html_file}")
        updated = True
    
    if not updated:
        print(f"- No changes needed for {html_file}")

print(f"\n✅ Cache version updated to {new_version} across all files!")
print(f"\nTo force browsers to reload, users can:")
print(f"1. Hard refresh: Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)")
print(f"2. Clear browser cache")
print(f"3. Open in incognito/private mode")

