// Theme management
document.addEventListener('DOMContentLoaded', () => {
    const themeSwitch = document.getElementById('themeSwitch');
    const htmlElement = document.documentElement;
    
    // Check saved theme preference
    const savedTheme = localStorage.getItem('theme') || 'dark';
    htmlElement.setAttribute('data-bs-theme', savedTheme);
    themeSwitch.checked = savedTheme === 'dark';
    
    // Handle theme switching
    themeSwitch.addEventListener('change', () => {
        const newTheme = themeSwitch.checked ? 'dark' : 'light';
        htmlElement.setAttribute('data-bs-theme', newTheme);
        localStorage.setItem('theme', newTheme);
    });
});

// Common utility functions and event handlers

// Show loading spinner
const showLoading = (elementId) => {
    const element = document.getElementById(elementId);
    if (element) {
        element.querySelector('.spinner-border')?.classList.remove('d-none');
    }
};

// Hide loading spinner 
const hideLoading = (elementId) => {
    const element = document.getElementById(elementId);
    if (element) {
        element.querySelector('.spinner-border')?.classList.add('d-none');
    }
};

// Display error messages
const showError = (message) => {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-danger alert-dismissible fade show';
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.querySelector('.container').insertBefore(alertDiv, document.querySelector('.container').firstChild);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
};

// Display success messages
const showSuccess = (message) => {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-success alert-dismissible fade show';
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.querySelector('.container').insertBefore(alertDiv, document.querySelector('.container').firstChild);
    
    // Auto-dismiss after 3 seconds
    setTimeout(() => {
        alertDiv.remove();
    }, 3000);
};

// Format date strings
const formatDate = (dateString) => {
    const options = { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    return new Date(dateString).toLocaleDateString('en-US', options);
};

// Validate file size and type
const validateFile = (file, allowedTypes, maxSize) => {
    if (!file) return false;
    
    // Check file type
    if (!allowedTypes.includes(file.type)) {
        showError(`Invalid file type. Allowed types: ${allowedTypes.join(', ')}`);
        return false;
    }
    
    // Check file size (in MB)
    if (file.size > maxSize * 1024 * 1024) {
        showError(`File size must be less than ${maxSize}MB`);
        return false;
    }
    
    return true;
};

// Handle API errors
const handleApiError = (error) => {
    console.error('API Error:', error);
    showError(error.message || 'An error occurred. Please try again.');
};

// Format confidence scores
const formatConfidence = (score) => {
    return (score * 100).toFixed(1) + '%';
};

// Initialize tooltips
document.addEventListener('DOMContentLoaded', () => {
    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltips.forEach(tooltip => {
        new bootstrap.Tooltip(tooltip);
    });
});

// Export common utilities
window.appUtils = {
    showLoading,
    hideLoading,
    showError,
    showSuccess,
    formatDate,
    validateFile,
    handleApiError,
    formatConfidence
};
