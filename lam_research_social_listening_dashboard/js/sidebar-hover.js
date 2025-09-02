/**
 * Sidebar Hover Functionality
 * Handles the show/hide behavior of the sidebar based on mouse position
 */

document.addEventListener('DOMContentLoaded', function() {
    // Target the actual sidebar and main content elements from the HTML structure
    const sidebar = document.querySelector('aside');
    const mainContent = document.querySelector('main');
    
    if (!sidebar || !mainContent) {
        console.warn('Sidebar or main content elements not found');
        return;
    }

    let isHoveringSidebar = false;
    let isHoveringLeftEdge = false;

    // Add CSS transitions for smooth animations
    sidebar.style.transition = 'transform 0.3s ease-in-out';
    mainContent.style.transition = 'margin-left 0.3s ease-in-out, width 0.3s ease-in-out';

    // Function to hide sidebar
    function hideSidebar() {
        sidebar.style.transform = 'translateX(-100%)';
        mainContent.style.marginLeft = '0';
        mainContent.style.width = '100%';
    }

    // Function to show sidebar
    function showSidebar() {
        sidebar.style.transform = 'translateX(0)';
        mainContent.style.marginLeft = '25%';
        mainContent.style.width = '75%';
    }

    // Hide sidebar when hovering over main content
    mainContent.addEventListener('mouseenter', function(e) {
        // Only hide if not hovering over sidebar or left edge
        if (!isHoveringSidebar && !isHoveringLeftEdge) {
            hideSidebar();
        }
    });

    // Keep sidebar visible when hovering over it
    sidebar.addEventListener('mouseenter', function() {
        isHoveringSidebar = true;
        showSidebar();
    });

    sidebar.addEventListener('mouseleave', function() {
        isHoveringSidebar = false;
        // Hide sidebar after a small delay to prevent flickering
        setTimeout(() => {
            if (!isHoveringSidebar && !isHoveringLeftEdge) {
                hideSidebar();
            }
        }, 200);
    });

    // Show sidebar when hovering near left edge of screen
    document.addEventListener('mousemove', function(e) {
        if (e.clientX <= 20) {
            isHoveringLeftEdge = true;
            showSidebar();
        } else if (e.clientX > 300) {
            isHoveringLeftEdge = false;
            // Hide sidebar if not hovering over it and not over left edge
            if (!isHoveringSidebar) {
                setTimeout(() => {
                    if (!isHoveringSidebar && !isHoveringLeftEdge) {
                        hideSidebar();
                    }
                }, 200);
            }
        }
    });

    // Handle window resize to maintain proper layout
    window.addEventListener('resize', function() {
        if (sidebar.style.transform === 'translateX(-100%)') {
            hideSidebar();
        } else {
            showSidebar();
        }
    });

    // Initialize sidebar state as visible
    showSidebar();
});

// Load and display average sentiment values for company A (Lam Research)
document.addEventListener('DOMContentLoaded', function() {
    function setSentimentValue(id, value, colorClass) {
        const el = document.getElementById(id);
        if (el) {
            el.textContent = value.toFixed(1) + '%';
            el.className = el.className.replace(/text-(success|warning|error|primary|info)-600/g, '').trim();
            if (colorClass) el.classList.add(colorClass);
        }
    }
    // Helper to fetch and set
    function fetchAndSet(url, id, colorClass) {
        fetch(url)
            .then(r => r.json())
            .then(data => {
                const key = Object.keys(data)[0];
                setSentimentValue(id, data[key], colorClass);
            })
            .catch(() => setSentimentValue(id, 0, colorClass));
    }
    fetchAndSet('../public/avg_negative_sentiment_A.json', 'avg-negative-sentiment', 'text-error-600');
    fetchAndSet('../public/avg_positive_sentiment_A.json', 'avg-positive-sentiment', 'text-success-600');
    fetchAndSet('../public/avg_neutral_sentiment_A.json', 'avg-neutral-sentiment', 'text-warning-600');
});