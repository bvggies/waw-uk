import json
import html

def escape_html(text):
    """Escape HTML special characters"""
    if not text:
        return ""
    return html.escape(str(text))

def generate_speaker_card(speaker):
    """Generate HTML for a single speaker card matching WiFAI style"""
    name = escape_html(speaker['name'])
    org = escape_html(speaker['org'])
    title = escape_html(speaker.get('title', ''))
    linkedin = speaker['linkedin']
    picture = speaker['picture']
    
    # Default placeholder if no picture
    if not picture:
        picture = "https://via.placeholder.com/400x400?text=Speaker"
    
    # LinkedIn link or placeholder
    linkedin_url = linkedin if linkedin else "#"
    link_attrs = 'target="_blank" rel="noopener"' if linkedin else ''
    
    # Display both organization and title (matching WiFAI format)
    org_html = ''
    if org:
        org_html = f'<p class="speaker-org">{org}</p>'
    if title:
        title_html = f'<p class="speaker-title">{title}</p>'
        org_html = org_html + title_html if org_html else title_html
    
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

# Speakers from WiFAI website (as listed on the page)
wifai_speakers = [
    {"name": "Tambra Raye Stevenson", "org": "Women Advancing Nutrition Dietetics and Agriculture", "title": "Founder"},
    {"name": "Antoinette Sallah", "org": "Solirag X", "title": "C.E.O"},
    {"name": "Layla", "org": "Iddyba Foundation", "title": "Founder"},
    {"name": "VERONICA ANNOR", "org": "CAPGEMINI", "title": "Consultant"},
    {"name": "Miracle Opeyemi Ogunbowale", "org": "El'mira Consults.", "title": "Founder"},
    {"name": "Ayeni-Wuraola Ogungbola", "org": "Nutrifield Foods", "title": "C.E.O"},
    {"name": "Constanza I. Robles Fumarola", "org": "Inanna", "title": "Founding Member"},
    {"name": "Janet Mulu ITS", "org": "ImpactDev Africa", "title": "Trade Specialist"},
    {"name": "Samara Dias", "org": "Ella Africa Foundation", "title": "C.E.O"},
    {"name": "Gloria Dalafu", "org": "School2u virtual academy", "title": "Founder"},
    {"name": "Omu Obilor", "org": "Ómu Consulting Limited", "title": "C.E.O"},
    {"name": "Ilona Karpanos", "org": "Cambridgeshire Chamber of Commerce", "title": "Manager"},
    {"name": "Abeni Ramsey", "org": "CITY Girl farms", "title": "Founder"},
    {"name": "Vivian Maduekeh", "org": "Food Health Systems Advisory", "title": "Managing Partner"},
    {"name": "Fatimah Bamisedun", "org": "Anre Solutions", "title": "Director"},
    {"name": "Deretho Francis ZIGBE", "org": "Starz Risk Solutions", "title": "Founder & CEO"},
    {"name": "Anna Jones", "org": "Just Farmers", "title": "Founder"},
    {"name": "D. Spence", "org": "YAHMAPP LTD", "title": "C.E.O"},
    {"name": "Anne Nicholls", "org": "Mimi Pia: Period CIC", "title": "C.E.O"},
    {"name": "SMG", "org": "SenBritish Group", "title": "Founder"},
    {"name": "Sandrine Henton", "org": "EG Capital", "title": "C.E.O"},
    {"name": "Ozlem Bacak", "org": "Luviland Ltd", "title": "Entrepreneur"},
    {"name": "Prama Bhardwaj", "org": "Mantis World & Gerana Initiative", "title": "C.E.O"},
    {"name": "Evelyn Alice Lucy Tuhairwe Karokora", "org": "Tesifa Sustainable Farm", "title": "Founder"},
    {"name": "Lucy Antwi-Boateng", "org": "Farrer & Co LLP", "title": "Project Manager"},
    {"name": "Michaelle Kubwimana", "org": "Kawah Coffee Ltd", "title": "C.E.O"},
    {"name": "Dolapo Enejoh", "org": "Food system and nutrition advisor", "title": "C.E.O"},
    {"name": "Johnson Bada", "org": "Go-Geeper Limited", "title": "C.E.O"},
]

# Load existing speakers data to match images and LinkedIn
with open('assets/speakers.json', 'r', encoding='utf-8') as f:
    existing_speakers = json.load(f)

# Create a lookup dictionary by name (case-insensitive)
speakers_lookup = {}
for speaker in existing_speakers:
    name_key = speaker['name'].lower().strip()
    speakers_lookup[name_key] = speaker

# Match WiFAI speakers with existing data
matched_speakers = []
for wifai_speaker in wifai_speakers:
    name = wifai_speaker['name']
    name_key = name.lower().strip()
    
    # Try to find matching speaker in existing data
    matched = None
    if name_key in speakers_lookup:
        matched = speakers_lookup[name_key]
    else:
        # Try partial matching for names with variations
        # Handle cases like "D. Spence" vs "d.spence", "VERONICA ANNOR" vs "Veronica Annor"
        for key, existing in speakers_lookup.items():
            # Normalize both names for comparison (remove dots, extra spaces, case)
            normalized_key = key.replace('.', '').replace(' ', '').lower()
            normalized_name = name_key.replace('.', '').replace(' ', '').lower()
            if normalized_name == normalized_key or name_key in key or key in name_key:
                matched = existing
                break
    
    # Create speaker object with WiFAI data but existing image/LinkedIn if available
    speaker_data = {
        'name': wifai_speaker['name'],
        'org': wifai_speaker['org'],
        'title': wifai_speaker['title'],
        'linkedin': matched['linkedin'] if matched else '',
        'picture': matched['picture'] if matched else ''
    }
    matched_speakers.append(speaker_data)

# Generate all speakers HTML
all_speakers_html = "\n".join([generate_speaker_card(speaker) for speaker in matched_speakers])

# Update speakers/index.html
with open('speakers/index.html', 'r', encoding='utf-8') as f:
    speakers_page_content = f.read()

# Find and replace the speakers grid content
speakers_start = speakers_page_content.find('<div class="speakers-grid-new">')
if speakers_start != -1:
    # Find the closing tag for speakers-grid-new
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
            print(f"Updated speakers/index.html with {len(matched_speakers)} speakers from WiFAI website")
        else:
            print("Could not find closing tag for speakers-grid-new")
    else:
        print("Could not properly parse speakers-grid-new structure")
else:
    print("Could not find speakers-grid-new in speakers/index.html")

print(f"\nProcessed {len(matched_speakers)} speakers from WiFAI website")
print("Maintained existing design and arrangements")

