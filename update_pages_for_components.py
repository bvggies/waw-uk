#!/usr/bin/env python3
"""
Script to update all HTML pages to use shared header and footer components
"""
import os
import re

# Pages to update (relative to root)
pages = [
    'about-us/index.html',
    'contact-us/index.html',
    'speakers/index.html',
    'our-sponsors/index.html',
    'exhibition/index.html',
    'tickets/index.html',
    'pre-register/index.html',
    'events/index.html',
    'privacy-policy/index.html',
    'terms-conditions/index.html',
]

# Header pattern - matches from <header to </header>
header_pattern = re.compile(
    r'<header[^>]*>.*?</header>',
    re.DOTALL
)

# Footer pattern - matches from <footer to </footer> including script tags before closing body
footer_pattern = re.compile(
    r'<footer[^>]*>.*?</footer>\s*<script[^>]*src=["\'][^"\']*script\.js["\'][^>]*></script>',
    re.DOTALL
)

header_replacement = '''    <!-- Header Placeholder - Loaded from components/header.html -->
    <div id="header-placeholder"></div>'''

footer_replacement = '''    <!-- Footer Placeholder - Loaded from components/footer.html -->
    <div id="footer-placeholder"></div>

    <script src="../components/load-components.js"></script>
    <script src="../script.js"></script>'''

for page_path in pages:
    if not os.path.exists(page_path):
        print(f"Skipping {page_path} - file not found")
        continue
    
    with open(page_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace header
    content = header_pattern.sub(header_replacement, content)
    
    # Replace footer
    content = footer_pattern.sub(footer_replacement, content)
    
    with open(page_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated {page_path}")

print("Done!")

