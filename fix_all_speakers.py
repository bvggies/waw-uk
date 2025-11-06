import csv
import re
import json
import html

def convert_google_drive_url(url):
    """Convert Google Drive URL to thumbnail format"""
    if not url or not url.strip():
        return ""
    
    url = url.strip()
    
    # Extract file ID from various Google Drive URL formats
    patterns = [
        r'id=([a-zA-Z0-9_-]+)',
        r'/d/([a-zA-Z0-9_-]+)',
        r'/file/d/([a-zA-Z0-9_-]+)',
        r'/open\?id=([a-zA-Z0-9_-]+)',
    ]
    
    file_id = None
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            file_id = match.group(1)
            break
    
    if file_id:
        # Use thumbnail API for better compatibility
        return f"https://drive.google.com/thumbnail?id={file_id}&sz=w800"
    
    return url

def normalize_linkedin_url(url):
    """Normalize LinkedIn URL"""
    if not url or not url.strip():
        return ""
    
    url = url.strip()
    
    # Skip if it's not a LinkedIn URL
    if 'linkedin.com' not in url.lower() and not url.startswith('www.') and not url.startswith('http'):
        return ""
    
    # Fix double protocol (e.g., https://Https://)
    url = re.sub(r'^https?://[Hh]ttps?://', 'https://', url)
    url = re.sub(r'^[Hh]ttps?://', 'https://', url)
    
    # Add protocol if missing
    if not url.startswith('http'):
        url = 'https://' + url.lstrip('/')
    
    # Ensure it's a proper LinkedIn URL
    if 'linkedin.com' not in url.lower():
        return ""
    
    return url

def escape_html(text):
    """Escape HTML special characters"""
    if not text:
        return ""
    return html.escape(str(text))

def generate_speaker_card(speaker):
    """Generate HTML for a single speaker card with fixed rounded rectangle image"""
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
    
    linkedin_url = linkedin if linkedin else "#"
    link_attrs = 'target="_blank" rel="noopener"' if linkedin else ''
    
    # Use img tag with fixed rounded rectangle styling
    return f'''                                    <div class="vc_col-sm-3">
                                        <div class="team-member" data-style="meta_overlaid">
                                            <div class="team-member-overlay"></div>
                                            <a href="{linkedin_url}" {link_attrs}></a>
                                            <div class="team-member-image">
                                                <img src="{picture}" alt="{name}" loading="lazy" onerror="this.style.display='none'; this.parentElement.classList.add('image-error');" />
                                            </div>
                                            <div class="team-meta">
                                                <h3>{name}</h3>
                                                {org_html}
                                                {linkedin_html}
                                            </div>
                                        </div>
                                    </div>'''

# Parse TSV file
speakers_data = []
with open('assets/speakers.tsv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter='\t')
    
    for row in reader:
        # Handle duplicate "Name" columns - use the 4th column (index 3) which is the actual name
        # The first "Name" column seems to be a different field
        name = row.get('Name', '').strip()
        
        # Skip header row or empty rows
        if not name or name == 'Name' or name == 'Email':
            continue
        
        # Get organization - check both possible column names
        org = row.get('Organisation/Institution', '').strip()
        if not org:
            org = row.get('Organisation', '').strip()
        
        # Get LinkedIn profile
        linkedin = normalize_linkedin_url(row.get('LinkedIn Profile', '').strip())
        
        # Get picture URL and convert it
        picture_url = row.get('Picture', '').strip()
        picture = convert_google_drive_url(picture_url)
        
        speakers_data.append({
            'name': name,
            'org': org,
            'linkedin': linkedin,
            'picture': picture
        })

# Save to JSON
with open('assets/speakers.json', 'w', encoding='utf-8') as f:
    json.dump(speakers_data, f, indent=2, ensure_ascii=False)

print(f"Processed {len(speakers_data)} speakers from TSV")

# Generate homepage speakers section (first 8 speakers)
homepage_speakers = speakers_data[:8]
homepage_html = "\n".join([generate_speaker_card(speaker) for speaker in homepage_speakers])

# Generate full speakers page HTML (all speakers)
all_speakers_html = "\n".join([generate_speaker_card(speaker) for speaker in speakers_data])

# Save to files
with open('assets/homepage_speakers.html', 'w', encoding='utf-8') as f:
    f.write(homepage_html)

with open('assets/all_speakers.html', 'w', encoding='utf-8') as f:
    f.write(all_speakers_html)

print(f"Generated HTML for {len(homepage_speakers)} homepage speakers")
print(f"Generated HTML for {len(speakers_data)} speakers page")

# Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    index_content = f.read()

# Find and replace homepage speakers section
homepage_start = index_content.find('<div class="speakers-grid">')
if homepage_start != -1:
    homepage_end = index_content.find('</div>', homepage_start + len('<div class="speakers-grid">'))
    if homepage_end != -1:
        # Find the closing </div> for speakers-grid
        # We need to find where the speakers-grid div ends
        # Count opening and closing divs to find the right closing tag
        div_count = 1
        search_pos = homepage_start + len('<div class="speakers-grid">')
        while div_count > 0 and search_pos < len(index_content):
            if index_content[search_pos:search_pos+4] == '<div':
                div_count += 1
            elif index_content[search_pos:search_pos+5] == '</div':
                div_count -= 1
            search_pos += 1
        
        if div_count == 0:
            homepage_end = search_pos - 1
            # Find the actual </div> tag
            actual_end = index_content.find('</div>', homepage_start + len('<div class="speakers-grid">'))
            if actual_end != -1:
                # Replace everything between opening and closing tags
                index_content = index_content[:homepage_start + len('<div class="speakers-grid">')] + '\n' + homepage_html + '\n' + index_content[actual_end:]
                with open('index.html', 'w', encoding='utf-8') as f:
                    f.write(index_content)
                print("Updated index.html with homepage speakers")
            else:
                print("Could not find closing tag for homepage speakers grid")
        else:
            print("Could not properly parse homepage speakers grid structure")
    else:
        print("Could not find end of homepage speakers grid")
else:
    print("Could not find homepage speakers grid in index.html")

# Update speakers/index.html
with open('speakers/index.html', 'r', encoding='utf-8') as f:
    speakers_page_content = f.read()

speakers_start = speakers_page_content.find('<div class="speakers-grid">')
if speakers_start != -1:
    speakers_end = speakers_page_content.find('</div>', speakers_start + len('<div class="speakers-grid">'))
    if speakers_end != -1:
        # Similar logic to find the correct closing tag
        speakers_page_content = speakers_page_content[:speakers_start + len('<div class="speakers-grid">')] + '\n' + all_speakers_html + '\n' + speakers_page_content[speakers_end:]
        with open('speakers/index.html', 'w', encoding='utf-8') as f:
            f.write(speakers_page_content)
        print("Updated speakers/index.html with all speakers")
    else:
        print("Could not find end of speakers grid in speakers/index.html")
else:
    print("Could not find speakers grid in speakers/index.html")

print("\nAll speakers processed and HTML files updated!")
print(f"Total speakers: {len(speakers_data)}")

