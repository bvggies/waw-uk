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

# Save to file
with open('assets/all_speakers_redesigned.html', 'w', encoding='utf-8') as f:
    f.write(all_speakers_html)

print(f"Generated redesigned HTML for {len(speakers)} speakers")

