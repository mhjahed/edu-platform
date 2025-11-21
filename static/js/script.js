// Global JavaScript for Exam Management System

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
    const alerts = document.querySelectorAll('.alert:not(.alert-danger)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Confirm before deleting
    const deleteButtons = document.querySelectorAll('.btn-delete, [data-action="delete"]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });

    // Form validation enhancement
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

    // Auto-save form data (for drafts)
    const autoSaveForms = document.querySelectorAll('[data-auto-save]');
    autoSaveForms.forEach(form => {
        const formData = {};
        const inputs = form.querySelectorAll('input, textarea, select');
        
        inputs.forEach(input => {
            input.addEventListener('change', function() {
                formData[input.name] = input.value;
                localStorage.setItem('form_' + form.id, JSON.stringify(formData));
            });
        });

        // Load saved data on page load
        const saved = localStorage.getItem('form_' + form.id);
        if (saved) {
            const savedData = JSON.parse(saved);
            Object.keys(savedData).forEach(key => {
                const input = form.querySelector(`[name="${key}"]`);
                if (input) {
                    input.value = savedData[key];
                }
            });
        }
    });

    // Character counter for textareas
    const textareas = document.querySelectorAll('textarea[maxlength]');
    textareas.forEach(textarea => {
        const maxLength = textarea.getAttribute('maxlength');
        const counter = document.createElement('div');
        counter.className = 'text-muted small mt-1';
        counter.textContent = `0/${maxLength} characters`;
        textarea.parentNode.appendChild(counter);

        textarea.addEventListener('input', function() {
            const currentLength = textarea.value.length;
            counter.textContent = `${currentLength}/${maxLength} characters`;
            
            if (currentLength > maxLength * 0.9) {
                counter.className = 'text-warning small mt-1';
            } else {
                counter.className = 'text-muted small mt-1';
            }
        });
    });

    // Loading states for buttons
    const loadingButtons = document.querySelectorAll('.btn[data-loading-text]');
    loadingButtons.forEach(button => {
        button.addEventListener('click', function() {
            const originalText = button.innerHTML;
            const loadingText = button.getAttribute('data-loading-text');
            
            button.innerHTML = `<span class="spinner-border spinner-border-sm me-2" role="status"></span>${loadingText}`;
            button.disabled = true;

            // Re-enable after 5 seconds (fallback)
            setTimeout(() => {
                button.innerHTML = originalText;
                button.disabled = false;
            }, 5000);
        });
    });

    // Dynamic form field additions
    const addFieldButtons = document.querySelectorAll('[data-add-field]');
    addFieldButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetContainer = document.getElementById(button.getAttribute('data-target'));
            const template = document.getElementById(button.getAttribute('data-template'));
            
            if (targetContainer && template) {
                const clone = template.content.cloneNode(true);
                targetContainer.appendChild(clone);
            }
        });
    });

    // Print functionality
    const printButtons = document.querySelectorAll('[data-action="print"]');
    printButtons.forEach(button => {
        button.addEventListener('click', function() {
            window.print();
        });
    });

});

// Exam Timer Functionality
class ExamTimer {
    constructor(endTime, element) {
        this.endTime = new Date(endTime).getTime();
        this.element = element;
        this.interval = null;
        this.warningThreshold = 5 * 60 * 1000; // 5 minutes in milliseconds
        this.start();
    }

    start() {
        this.update();
        this.interval = setInterval(() => this.update(), 1000);
    }

    update() {
        const now = new Date().getTime();
        const timeLeft = this.endTime - now;

        if (timeLeft <= 0) {
            this.element.innerHTML = 'Time Up!';
            this.element.classList.add('text-danger');
            clearInterval(this.interval);
            this.timeUp();
            return;
        }

        // Apply warning style if less than threshold
        if (timeLeft <= this.warningThreshold) {
            this.element.classList.add('warning');
        }

        const hours = Math.floor(timeLeft / (1000 * 60 * 60));
        const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);

        this.element.innerHTML = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }

    timeUp() {
        // Auto-submit form if exists
        const examForm = document.getElementById('exam-form');
        if (examForm) {
            alert('Time is up! Your exam will be submitted automatically.');
            examForm.submit();
        }
    }

    stop() {
        clearInterval(this.interval);
    }
}

// Auto-save answers during exam
class ExamAutoSave {
    constructor(formId, saveUrl, interval = 30000) { // Save every 30 seconds
        this.form = document.getElementById(formId);
        this.saveUrl = saveUrl;
        this.interval = interval;
        this.timeoutId = null;
        this.isSubmitting = false;

        if (this.form) {
            this.init();
        }
    }

    init() {
        // Listen for changes in form inputs
        const inputs = this.form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('change', () => this.scheduleSave());
            input.addEventListener('input', () => this.scheduleSave());
        });

        // Prevent data loss on page unload
        window.addEventListener('beforeunload', (e) => {
            if (!this.isSubmitting && this.hasUnsavedChanges()) {
                e.preventDefault();
                e.returnValue = 'You have unsaved answers. Are you sure you want to leave?';
            }
        });

        // Start periodic auto-save
        this.startPeriodicSave();
    }

    scheduleSave() {
        // Clear existing timeout
        if (this.timeoutId) {
            clearTimeout(this.timeoutId);
        }

        // Schedule new save
        this.timeoutId = setTimeout(() => this.save(), 2000); // Save 2 seconds after last change
    }

    startPeriodicSave() {
        setInterval(() => this.save(), this.interval);
    }

    async save() {
        if (this.isSubmitting) return;

        try {
            const formData = new FormData(this.form);
            const response = await fetch(this.saveUrl, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                }
            });

            if (response.ok) {
                this.showSaveStatus('Answers saved automatically', 'success');
            }
        } catch (error) {
            this.showSaveStatus('Auto-save failed', 'warning');
        }
    }

    showSaveStatus(message, type = 'info') {
        const statusElement = document.getElementById('save-status');
        if (statusElement) {
            statusElement.className = `alert alert-${type} alert-dismissible fade show`;
            statusElement.innerHTML = `${message} <button type="button" class="btn-close" data-bs-dismiss="alert"></button>`;
            
            // Auto-hide after 3 seconds
            setTimeout(() => {
                const alert = new bootstrap.Alert(statusElement);
                alert.close();
            }, 3000);
        }
    }

    hasUnsavedChanges() {
        // Simple check - in a real app you'd compare with last saved state
        const inputs = this.form.querySelectorAll('input:checked, textarea, select');
        return inputs.length > 0;
    }

    setSubmitting(isSubmitting) {
        this.isSubmitting = isSubmitting;
    }
}

// Utility functions
const Utils = {
    formatDate(date) {
        return new Intl.DateTimeFormat('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        }).format(new Date(date));
    },

    formatDuration(minutes) {
        const hours = Math.floor(minutes / 60);
        const mins = minutes % 60;
        return hours > 0 ? `${hours}h ${mins}m` : `${mins}m`;
    },

    showLoading(element) {
        const originalContent = element.innerHTML;
        element.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
        element.disabled = true;
        return originalContent;
    },

    hideLoading(element, originalContent) {
        element.innerHTML = originalContent;
        element.disabled = false;
    },

    copyToClipboard(text) {
        navigator.clipboard.writeText(text).then(() => {
            this.showToast('Copied to clipboard!', 'success');
        });
    },

    showToast(message, type = 'info') {
        // Create a toast notification
        const toastContainer = document.getElementById('toast-container') || this.createToastContainer();
        const toast = this.createToast(message, type);
        toastContainer.appendChild(toast);
        
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
    },

    createToastContainer() {
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'position-fixed bottom-0 end-0 p-3';
        container.style.zIndex = '1070';
        document.body.appendChild(container);
        return container;
    },

    createToast(message, type) {
        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.innerHTML = `
            <div class="toast-header">
                <i class="fas fa-${type === 'success' ? 'check-circle text-success' : type === 'error' ? 'exclamation-circle text-danger' : 'info-circle text-info'}"></i>
                <strong class="me-auto ms-2">Notification</strong>
                <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">${message}</div>
        `;
        return toast;
    }
};