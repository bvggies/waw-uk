import json
import re

def convert_google_drive_url(url):
    """Convert Google Drive sharing link to direct image URL with multiple fallback formats"""
    if not url or not url.strip():
        return ""
    
    # Extract file ID from various Google Drive URL formats
    patterns = [
        r'id=([a-zA-Z0-9_-]+)',
        r'/d/([a-zA-Z0-9_-]+)',
        r'/file/d/([a-zA-Z0-9_-]+)',
    ]
    
    file_id = None
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            file_id = match.group(1)
            break
    
    if file_id:
        # Try multiple formats - Google Drive thumbnail API is more reliable
        # Format 1: Thumbnail API (most reliable for images)
        return f"https://drive.google.com/thumbnail?id={file_id}&sz=w800"
        # Alternative formats if needed:
        # return f"https://drive.google.com/uc?export=download&id={file_id}"
        # return f"https://lh3.googleusercontent.com/d/{file_id}"
    
    return url

# Load speakers data
with open('assets/speakers.json', 'r', encoding='utf-8') as f:
    speakers = json.load(f)

# Update picture URLs
for speaker in speakers:
    if speaker.get('picture'):
        speaker['picture'] = convert_google_drive_url(speaker['picture'])

# Save updated data
with open('assets/speakers.json', 'w', encoding='utf-8') as f:
    json.dump(speakers, f, indent=2, ensure_ascii=False)

print(f"Updated {len(speakers)} speaker image URLs")

# Now regenerate the HTML files
import html

def escape_html(text):
    """Escape HTML special characters"""
    if not text:
        return ""
    return html.escape(str(text))

def generate_speaker_card(speaker, index):
    """Generate HTML for a single speaker card"""
    name = escape_html(speaker['name'])
    org = escape_html(speaker['org'])
    linkedin = speaker['linkedin']
    picture = speaker['picture']
    
    # Default placeholder if no picture
    if not picture:
        picture = "https://via.placeholder.com/400x400?text=Speaker"
    
    linkedin_html = ""
    if linkedin:
        linkedin_html = f'<a href="{escape_html(linkedin)}" target="_blank" rel="noopener" class="speaker-linkedin" aria-label="{name} LinkedIn Profile"><i class="fab fa-linkedin"></i></a>'
    
    org_html = f'<p class="speaker-org">{org}</p>' if org else ''
    
    # Don't escape URLs in style attributes and href
    picture_url = picture.replace("'", "\\'") if picture else "https://via.placeholder.com/400x400?text=Speaker"
    linkedin_url = linkedin if linkedin else "#"
    link_attrs = 'target="_blank" rel="noopener"' if linkedin else ''
    
    return f'''                                    <div class="vc_col-sm-3">
                                        <div class="team-member" data-style="meta_overlaid">
                                            <div class="team-member-overlay"></div>
                                            <a href="{linkedin_url}" {link_attrs}></a>
                                            <div class="team-member-image" style="background-image: url('{picture_url}');"></div>
                                            <div class="team-meta">
                                                <h3>{name}</h3>
                                                {org_html}
                                                {linkedin_html}
                                            </div>
                                        </div>
                                    </div>'''

# Generate homepage speakers section (first 8 speakers)
homepage_speakers = speakers[:8]
homepage_html = "\n".join([generate_speaker_card(speaker, i) for i, speaker in enumerate(homepage_speakers)])

# Generate full speakers page HTML (all speakers)
all_speakers_html = "\n".join([generate_speaker_card(speaker, i) for i, speaker in enumerate(speakers)])

# Save to files
with open('assets/homepage_speakers.html', 'w', encoding='utf-8') as f:
    f.write(homepage_html)

with open('assets/all_speakers.html', 'w', encoding='utf-8') as f:
    f.write(all_speakers_html)

print(f"Generated HTML for {len(homepage_speakers)} homepage speakers")
print(f"Generated HTML for {len(speakers)} speakers page")
print("Files saved: assets/homepage_speakers.html and assets/all_speakers.html")

