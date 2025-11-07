# Clear ALL speakers and old content from the speakers page
with open('speakers/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the speakers-grid-new opening tag
start_marker = '<div class="speakers-grid-new">'
start_pos = content.find(start_marker)

if start_pos != -1:
    # Find the closing tag for the wpb_wrapper that contains speakers-grid-new
    # First, find where speakers-grid-new closes
    search_pos = start_pos + len(start_marker)
    div_count = 1
    
    # Find the closing </div> for speakers-grid-new
    while div_count > 0 and search_pos < len(content):
        if search_pos + 4 <= len(content) and content[search_pos:search_pos+4] == '<div':
            div_count += 1
        elif search_pos + 5 <= len(content) and content[search_pos:search_pos+5] == '</div':
            div_count -= 1
            if div_count == 0:
                grid_end_pos = search_pos + 6
                break
        search_pos += 1
    else:
        # Fallback: find next </div>
        grid_end_pos = content.find('</div>', start_pos + len(start_marker)) + 6
    
    # Now find where wpb_wrapper closes (this should be after all speaker content)
    # Look backwards from grid_end_pos to find the wpb_wrapper opening
    wrapper_start = content.rfind('<div class="wpb_wrapper">', 0, start_pos)
    
    # Find the closing </div> for wpb_wrapper
    # Count divs from wrapper_start
    wrapper_search = wrapper_start
    wrapper_div_count = 1
    while wrapper_div_count > 0 and wrapper_search < len(content):
        if wrapper_search + 4 <= len(content) and content[wrapper_search:wrapper_search+4] == '<div':
            wrapper_div_count += 1
        elif wrapper_search + 5 <= len(content) and content[wrapper_search:wrapper_search+5] == '</div':
            wrapper_div_count -= 1
            if wrapper_div_count == 0:
                wrapper_end_pos = wrapper_search + 6
                break
        wrapper_search += 1
    else:
        # Fallback
        wrapper_end_pos = content.find('</div>', grid_end_pos) + 6
    
    # Check if there's old content between grid_end_pos and wrapper_end_pos
    old_content = content[grid_end_pos:wrapper_end_pos]
    
    # Remove everything between speakers-grid-new opening and closing, and any old content after
    new_content = content[:start_pos + len(start_marker)] + '\n                                ' + content[wrapper_end_pos:]
    
    # Also check for any remaining team-member or vc_col-sm-3 content and remove it
    import re
    # Remove any orphaned divs with team-member or vc_col-sm-3 classes
    new_content = re.sub(r'<div class="vc_col-sm-3">.*?</div>\s*</div>', '', new_content, flags=re.DOTALL)
    new_content = re.sub(r'<div class="team-member".*?</div>\s*</div>', '', new_content, flags=re.DOTALL)
    
    # Clean up any orphaned tags
    new_content = re.sub(r'<a href="#"\s*></a>', '', new_content)
    new_content = re.sub(r'<div class="team-member-image">.*?</div>', '', new_content, flags=re.DOTALL)
    new_content = re.sub(r'<div class="team-meta">.*?</div>', '', new_content, flags=re.DOTALL)
    
    with open('speakers/index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("Cleared all speakers and old content from the speakers page")
    print("The speakers-grid-new div is now completely empty")
else:
    print("Could not find speakers-grid-new in the file")

