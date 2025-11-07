# Clear all speakers from the speakers page
with open('speakers/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the speakers-grid-new opening tag
start_marker = '<div class="speakers-grid-new">'
start_pos = content.find(start_marker)

if start_pos != -1:
    # Find the closing tag for speakers-grid-new
    # We need to find the matching </div> that closes speakers-grid-new
    # Count divs to find the correct closing tag
    search_pos = start_pos + len(start_marker)
    div_count = 1
    
    while div_count > 0 and search_pos < len(content):
        if search_pos + 4 <= len(content) and content[search_pos:search_pos+4] == '<div':
            div_count += 1
        elif search_pos + 5 <= len(content) and content[search_pos:search_pos+5] == '</div':
            div_count -= 1
            if div_count == 0:
                # Found the closing tag
                end_pos = search_pos + 6  # Include </div>
                break
        search_pos += 1
    else:
        # If we didn't find a proper closing, look for the next </div> after some content
        # Find the next </div> that appears after some whitespace/newlines
        temp_pos = content.find('</div>', start_pos + len(start_marker))
        if temp_pos != -1:
            # Check if there's content between start and this </div>
            between = content[start_pos + len(start_marker):temp_pos].strip()
            if between:
                end_pos = temp_pos + 6
            else:
                end_pos = start_pos + len(start_marker)
        else:
            end_pos = start_pos + len(start_marker)
    
    # Replace everything between opening and closing tags with just whitespace
    new_content = content[:start_pos + len(start_marker)] + '\n                                ' + content[end_pos:]
    
    # Also remove any old team-member content that might be after the grid
    # Find and remove any team-member divs that appear after speakers-grid-new
    # Look for patterns like: <div class="team-member" or <div class="vc_col-sm-3"> with team-member inside
    import re
    
    # Remove any orphaned team-member content after the closing </div> of speakers-grid-new
    # This is a bit tricky, so let's find where the wpb_wrapper div closes
    wrapper_end = new_content.find('</div>', new_content.find('</div>', end_pos) + 1)
    if wrapper_end != -1:
        # Check if there's team-member content between speakers-grid-new closing and wpb_wrapper closing
        between_content = new_content[end_pos:wrapper_end]
        if 'team-member' in between_content or 'vc_col-sm-3' in between_content:
            # Remove all team-member related content
            # Find the start of the first team-member or vc_col-sm-3 after speakers-grid-new closes
            cleanup_start = new_content.find('<div class="vc_col-sm-3">', end_pos)
            if cleanup_start == -1:
                cleanup_start = new_content.find('<div class="team-member"', end_pos)
            
            if cleanup_start != -1:
                # Find where this section ends (likely before the closing wpb_wrapper)
                # Look for the closing </div> of the wpb_wrapper
                cleanup_end = new_content.rfind('</div>', cleanup_start, wrapper_end)
                if cleanup_end != -1:
                    # Remove everything from cleanup_start to cleanup_end
                    new_content = new_content[:cleanup_start] + new_content[cleanup_end + 6:]
    
    with open('speakers/index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("Cleared all speakers from the speakers page")
    print("The speakers-grid-new div is now empty and ready for new content")
else:
    print("Could not find speakers-grid-new in the file")

