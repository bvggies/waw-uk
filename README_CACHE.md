# Cache-Busting System for WiFAI Website

This website includes a comprehensive cache-busting system to ensure all browsers display the latest updates.

## How It Works

1. **Version File**: `version.js` contains the current site version
2. **Query Parameters**: All CSS and JS files include version query parameters (e.g., `styles.css?v=1.0.1`)
3. **Meta Tags**: HTML files include cache-control meta tags
4. **Client-Side Check**: JavaScript checks for version changes and forces reload if needed
5. **Server Headers**: `.htaccess` file (if using Apache) sets proper cache headers

## Updating the Version

When you make changes to the website, update the version to force browsers to reload:

### Method 1: Using Python Script (Recommended)
```bash
python update_cache_version.py 1.0.2
```

### Method 2: Manual Update
1. Edit `version.js` and change the version number
2. Update all HTML files to use the new version in query parameters
3. Update CSS/JS file references

## Files Modified

- `version.js` - Contains current version
- `update_cache_version.py` - Script to update versions across all files
- All HTML files - Include cache-control meta tags and versioned assets
- `script.js` - Includes client-side cache-busting logic
- `components/load-components.js` - Uses cache-busting for component loads
- `.htaccess` - Server-side cache headers (Apache)

## For Users Experiencing Cache Issues

If users see old content, they can:

1. **Hard Refresh**: 
   - Windows/Linux: `Ctrl + Shift + R` or `Ctrl + F5`
   - Mac: `Cmd + Shift + R`

2. **Clear Browser Cache**:
   - Chrome: Settings > Privacy > Clear browsing data
   - Firefox: Settings > Privacy > Clear Data
   - Safari: Preferences > Privacy > Manage Website Data

3. **Incognito/Private Mode**: Open the site in a private browsing window

4. **Disable Cache** (for developers):
   - Chrome DevTools: Network tab > Check "Disable cache"

## Version History

- 1.0.1 - Initial cache-busting implementation
- 1.0.0 - Base version

## Notes

- The version number should be incremented whenever significant changes are made
- Minor updates can use patch version (1.0.1, 1.0.2, etc.)
- Major updates should use major version (2.0.0, 3.0.0, etc.)

