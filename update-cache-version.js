// Cache Version Updater
// Run this script to update the version number across all HTML files
// Usage: node update-cache-version.js

const fs = require('fs');
const path = require('path');

// Get new version from command line or increment current
const args = process.argv.slice(2);
let newVersion = args[0] || '1.0.1';

// Update version.js
const versionJsPath = path.join(__dirname, 'version.js');
const versionJsContent = `// Version number - Update this whenever you make changes to force cache refresh
window.SITE_VERSION = '${newVersion}';
`;
fs.writeFileSync(versionJsPath, versionJsContent);
console.log(`✓ Updated version.js to ${newVersion}`);

// List of HTML files to update
const htmlFiles = [
    'index.html',
    'about-us/index.html',
    'exhibition/index.html',
    'experience/index.html',
    'faq/index.html',
    'media/index.html',
    'our-sponsors/index.html',
    'speakers/index.html',
    'travel-info/index.html',
    'contact-us/index.html',
    'terms-conditions/index.html',
    'privacy-policy/index.html',
    'events/index.html',
    'pre-register/index.html',
    'tickets/index.html'
];

// Patterns to replace
const patterns = [
    {
        // CSS files
        regex: /href=["']([^"']*\.css)(\?v=[\d.]+)?["']/g,
        replacement: `href="$1?v=${newVersion}"`
    },
    {
        // JS files (except version.js which has its own pattern)
        regex: /src=["']([^"']*\.js)(\?v=[\d.]+)?["']/g,
        replacement: (match, file) => {
            if (file.includes('version.js')) {
                return match.replace(/\?v=[\d.]+/, `?v=${newVersion}`);
            }
            return `src="${file}?v=${newVersion}"`;
        }
    },
    {
        // version.js script tag
        regex: /src=["']version\.js(\?v=[\d.]+)?["']/g,
        replacement: `src="version.js?v=${newVersion}"`
    },
    {
        // Add cache-control meta tags if not present
        regex: /<meta name="theme-color"/,
        replacement: `<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <meta http-equiv="Pragma" content="no-cache">
    <meta http-equiv="Expires" content="0">
    <meta name="theme-color"`
    }
];

// Update each HTML file
htmlFiles.forEach(file => {
    const filePath = path.join(__dirname, file);
    
    if (!fs.existsSync(filePath)) {
        console.log(`⚠ Skipping ${file} (not found)`);
        return;
    }
    
    let content = fs.readFileSync(filePath, 'utf8');
    let updated = false;
    
    // Apply patterns
    patterns.forEach(pattern => {
        if (typeof pattern.replacement === 'function') {
            const newContent = content.replace(pattern.regex, pattern.replacement);
            if (newContent !== content) {
                content = newContent;
                updated = true;
            }
        } else {
            const newContent = content.replace(pattern.regex, pattern.replacement);
            if (newContent !== content) {
                content = newContent;
                updated = true;
            }
        }
    });
    
    // Add version.js script if not present (for root index.html)
    if (file === 'index.html' && !content.includes('version.js')) {
        content = content.replace(
            /<title>([^<]+)<\/title>/,
            `<title>$1</title>
    <script src="version.js?v=${newVersion}"></script>`
        );
        updated = true;
    }
    
    // Add version.js script for subdirectory pages
    if (file !== 'index.html' && !content.includes('version.js')) {
        content = content.replace(
            /<title>([^<]+)<\/title>/,
            `<title>$1</title>
    <script src="../version.js?v=${newVersion}"></script>`
        );
        updated = true;
    }
    
    if (updated) {
        fs.writeFileSync(filePath, content, 'utf8');
        console.log(`✓ Updated ${file}`);
    } else {
        console.log(`- No changes needed for ${file}`);
    }
});

console.log(`\n✅ Cache version updated to ${newVersion} across all files!`);
console.log(`\nTo force browsers to reload, users can:`);
console.log(`1. Hard refresh: Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)`);
console.log(`2. Clear browser cache`);
console.log(`3. Open in incognito/private mode`);

