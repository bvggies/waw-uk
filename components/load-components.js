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

    // Check if Font Awesome CSS is loaded
    function isFontAwesomeLoaded() {
        // Check if Font Awesome stylesheet is loaded by testing if a FA class exists
        const testEl = document.createElement('i');
        testEl.className = 'fab fa-facebook';
        testEl.style.position = 'absolute';
        testEl.style.visibility = 'hidden';
        document.body.appendChild(testEl);
        const computed = window.getComputedStyle(testEl, ':before');
        const content = computed.getPropertyValue('content');
        document.body.removeChild(testEl);
        return content && content !== 'none' && content !== '';
    }

    // Wait for Font Awesome to load
    function waitForFontAwesome(callback, maxAttempts = 50) {
        let attempts = 0;
        const checkInterval = setInterval(function() {
            attempts++;
            if (isFontAwesomeLoaded() || attempts >= maxAttempts) {
                clearInterval(checkInterval);
                callback();
            }
        }, 100);
    }

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
                    // Force a reflow to ensure CSS is applied
                    const footer = document.getElementById('footer-outer');
                    if (footer) {
                        footer.offsetHeight; // Trigger reflow
                    }
                }
            })
            .catch(error => console.error('Error loading footer:', error));
    }

    // Wait for Font Awesome CSS to be loaded before loading footer
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            waitForFontAwesome(loadFooter);
        });
    } else {
        waitForFontAwesome(loadFooter);
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

