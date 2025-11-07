import html
import re

def escape_html(text):
    """Escape HTML special characters"""
    if not text:
        return ""
    return html.escape(str(text))

def normalize_linkedin_url(url):
    """Normalize LinkedIn URL"""
    if not url or not url.strip():
        return "#"
    
    url = url.strip()
    
    # Fix double protocol
    url = re.sub(r'^https?://[Hh]ttps?://', 'https://', url)
    
    # Add protocol if missing
    if not url.startswith('http'):
        url = 'https://' + url.lstrip('/')
    
    # Ensure it's a proper LinkedIn URL
    if 'linkedin.com' not in url.lower():
        return "#"
    
    return url

# All 28 speakers from WiFAI website with exact structure
wifai_speakers = [
    {"name": "Tambra Raye Stevenson", "org": "Women Advancing Nutrition Dietetics and Agriculture", "title": "Founder", "linkedin": "LinkedIn.com/in/tambra.html", "img": "https://wifai.org.uk/wp-content/uploads/2025/09/IG-Post_20241119_140304_0000-Tambra-Raye-Stevenson.png"},
    {"name": "Antoinette Sallah", "org": "Solirag X", "title": "C.E.O", "linkedin": "www.linkedin.com/index.html#/", "img": "../wp-content/uploads/2025/09/20250526_184038-SAL-LOUM-scaled.jpg"},
    {"name": "Layla", "org": "Iddyba Foundation", "title": "Founder", "linkedin": "www.linkedin.com/index.html#/", "img": "../wp-content/uploads/2025/09/Profile-Picture-L-Davies-1-scaled.jpg"},
    {"name": "VERONICA ANNOR", "org": "CAPGEMINI", "title": "Consultant", "linkedin": "www.linkedin.com/in/thewuraola.html", "img": "../wp-content/uploads/2025/09/IMG_6435-Veronica-Annor-scaled.jpg"},
    {"name": "Miracle Opeyemi Ogunbowale", "org": "El'mira Consults.", "title": "Founder", "linkedin": "www.linkedin.com/in/thewuraola.html", "img": "../wp-content/uploads/2025/09/WhatsApp-Image-2025-03-10-at-10.13.45-Miracle-Ogunbowale-1.jpg"},
    {"name": "Ayeni-Wuraola Ogungbola", "org": "Nutrifield Foods", "title": "C.E.O", "linkedin": "http://www.linkedin.com/in/thewuraola", "img": "../wp-content/uploads/2025/09/headshot-3-AYENI-WURAOLA-OGUNGBOLA-scaled.jpg"},
    {"name": "Constanza I. Robles Fumarola", "org": "Inanna", "title": "Founding Member", "linkedin": "https://www.linkedin.com/in/constanzarobles/", "img": "../wp-content/uploads/2025/09/Constanza_1-removebg-preview-Constanza-Robles-Fumarola.jpg"},
    {"name": "Janet Mulu ITS", "org": "ImpactDev Africa", "title": "Trade Specialist", "linkedin": "https://www.linkedin.com/in/janetmulu/", "img": "../wp-content/uploads/2025/09/Profile-Pic-Janet-Mulu-scaled.jpg"},
    {"name": "Samara Dias", "org": "Ella Africa Foundation", "title": "C.E.O", "linkedin": "https://www.linkedin.com/in/samaravdias/", "img": "../wp-content/uploads/2025/09/Screenshot-2025-08-18-at-09.35.53-Samara-Dias.png"},
    {"name": "Gloria Dalafu", "org": "School2u virtual academy", "title": "Founder", "linkedin": "https://www.linkedin.com/#/", "img": "../wp-content/uploads/2025/09/45816c9b-9a63-481c-8b43-b7b092d2d83f28-Bashira.jpg"},
    {"name": "Omu Obilor", "org": "Ómu Consulting Limited", "title": "C.E.O", "linkedin": "https://www.linkedin.com/in/omuobilor", "img": "../wp-content/uploads/2025/09/DSC05380-Omu-Obilor-Experience-Africa-scaled.jpg"},
    {"name": "Ilona Karpanos", "org": "Cambridgeshire Chamber of Commerce", "title": "Manager", "linkedin": "https://www.linkedin.com/#/", "img": "../wp-content/uploads/2025/09/IMG_0751-I-K.jpg"},
    {"name": "Abeni Ramsey", "org": "CITY Girl farms", "title": "Founder", "linkedin": "https://www.linkedin.com/in/abeni-ramsey-6945b9a/", "img": "../wp-content/uploads/2025/09/IMG_0798-Abeni-Ramsey-1.jpg"},
    {"name": "Vivian Maduekeh", "org": "Food Health Systems Advisory", "title": "Managing Partner", "linkedin": "https://www.linkedin.com/in/vivianmaduekeh", "img": "https://wifai.org.uk/wp-content/uploads/2025/09/IMG_20220508_025348_503-VIVIAN-MADUEKEH.webp"},
    {"name": "Fatimah Bamisedun", "org": "Anre Solutions", "title": "Director", "linkedin": "https://www.linkedin.com/in/fatimah-bamisedun", "img": "../wp-content/uploads/2025/09/IMG_9971-Fatimah-Bamisedun.jpg"},
    {"name": "Deretho Francis ZIGBE", "org": "Starz Risk Solutions", "title": "Founder & CEO", "linkedin": "www.linkedin.com/in/deretho-f-zigbe-mba-a7a69aa4.html", "img": "../wp-content/uploads/2025/09/WhatsApp-Image-2025-07-08-at-14.53.15_852f8d13-ZIGBE-Deretho-Francis.jpg"},
    {"name": "Anna Jones", "org": "Just Farmers", "title": "Founder", "linkedin": "https://www.linkedin.com/in/jonesthejourno/", "img": "../wp-content/uploads/2025/09/Anna-002-Anna-Jones-1-scaled.jpg"},
    {"name": "D. Spence", "org": "YAHMAPP LTD", "title": "C.E.O", "linkedin": "http://www.linkedin.com/in/dwaynespence", "img": "../wp-content/uploads/2025/09/53d603f9-d405-454f-8151-9b64688aa0c9-Yahmapp.jpg"},
    {"name": "Anne Nicholls", "org": "Mimi Pia: Period CIC", "title": "C.E.O", "linkedin": "http://linkedin.com/in/anne-nicholls", "img": "../wp-content/uploads/2025/09/Untitled-design-7-Anne-Nicholls-1.png"},
    {"name": "SMG", "org": "SenBritish Group", "title": "Founder", "linkedin": "http://linkedin.com/in/serigne-mansour-gaye-09525117", "img": "../wp-content/uploads/2025/09/IMG_2120-Mansour-Gaye.jpg"},
    {"name": "Sandrine Henton", "org": "EG Capital", "title": "C.E.O", "linkedin": "https://www.linkedin.com/in/sandrine-henton-1396405", "img": "https://media.licdn.com/dms/image/v2/D4D03AQGsngl_boGXQQ/profile-displayphoto-shrink_200_200/profile-displayphoto-shrink_200_200/0/1672006410051?e=1761782400&v=beta&t=8CMg9_sLPeNI1jKVyPaRYCAfLLoktMvq1tjOuJx2E3s"},
    {"name": "Ozlem Bacak", "org": "Luviland Ltd", "title": "Entrepreneur", "linkedin": "http://linkedin.com/in/özlem-bacak-2104232a", "img": "../wp-content/uploads/2025/09/WhatsApp-Image-2025-09-06-at-22.20.12-Ozlem-Bacak.jpg"},
    {"name": "Prama Bhardwaj", "org": "Mantis World & Gerana Initiative", "title": "C.E.O", "linkedin": "https://www.linkedin.com/in/pramabhardwaj/", "img": "https://media.licdn.com/dms/image/v2/D4E03AQGibqSd6w3DkA/profile-displayphoto-scale_200_200/B4EZkpKUxmKQAY-/0/1757332197921?e=1761782400&v=beta&t=rS56hKSrE9fSOlcUa8Rf6RN9q2txMHRBoSSvcUP_xD8"},
    {"name": "Evelyn Alice Lucy Tuhairwe Karokora", "org": "Tesifa Sustainable Farm", "title": "Founder", "linkedin": "http://www.linkedin.com/in/evelyn-karokora-5ba35634", "img": "../wp-content/uploads/2025/09/professional-pic-2021-Evelyn-Karokora-scaled.jpg"},
    {"name": "Lucy Antwi-Boateng", "org": "Farrer & Co LLP", "title": "Project Manager", "linkedin": "https://www.linkedin.com/in/lucy-antwi-boateng-343847169", "img": "../wp-content/uploads/2025/09/IMG_2917-Lucy-Antwi-Boateng-scaled.jpg"},
    {"name": "Michaelle Kubwimana", "org": "Kawah Coffee Ltd", "title": "C.E.O", "linkedin": "https://www.linkedin.com/in/michaelle-kubwimana-08b57b26/", "img": "../wp-content/uploads/2025/09/Portrait-Gary-2-small-Kawah-coffee-scaled.jpg"},
    {"name": "Dolapo Enejoh", "org": "Food system and nutrition advisor", "title": "C.E.O", "linkedin": "https://www.linkedin.com/in/dolapoenejoh", "img": "../wp-content/uploads/2025/09/Dolapo-Passport-Dolapo-Enejoh.jpg"},
    {"name": "Johnson Bada", "org": "Go-Geeper Limited", "title": "C.E.O", "linkedin": "https://www.linkedin.com/in/johnsonbada/", "img": "../wp-content/uploads/2025/09/JB_25-Johnson-Bada-scaled.png"},
]

def generate_speaker_card(speaker):
    """Generate HTML for a single speaker card matching WiFAI exact structure"""
    name = escape_html(speaker['name'])
    org = escape_html(speaker['org'])
    title = escape_html(speaker.get('title', ''))
    linkedin = normalize_linkedin_url(speaker.get('linkedin', '#'))
    img = speaker.get('img', 'https://via.placeholder.com/400x400?text=Speaker')
    
    # Determine if link should open in new tab
    link_attrs = ''
    if linkedin != "#" and linkedin.startswith('http'):
        link_attrs = 'target="_blank" rel="noopener"'
    
    return f'''<article class="speaker-card">
      <div class="speaker-photo-wrap">
        <img decoding="async" class="speaker-photo" src="{img}" alt="{name}">
      </div>
      <div class="speaker-body">
        <h3 class="speaker-name">{name}</h3>
        <p class="speaker-role">{org}</p>
        <div class="speaker-excerpt">{title}</div>
        <a class="speaker-link" href="{linkedin}" {link_attrs}>View Profile</a>
      </div>
    </article>'''

# Generate all speakers HTML
all_speakers_html = "\n".join([generate_speaker_card(speaker) for speaker in wifai_speakers])

# Generate the complete speakers page structure
speakers_page_html = f'''<div class="speakers-page">
  <div class="speakers-header">
    <h1 class="speakers-title">CONFERENCE SPEAKERS</h1>

    <div class="speakers-search">
      <input id="speakersSearch" type="search" placeholder="Search" aria-label="Search speakers">
      <button id="speakersClear" type="button" aria-label="Clear search">✕</button>
    </div>
  </div>

  <div id="speakersGrid" class="speakers-grid" aria-live="polite">

{all_speakers_html}

  </div>

  <div id="speakersNoResults" class="no-results" style="display:none;">No speakers found.</div>
</div>'''

# Update speakers/index.html
with open('speakers/index.html', 'r', encoding='utf-8') as f:
    speakers_page_content = f.read()

# Find the wpb_wrapper div and replace its content
wpb_wrapper_start = speakers_page_content.find('<div class="wpb_wrapper">')
if wpb_wrapper_start != -1:
    # Find the closing tag for wpb_wrapper
    search_pos = wpb_wrapper_start + len('<div class="wpb_wrapper">')
    div_count = 1
    
    while div_count > 0 and search_pos < len(speakers_page_content):
        if search_pos + 4 <= len(speakers_page_content) and speakers_page_content[search_pos:search_pos+4] == '<div':
            div_count += 1
        elif search_pos + 5 <= len(speakers_page_content) and speakers_page_content[search_pos:search_pos+5] == '</div':
            div_count -= 1
            if div_count == 0:
                wpb_wrapper_end = search_pos + 6
                break
        search_pos += 1
    else:
        wpb_wrapper_end = speakers_page_content.find('</div>', wpb_wrapper_start + len('<div class="wpb_wrapper">')) + 6
    
    # Replace everything between opening and closing tags
    speakers_page_content = speakers_page_content[:wpb_wrapper_start + len('<div class="wpb_wrapper">')] + '\n' + speakers_page_html + '\n                            ' + speakers_page_content[wpb_wrapper_end:]
    
    with open('speakers/index.html', 'w', encoding='utf-8') as f:
        f.write(speakers_page_content)
    
    print(f"Copied exact WiFAI structure with {len(wifai_speakers)} speakers")
    print("Maintained exact HTML structure, classes, and layout from WiFAI")
else:
    print("Could not find wpb_wrapper in speakers/index.html")

