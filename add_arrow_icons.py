import re

# Read the speakers page
with open('speakers/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all View Profile links that don't have arrow icons yet
# Pattern: <a class="speaker-link"...>View Profile</a>
# Replace with: <a class="speaker-link"...>View Profile <i class="fas fa-arrow-right"></i></a>

# First, find all View Profile links without icons
pattern = r'(<a class="speaker-link"[^>]*>View Profile</a>)'
replacement = r'<a class="speaker-link"\1>View Profile <i class="fas fa-arrow-right"></i></a>'

# Actually, let's be more careful - match the full tag
pattern = r'(<a class="speaker-link"[^>]*>View Profile</a>)'
replacement = r'\1 <i class="fas fa-arrow-right"></i>'

# But we need to insert before </a>
pattern = r'(<a class="speaker-link"[^>]*>View Profile)(</a>)'
replacement = r'\1 <i class="fas fa-arrow-right"></i>\2'

content = re.sub(pattern, replacement, content)

# Write back
with open('speakers/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Added arrow icons to all View Profile links")

