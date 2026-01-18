// Enhanced Tesla Research Hub JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Add smooth scrolling for navigation
    const sections = document.querySelectorAll('section');
    const navItems = [];

    // Create navigation menu
    createNavigationMenu();
    
    // Add scroll animations
    addScrollAnimations();
    
    // Add interactive elements
    addInteractiveElements();
    
    // Add audio player for podcast
    addAudioPlayer();

    function createNavigationMenu() {
        const nav = document.createElement('nav');
        nav.className = 'floating-nav';
        
        const navList = document.createElement('ul');
        
        sections.forEach((section, index) => {
            const navItem = document.createElement('li');
            const navLink = document.createElement('a');
            navLink.href = `#${section.id}`;
            navLink.textContent = section.querySelector('h2').textContent;
            navLink.addEventListener('click', smoothScroll);
            
            navItem.appendChild(navLink);
            navList.appendChild(navItem);
            navItems.push(navLink);
        });
        
        nav.appendChild(navList);
        document.body.appendChild(nav);
    }

    function smoothScroll(e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');
        const targetSection = document.querySelector(targetId);
        
        targetSection.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
        
        // Update active nav item
        navItems.forEach(item => item.classList.remove('active'));
        this.classList.add('active');
    }

    function addScrollAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                }
            });
        }, observerOptions);

        sections.forEach(section => {
            section.classList.add('fade-in');
            observer.observe(section);
        });
    }

    function addInteractiveElements() {
        // Add expandable sections for detailed content
        const detailSections = document.querySelectorAll('h3');
        
        detailSections.forEach(heading => {
            const content = heading.nextElementSibling;
            if (content && content.tagName === 'P') {
                heading.classList.add('expandable');
                heading.addEventListener('click', function() {
                    this.classList.toggle('expanded');
                    content.classList.toggle('expanded');
                });
            }
        });

        // Add hover effects to links
        const links = document.querySelectorAll('a[href^="http"]');
        links.forEach(link => {
            link.classList.add('external-link');
            link.setAttribute('target', '_blank');
            link.setAttribute('rel', 'noopener noreferrer');
        });
    }

    function addAudioPlayer() {
        // Create audio player section
        const audioSection = document.createElement('section');
        audioSection.id = 'podcast-player';
        audioSection.innerHTML = `
            <h2>Podcast Episode: Tesla's Wireless Power - Myth vs Reality</h2>
            <div class="audio-player">
                <div class="audio-info">
                    <p>A comprehensive analysis of Tesla's wireless power concepts and the myths surrounding "free energy" has been prepared. The audio file is available separately due to size constraints.</p>
                    <p>The podcast covers Tesla's actual work, scientific analysis of his concepts, and separates fact from fiction regarding wireless power and free energy claims.</p>
                </div>
            </div>
        `;
        
        // Insert before conclusion
        const conclusion = document.querySelector('#conclusion');
        conclusion.parentNode.insertBefore(audioSection, conclusion);
    }

    // Add keyboard navigation
    document.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
            const currentSection = getCurrentSection();
            const currentIndex = Array.from(sections).indexOf(currentSection);
            
            let nextIndex;
            if (e.key === 'ArrowDown') {
                nextIndex = Math.min(currentIndex + 1, sections.length - 1);
            } else {
                nextIndex = Math.max(currentIndex - 1, 0);
            }
            
            sections[nextIndex].scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });

    function getCurrentSection() {
        let current = sections[0];
        sections.forEach(section => {
            const rect = section.getBoundingClientRect();
            if (rect.top <= 100) {
                current = section;
            }
        });
        return current;
    }
});

