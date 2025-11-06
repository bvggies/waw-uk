import re

# Read the generated speakers HTML with updated URLs
with open('assets/all_speakers.html', 'r', encoding='utf-8') as f:
    speakers_html = f.read()

# Read the speakers page
with open('speakers/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the speakers grid section
# Look for the opening tag and replace everything until the closing tags
pattern = r'(<div class="speakers-grid">).*?(</div>\s*</div>\s*</div>\s*</div>\s*</div>\s*</div>)'
replacement = r'\1\n' + speakers_html + r'\n                                </div>\n                            </div>\n                        </div>\n                    </div>\n                </div>'

content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Write back
with open('speakers/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated speakers page with corrected image URLs')

