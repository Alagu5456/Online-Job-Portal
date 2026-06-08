// Main JavaScript file for JobPortal
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

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert-dismissible');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Form validation enhancement
    var forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // File upload validation
    var fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(function(input) {
        input.addEventListener('change', function(e) {
            var file = e.target.files[0];
            var feedback = input.parentNode.querySelector('.invalid-feedback') || 
                          input.parentNode.querySelector('.form-text');
            
            if (file) {
                // Check file size (16MB limit)
                if (file.size > 16 * 1024 * 1024) {
                    input.setCustomValidity('File size must be less than 16MB');
                    if (feedback) {
                        feedback.textContent = 'File size must be less than 16MB';
                        feedback.classList.add('text-danger');
                    }
                } else if (file.type !== 'application/pdf') {
                    input.setCustomValidity('Only PDF files are allowed');
                    if (feedback) {
                        feedback.textContent = 'Only PDF files are allowed';
                        feedback.classList.add('text-danger');
                    }
                } else {
                    input.setCustomValidity('');
                    if (feedback) {
                        feedback.textContent = 'File looks good!';
                        feedback.classList.remove('text-danger');
                        feedback.classList.add('text-success');
                    }
                }
            }
        });
    });

    // Search form enhancements
    var searchForm = document.querySelector('form[method="GET"]');
    if (searchForm) {
        // Add loading state to search button
        searchForm.addEventListener('submit', function() {
            var submitBtn = searchForm.querySelector('button[type="submit"]');
            if (submitBtn) {
                var originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Searching...';
                submitBtn.disabled = true;
                
                // Re-enable after 3 seconds as fallback
                setTimeout(function() {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }, 3000);
            }
        });
    }

    // Smooth scroll for anchor links
    var anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            var target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Confirmation dialogs for dangerous actions
    var dangerousActions = document.querySelectorAll('[onclick*="confirm"]');
    dangerousActions.forEach(function(element) {
        element.addEventListener('click', function(e) {
            var confirmed = confirm(this.getAttribute('onclick').match(/confirm\('([^']+)'\)/)[1]);
            if (!confirmed) {
                e.preventDefault();
            }
        });
    });

    // Auto-refresh application status (for demo purposes)
    if (window.location.pathname.includes('dashboard') || 
        window.location.pathname.includes('my-applications')) {
        
        // Add subtle animation to status badges
        var statusBadges = document.querySelectorAll('.badge');
        statusBadges.forEach(function(badge) {
            if (badge.textContent.trim() === 'Pending') {
                badge.style.animation = 'pulse 2s infinite';
            }
        });
    }

    // Character counter for textareas
    var textareas = document.querySelectorAll('textarea');
    textareas.forEach(function(textarea) {
        var maxLength = textarea.getAttribute('maxlength');
        if (maxLength) {
            var counter = document.createElement('small');
            counter.className = 'form-text text-muted';
            counter.textContent = '0 / ' + maxLength + ' characters';
            textarea.parentNode.appendChild(counter);
            
            textarea.addEventListener('input', function() {
                var current = textarea.value.length;
                counter.textContent = current + ' / ' + maxLength + ' characters';
                
                if (current > maxLength * 0.9) {
                    counter.classList.add('text-warning');
                } else {
                    counter.classList.remove('text-warning');
                }
            });
        }
    });

    // Add fade-in animation to cards
    var cards = document.querySelectorAll('.card');
    cards.forEach(function(card, index) {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(function() {
            card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });

    // Table row click handlers
    var tableRows = document.querySelectorAll('table tbody tr');
    tableRows.forEach(function(row) {
        var viewLink = row.querySelector('a[href*="job_detail"]') || 
                      row.querySelector('a[href*="review_application"]');
        if (viewLink) {
            row.style.cursor = 'pointer';
            row.addEventListener('click', function(e) {
                // Don't trigger if clicking on actual links or buttons
                if (e.target.tagName !== 'A' && e.target.tagName !== 'BUTTON' && 
                    !e.target.closest('a') && !e.target.closest('button')) {
                    window.location.href = viewLink.href;
                }
            });
        }
    });

    // Statistics counter animation
    var statNumbers = document.querySelectorAll('.card h3');
    statNumbers.forEach(function(element) {
        var finalNumber = parseInt(element.textContent);
        if (!isNaN(finalNumber) && finalNumber > 0) {
            var currentNumber = 0;
            var increment = Math.ceil(finalNumber / 20);
            var timer = setInterval(function() {
                currentNumber += increment;
                if (currentNumber >= finalNumber) {
                    currentNumber = finalNumber;
                    clearInterval(timer);
                }
                element.textContent = currentNumber;
            }, 50);
        }
    });

    // Lazy loading for job listings
    if ('IntersectionObserver' in window) {
        var jobCards = document.querySelectorAll('.card');
        var jobObserver = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                    jobObserver.unobserve(entry.target);
                }
            });
        });

        jobCards.forEach(function(card) {
            jobObserver.observe(card);
        });
    }

    // Form auto-save for long forms (like job posting)
    var longForms = document.querySelectorAll('form textarea, form input[type="text"]');
    longForms.forEach(function(input) {
        var saveKey = 'jobportal_autosave_' + input.name;
        
        // Load saved data
        var savedValue = localStorage.getItem(saveKey);
        if (savedValue && !input.value) {
            input.value = savedValue;
        }
        
        // Save data on input
        input.addEventListener('input', function() {
            localStorage.setItem(saveKey, input.value);
        });
        
        // Clear saved data on form submit
        input.form.addEventListener('submit', function() {
            localStorage.removeItem(saveKey);
        });
    });

    // Add keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + K for search focus
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            var searchInput = document.querySelector('input[name="search_term"]');
            if (searchInput) {
                searchInput.focus();
                searchInput.select();
            }
        }
        
        // Escape to close modals and clear search
        if (e.key === 'Escape') {
            var searchInput = document.querySelector('input[name="search_term"]');
            if (searchInput && document.activeElement === searchInput) {
                searchInput.value = '';
                searchInput.blur();
            }
        }
    });

    // Print-friendly styles for application review
    if (window.location.pathname.includes('review_application')) {
        var printBtn = document.createElement('button');
        printBtn.className = 'btn btn-outline-secondary btn-sm';
        printBtn.innerHTML = '<i class="fas fa-print me-1"></i>Print';
        printBtn.addEventListener('click', function() {
            window.print();
        });
        
        var cardHeader = document.querySelector('.card-header');
        if (cardHeader) {
            cardHeader.appendChild(printBtn);
        }
    }

    console.log('JobPortal JavaScript initialized successfully');
});

// Utility functions
window.JobPortal = {
    showToast: function(message, type = 'info') {
        // Create toast notification
        var toast = document.createElement('div');
        toast.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        toast.style.top = '20px';
        toast.style.right = '20px';
        toast.style.zIndex = '1050';
        toast.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(toast);
        
        // Auto-remove after 5 seconds
        setTimeout(function() {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 5000);
    },
    
    formatDate: function(dateString) {
        var date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    },
    
    copyToClipboard: function(text) {
        if (navigator.clipboard) {
            navigator.clipboard.writeText(text).then(function() {
                JobPortal.showToast('Copied to clipboard!', 'success');
            });
        } else {
            // Fallback for older browsers
            var textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            JobPortal.showToast('Copied to clipboard!', 'success');
        }
    }
};

// Add CSS animations
var style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @media print {
        .btn, .navbar, .pagination, .alert {
            display: none !important;
        }
        
        .card {
            border: 1px solid #000 !important;
            box-shadow: none !important;
        }
    }
`;
document.head.appendChild(style);
