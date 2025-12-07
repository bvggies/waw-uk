#!/usr/bin/env python3
"""
Update viewport meta tags in all HTML files for better mobile support
"""

import os
import re
from pathlib import Path

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
    'tickets/index.html',
    'components/header.html',
    'components/footer.html'
]

base_dir = Path(__file__).parent
viewport_new = '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">'

for html_file in html_files:
    file_path = base_dir / html_file
    
    if not file_path.exists():
        print(f"⚠ Skipping {html_file} (not found)")
        continue
    
    content = file_path.read_text(encoding='utf-8')
    original_content = content
    
    # Replace viewport meta tag
    content = re.sub(
        r'<meta\s+name=["\']viewport["\']\s+content=["\'][^"\']*["\']\s*>',
        viewport_new,
        content,
        flags=re.IGNORECASE
    )
    
    if content != original_content:
        file_path.write_text(content, encoding='utf-8')
        print(f"✓ Updated {html_file}")
    else:
        print(f"- No changes needed for {html_file}")

print("\n✅ Viewport meta tags updated across all files!")

