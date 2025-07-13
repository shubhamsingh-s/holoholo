// Holoholo E-commerce JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Search autocomplete
    initializeSearchAutocomplete();

    // Cart functionality
    initializeCart();

    // Product image lazy loading
    initializeLazyLoading();

    // Smooth scrolling for anchor links
    initializeSmoothScrolling();

    // Form validation
    initializeFormValidation();

    // Back to top button
    initializeBackToTop();
});

// Search Autocomplete
function initializeSearchAutocomplete() {
    const searchInput = document.querySelector('input[name="q"]');
    if (!searchInput) return;

    let searchTimeout;
    const suggestionsContainer = document.createElement('div');
    suggestionsContainer.className = 'search-suggestions';
    suggestionsContainer.style.cssText = `
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background: white;
        border: 1px solid #ddd;
        border-top: none;
        border-radius: 0 0 4px 4px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        z-index: 1000;
        display: none;
    `;

    searchInput.parentElement.style.position = 'relative';
    searchInput.parentElement.appendChild(suggestionsContainer);

    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        const query = this.value.trim();
        
        if (query.length < 2) {
            suggestionsContainer.style.display = 'none';
            return;
        }

        searchTimeout = setTimeout(() => {
            // Simulate search suggestions
            const suggestions = [
                query + ' products',
                query + ' category',
                'Best ' + query,
                query + ' deals'
            ];

            displaySuggestions(suggestions);
        }, 300);
    });

    searchInput.addEventListener('blur', function() {
        setTimeout(() => {
            suggestionsContainer.style.display = 'none';
        }, 200);
    });

    function displaySuggestions(suggestions) {
        suggestionsContainer.innerHTML = suggestions.map(suggestion => 
            `<div class="suggestion-item p-2 border-bottom" style="cursor: pointer;">${suggestion}</div>`
        ).join('');

        suggestionsContainer.style.display = 'block';

        // Add click handlers
        suggestionsContainer.querySelectorAll('.suggestion-item').forEach(item => {
            item.addEventListener('click', function() {
                searchInput.value = this.textContent;
                suggestionsContainer.style.display = 'none';
                searchInput.form.submit();
            });
        });
    }
}

// Cart Functionality
function initializeCart() {
    // Add to cart animation
    document.querySelectorAll('form[action*="add_to_cart"]').forEach(form => {
        form.addEventListener('submit', function(e) {
            const button = this.querySelector('button[type="submit"]');
            const originalText = button.innerHTML;
            
            button.innerHTML = '<span class="loading"></span> Adding...';
            button.disabled = true;

            // Simulate loading
            setTimeout(() => {
                button.innerHTML = originalText;
                button.disabled = false;
            }, 1000);
        });
    });

    // Cart quantity updates
    document.querySelectorAll('input[name="quantity"]').forEach(input => {
        input.addEventListener('change', function() {
            if (this.value < 1) {
                this.value = 1;
            }
        });
    });
}

// Lazy Loading for Images
function initializeLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));
}

// Smooth Scrolling
function initializeSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Form Validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Real-time validation
    document.querySelectorAll('input[required], textarea[required]').forEach(input => {
        input.addEventListener('blur', function() {
            validateField(this);
        });
    });
}

function validateField(field) {
    const value = field.value.trim();
    const isValid = field.checkValidity();
    
    if (isValid) {
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
    } else {
        field.classList.remove('is-valid');
        field.classList.add('is-invalid');
    }
}

// Back to Top Button
function initializeBackToTop() {
    const backToTopButton = document.createElement('button');
    backToTopButton.innerHTML = '<i class="fas fa-arrow-up"></i>';
    backToTopButton.className = 'btn btn-primary back-to-top';
    backToTopButton.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        display: none;
        z-index: 1000;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    `;

    document.body.appendChild(backToTopButton);

    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopButton.style.display = 'block';
        } else {
            backToTopButton.style.display = 'none';
        }
    });

    backToTopButton.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// Utility Functions
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = `
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
    `;
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    document.body.appendChild(notification);

    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Product Rating System
function initializeRatingSystem() {
    const ratingInputs = document.querySelectorAll('input[name="rating"]');
    const ratingDisplay = document.querySelector('.rating-display');
    
    ratingInputs.forEach(input => {
        input.addEventListener('change', function() {
            const rating = parseInt(this.value);
            displayStars(rating);
        });
    });

    function displayStars(rating) {
        if (!ratingDisplay) return;
        
        ratingDisplay.innerHTML = '';
        for (let i = 1; i <= 5; i++) {
            const star = document.createElement('i');
            star.className = i <= rating ? 'fas fa-star text-warning' : 'far fa-star text-warning';
            ratingDisplay.appendChild(star);
        }
    }
}

// Wishlist Functionality
function toggleWishlist(productId) {
    const wishlistButton = document.querySelector(`[data-product-id="${productId}"]`);
    const icon = wishlistButton.querySelector('i');
    
    if (icon.classList.contains('far')) {
        icon.classList.remove('far');
        icon.classList.add('fas');
        wishlistButton.classList.add('text-danger');
        showNotification('Added to wishlist!', 'success');
    } else {
        icon.classList.remove('fas');
        icon.classList.add('far');
        wishlistButton.classList.remove('text-danger');
        showNotification('Removed from wishlist!', 'info');
    }
}

// Product Quick View
function openQuickView(productId) {
    // This would typically open a modal with product details
    showNotification('Quick view functionality would be implemented here.', 'info');
}

// Share Product
function shareProduct(productId, platform) {
    const url = window.location.href;
    const title = document.title;
    
    let shareUrl;
    switch (platform) {
        case 'facebook':
            shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`;
            break;
        case 'twitter':
            shareUrl = `https://twitter.com/intent/tweet?url=${encodeURIComponent(url)}&text=${encodeURIComponent(title)}`;
            break;
        case 'email':
            shareUrl = `mailto:?subject=${encodeURIComponent(title)}&body=${encodeURIComponent(url)}`;
            break;
        default:
            return;
    }
    
    window.open(shareUrl, '_blank', 'width=600,height=400');
}

// Initialize rating system if on product page
if (document.querySelector('.rating-display')) {
    initializeRatingSystem();
}

// Export functions for global use
window.Holoholo = {
    showNotification,
    formatCurrency,
    toggleWishlist,
    openQuickView,
    shareProduct
}; 