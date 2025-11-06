import json
import html
import re

def escape_html(text):
    """Escape HTML special characters"""
    if not text:
        return ""
    return html.escape(str(text))

def generate_speaker_card(speaker, index):
    """Generate HTML for a single speaker card using img tag instead of background-image"""
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
    
    # Use img tag instead of background-image for better error handling
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

# Load speakers data
with open('assets/speakers.json', 'r', encoding='utf-8') as f:
    speakers = json.load(f)

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

print(f"Generated HTML with img tags for {len(homepage_speakers)} homepage speakers")
print(f"Generated HTML with img tags for {len(speakers)} speakers page")

