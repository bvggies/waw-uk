// Menu Toggle
const menuToggle = document.getElementById('menu-toggle');
const mainNav = document.getElementById('main-nav');
const closeMenu = document.querySelector('.close-menu');

if (menuToggle) {
    menuToggle.addEventListener('click', () => {
        mainNav.classList.toggle('active');
        menuToggle.classList.toggle('active');
        document.body.style.overflow = mainNav.classList.contains('active') ? 'hidden' : '';
    });
}

if (closeMenu) {
    closeMenu.addEventListener('click', () => {
        mainNav.classList.remove('active');
        if (menuToggle) menuToggle.classList.remove('active');
        document.body.style.overflow = '';
    });
}

// Search Toggle
const searchToggle = document.querySelector('.search-toggle');
const searchOverlay = document.getElementById('search-overlay');
const closeSearch = document.querySelector('.close-search');
const searchInput = document.getElementById('search-input');

if (searchToggle) {
    searchToggle.addEventListener('click', () => {
        searchOverlay.classList.add('active');
        searchInput.focus();
        document.body.style.overflow = 'hidden';
    });
}

if (closeSearch) {
    closeSearch.addEventListener('click', () => {
        searchOverlay.classList.remove('active');
        document.body.style.overflow = '';
    });
}

// Close search on ESC key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && searchOverlay.classList.contains('active')) {
        searchOverlay.classList.remove('active');
        document.body.style.overflow = '';
    }
});

// Dropdown Menus
const dropdowns = document.querySelectorAll('.has-dropdown, .has-submenu');

dropdowns.forEach(dropdown => {
    const link = dropdown.querySelector('a');
    
    if (link) {
        link.addEventListener('click', (e) => {
            // Prevent default link behavior on mobile
            if (window.innerWidth < 768) {
                e.preventDefault();
                dropdown.classList.toggle('active');
            }
        });
    }
});

// Desktop dropdown hover
if (window.innerWidth >= 768) {
    dropdowns.forEach(dropdown => {
        dropdown.addEventListener('mouseenter', () => {
            dropdown.classList.add('active');
        });
        
        dropdown.addEventListener('mouseleave', () => {
            dropdown.classList.remove('active');
        });
    });
}

// Close dropdowns when clicking outside
document.addEventListener('click', (e) => {
    if (!e.target.closest('.has-dropdown, .has-submenu')) {
        dropdowns.forEach(dropdown => {
            dropdown.classList.remove('active');
        });
    }
});

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#' && href.length > 1) {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    });
});

// Close mobile menu when clicking on a link
const navLinks = document.querySelectorAll('.nav-menu a');
navLinks.forEach(link => {
    link.addEventListener('click', () => {
        if (window.innerWidth < 768) {
            mainNav.classList.remove('active');
            if (menuToggle) menuToggle.classList.remove('active');
            document.body.style.overflow = '';
        }
    });
});

// Handle window resize
let resizeTimer;
window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(() => {
        // Close mobile menu on resize to desktop
        if (window.innerWidth >= 768) {
            mainNav.classList.remove('active');
            if (menuToggle) menuToggle.classList.remove('active');
            document.body.style.overflow = '';
        }
    }, 250);
});

// Add active state to navigation links based on scroll position
const sections = document.querySelectorAll('section');
const navLinksArray = Array.from(navLinks);

window.addEventListener('scroll', () => {
    let current = '';
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (window.pageYOffset >= sectionTop - 200) {
            current = section.getAttribute('id');
        }
    });

    navLinksArray.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });
});

// Video Parallax Effect
const nectarVideo = document.querySelector('.nectar-video-bg');
const videoWrap = document.querySelector('.nectar-video-wrap');

if (nectarVideo && videoWrap) {
    // Parallax effect on scroll
    let ticking = false;
    
    function updateParallax() {
        if (!ticking) {
            window.requestAnimationFrame(() => {
                const rect = videoWrap.getBoundingClientRect();
                const isVisible = rect.top < window.innerHeight && rect.bottom > 0;
                
                if (isVisible) {
                    const scrollY = window.pageYOffset;
                    const elementTop = videoWrap.offsetTop;
                    const elementHeight = videoWrap.offsetHeight;
                    const windowHeight = window.innerHeight;
                    
                    // Calculate parallax offset
                    const scrolled = scrollY - elementTop + windowHeight;
                    const parallaxSpeed = 0.2; // Adjust speed as needed
                    const translateY = (scrolled - windowHeight) * parallaxSpeed;
                    
                    nectarVideo.style.transform = `translate3d(0px, ${translateY}px, 0px)`;
                }
                
                ticking = false;
            });
            
            ticking = true;
        }
    }
    
    window.addEventListener('scroll', updateParallax);
    updateParallax(); // Initial call
}

// Fade-in animation
const animatedElements = document.querySelectorAll('[data-bg-animation="fade-in"]');
if (animatedElements.length > 0) {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated-in');
            }
        });
    }, observerOptions);
    
    animatedElements.forEach(el => {
        observer.observe(el);
    });
}

// Load fancy box background images with loading state
const fancyBoxes = document.querySelectorAll('.box-bg[data-nectar-img-src]');
fancyBoxes.forEach(box => {
    const imgSrc = box.getAttribute('data-nectar-img-src');
    if (imgSrc) {
        // Add loading class
        box.classList.add('loading');
        
        // Create image element to preload
        const img = new Image();
        img.onload = () => {
            box.style.backgroundImage = `url(${imgSrc})`;
            box.classList.remove('loading');
            box.classList.add('loaded');
        };
        img.onerror = () => {
            box.classList.remove('loading');
            box.classList.add('error');
        };
        img.src = imgSrc;
    }
});

// Add loading animation for images
const style = document.createElement('style');
style.textContent = `
    .box-bg.loading {
        background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
        background-size: 200% 100%;
        animation: loading 1.5s infinite;
    }
    
    @keyframes loading {
        0% { background-position: 200% 0; }
        100% { background-position: -200% 0; }
    }
    
    .box-bg.loaded {
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
`;
document.head.appendChild(style);

// Performance: Lazy load images with IntersectionObserver
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    observer.unobserve(img);
                }
            }
        });
    }, {
        rootMargin: '50px'
    });
    
    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

// Add loaded class to lazy-loaded images
document.querySelectorAll('img[loading="lazy"]').forEach(img => {
    if (img.complete) {
        img.classList.add('loaded');
    } else {
        img.addEventListener('load', () => {
            img.classList.add('loaded');
        });
    }
});

// Handle Google Drive image loading errors for speaker images
document.addEventListener('DOMContentLoaded', () => {
    const speakerImages = document.querySelectorAll('.team-member-image');
    
    speakerImages.forEach(imgDiv => {
        const bgImage = imgDiv.style.backgroundImage;
        if (bgImage && bgImage.includes('drive.google.com')) {
            // Extract URL from background-image style
            const urlMatch = bgImage.match(/url\(['"]?([^'"]+)['"]?\)/);
            if (urlMatch) {
                const imageUrl = urlMatch[1];
                
                // Create a test image to check if it loads
                const testImg = new Image();
                testImg.crossOrigin = 'anonymous';
                testImg.onload = () => {
                    // Image loaded successfully - ensure it's set
                    if (!imgDiv.style.backgroundImage.includes(imageUrl)) {
                        imgDiv.style.backgroundImage = `url('${imageUrl}')`;
                    }
                };
                testImg.onerror = () => {
                    // Image failed to load - try alternative format
                    const fileIdMatch = imageUrl.match(/[?&]id=([a-zA-Z0-9_-]+)/);
                    if (fileIdMatch) {
                        const fileId = fileIdMatch[1];
                        // Try alternative URL format
                        const altUrl = `https://drive.google.com/uc?export=download&id=${fileId}`;
                        const altTestImg = new Image();
                        altTestImg.crossOrigin = 'anonymous';
                        altTestImg.onload = () => {
                            imgDiv.style.backgroundImage = `url('${altUrl}')`;
                        };
                        altTestImg.onerror = () => {
                            // Both formats failed - add error class for styling
                            imgDiv.classList.add('image-error');
                            console.warn(`Failed to load speaker image: ${imageUrl}`);
                        };
                        altTestImg.src = altUrl;
                    } else {
                        // No file ID found - add error class
                        imgDiv.classList.add('image-error');
                    }
                };
                testImg.src = imageUrl;
            }
        }
    });
});

// WiFAI Speakers Search Functionality
document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('speakersSearch');
    const clearButton = document.getElementById('speakersClear');
    const speakersGrid = document.getElementById('speakersGrid');
    const noResults = document.getElementById('speakersNoResults');
    
    if (!searchInput || !speakersGrid) return;
    
    const speakerCards = Array.from(speakersGrid.querySelectorAll('.speaker-card'));
    
    function filterSpeakers() {
        const searchTerm = searchInput.value.toLowerCase().trim();
        let visibleCount = 0;
        
        speakerCards.forEach(card => {
            const name = card.querySelector('.speaker-name')?.textContent.toLowerCase() || '';
            const role = card.querySelector('.speaker-role')?.textContent.toLowerCase() || '';
            const excerpt = card.querySelector('.speaker-excerpt')?.textContent.toLowerCase() || '';
            
            const matches = !searchTerm || 
                name.includes(searchTerm) || 
                role.includes(searchTerm) || 
                excerpt.includes(searchTerm);
            
            if (matches) {
                card.style.display = '';
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });
        
        // Show/hide no results message
        if (noResults) {
            if (visibleCount === 0 && searchTerm) {
                noResults.style.display = 'block';
                speakersGrid.style.display = 'none';
            } else {
                noResults.style.display = 'none';
                speakersGrid.style.display = 'grid';
            }
        }
    }
    
    // Search input event
    searchInput.addEventListener('input', filterSpeakers);
    
    // Clear button event
    if (clearButton) {
        clearButton.addEventListener('click', () => {
            searchInput.value = '';
            filterSpeakers();
            searchInput.focus();
        });
    }
    
    // Show clear button when there's text
    searchInput.addEventListener('input', () => {
        if (clearButton) {
            clearButton.style.display = searchInput.value.trim() ? 'block' : 'none';
        }
    });
});