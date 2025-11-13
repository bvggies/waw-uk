// Load shared header and footer components
(function() {
    // Determine the base path based on current page location
    function getBasePath() {
        const path = window.location.pathname;
        const depth = path.split('/').filter(p => p && p !== 'index.html').length - 1;
        return depth > 0 ? '../'.repeat(depth) : './';
    }

    const basePath = getBasePath();
    const componentsPath = basePath === './' ? './components/' : '../components/';

    // Load header
    fetch(componentsPath + 'header.html')
        .then(response => response.text())
        .then(html => {
            const headerPlaceholder = document.getElementById('header-placeholder');
            if (headerPlaceholder) {
                headerPlaceholder.outerHTML = html;
                // Re-initialize menu toggle after header is loaded
                initMenuToggle();
                // Initialize countdown timer if script.js is loaded
                if (typeof initCountdown === 'function') {
                    initCountdown();
                }
            }
        })
        .catch(error => console.error('Error loading header:', error));

    // Load footer
    function loadFooter() {
        fetch(componentsPath + 'footer.html')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to load footer');
                }
                return response.text();
            })
            .then(html => {
                const footerPlaceholder = document.getElementById('footer-placeholder');
                if (footerPlaceholder) {
                    footerPlaceholder.outerHTML = html;
                    // Font Awesome 6 uses CSS, so icons should work automatically
                    // But we can verify the icons are present
                    const icons = footerPlaceholder.querySelectorAll('.fab');
                    if (icons.length === 0) {
                        // Try to find icons in the newly inserted footer
                        const footer = document.getElementById('footer-outer');
                        if (footer) {
                            const footerIcons = footer.querySelectorAll('.fab');
                            console.log('Footer icons found:', footerIcons.length);
                        }
                    }
                }
            })
            .catch(error => console.error('Error loading footer:', error));
    }

    // Wait for Font Awesome CSS to be loaded before loading footer
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            // Small delay to ensure Font Awesome CSS is fully loaded
            setTimeout(loadFooter, 100);
        });
    } else {
        setTimeout(loadFooter, 100);
    }

    // Initialize menu toggle functionality
    function initMenuToggle() {
        const menuToggle = document.getElementById('menu-toggle');
        const mainNav = document.getElementById('main-nav');
        const closeMenu = document.querySelector('.close-menu');

        if (menuToggle && mainNav) {
            menuToggle.addEventListener('click', function() {
                mainNav.classList.toggle('active');
                document.body.classList.toggle('menu-open');
            });
        }

        if (closeMenu && mainNav) {
            closeMenu.addEventListener('click', function() {
                mainNav.classList.remove('active');
                document.body.classList.remove('menu-open');
            });
        }

        // Close menu when clicking outside
        document.addEventListener('click', function(event) {
            if (mainNav && mainNav.classList.contains('active')) {
                if (!mainNav.contains(event.target) && !menuToggle.contains(event.target)) {
                    mainNav.classList.remove('active');
                    document.body.classList.remove('menu-open');
                }
            }
        });
    }

    // Initialize on page load (in case components load before this script)
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initMenuToggle);
    } else {
        initMenuToggle();
    }
})();

