import json
import html
import re

def escape_html(text):
    """Escape HTML special characters"""
    if not text:
        return ""
    return html.escape(str(text))

def generate_speaker_card(speaker):
    """Generate HTML for a single speaker card matching WiFAI style"""
    name = escape_html(speaker['name'])
    org = escape_html(speaker['org'])
    linkedin = speaker['linkedin']
    picture = speaker['picture']
    
    # Default placeholder if no picture
    if not picture:
        picture = "https://via.placeholder.com/400x400?text=Speaker"
    
    # LinkedIn link or placeholder
    linkedin_url = linkedin if linkedin else "#"
    link_attrs = 'target="_blank" rel="noopener"' if linkedin else ''
    
    org_html = f'<p class="speaker-title">{org}</p>' if org else ''
    
    return f'''                                    <div class="speaker-card">
                                        <div class="speaker-image-wrapper">
                                            <img src="{picture}" alt="{name}" class="speaker-image" loading="lazy" onerror="this.style.display='none'; this.parentElement.classList.add('image-error');" />
                                        </div>
                                        <div class="speaker-info">
                                            <h3 class="speaker-name">{name}</h3>
                                            {org_html}
                                            <a href="{linkedin_url}" {link_attrs} class="speaker-profile-link">
                                                <span>View Profile</span>
                                                <i class="fas fa-arrow-right"></i>
                                            </a>
                                        </div>
                                    </div>'''

# Load speakers data
with open('assets/speakers.json', 'r', encoding='utf-8') as f:
    speakers = json.load(f)

# Generate all speakers HTML
all_speakers_html = "\n".join([generate_speaker_card(speaker) for speaker in speakers])

# Update speakers/index.html
with open('speakers/index.html', 'r', encoding='utf-8') as f:
    speakers_page_content = f.read()

# Find and replace the speakers grid content
speakers_start = speakers_page_content.find('<div class="speakers-grid-new">')
if speakers_start != -1:
    # Find the closing tag for speakers-grid-new
    # We need to find where this div ends - it should be before the closing </div> of wpb_wrapper
    # Let's find the next </div> that closes speakers-grid-new
    search_pos = speakers_start + len('<div class="speakers-grid-new">')
    
    # Count divs to find the matching closing tag
    div_count = 1
    while div_count > 0 and search_pos < len(speakers_page_content):
        if search_pos + 4 <= len(speakers_page_content) and speakers_page_content[search_pos:search_pos+4] == '<div':
            div_count += 1
        elif search_pos + 5 <= len(speakers_page_content) and speakers_page_content[search_pos:search_pos+5] == '</div':
            div_count -= 1
        search_pos += 1
    
    if div_count == 0:
        speakers_end = search_pos - 1
        # Find the actual </div> tag position
        actual_end = speakers_page_content.rfind('</div>', speakers_start, speakers_end + 10)
        if actual_end != -1:
            # Replace everything between opening and closing tags
            speakers_page_content = speakers_page_content[:speakers_start + len('<div class="speakers-grid-new">')] + '\n' + all_speakers_html + '\n                                ' + speakers_page_content[actual_end:]
            with open('speakers/index.html', 'w', encoding='utf-8') as f:
                f.write(speakers_page_content)
            print("Updated speakers/index.html with WiFAI-style layout")
        else:
            print("Could not find closing tag for speakers-grid-new")
    else:
        print("Could not properly parse speakers-grid-new structure")
else:
    print("Could not find speakers-grid-new in speakers/index.html")

print(f"Generated HTML for {len(speakers)} speakers with WiFAI-style layout")

