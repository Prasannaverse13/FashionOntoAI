// Feature extraction functionality

// Initialize extraction page
document.addEventListener('DOMContentLoaded', () => {
    initializeFileUploads();
});

// Initialize file upload handlers
function initializeFileUploads() {
    const imageFile = document.getElementById('imageFile');
    const uploadForm = document.getElementById('uploadForm');
    
    imageFile.addEventListener('change', handleImagePreview);
    uploadForm.addEventListener('submit', handleExtraction);
}

// Update preview details
function updatePreviewDetails(category) {
    const previewDetails = document.getElementById('previewDetails');
    if (category) {
        previewDetails.innerHTML = `
            <h5 class="text-center">Selected Category: ${category}</h5>
        `;
    } else {
        previewDetails.innerHTML = `
            <p class="text-muted text-center">Select a category and upload an image to begin</p>
        `;
    }
}

// Handle image preview
function handleImagePreview(event) {
    const file = event.target.files[0];
    if (!validateFile(file, ['image/jpeg', 'image/png', 'image/webp'], 5)) return;
    
    const reader = new FileReader();
    reader.onload = function(e) {
        const previewImage = document.getElementById('previewImage');
        const noPreview = document.getElementById('noPreview');
        
        previewImage.src = e.target.result;
        previewImage.classList.remove('d-none');
        noPreview.classList.add('d-none');
    };
    reader.readAsDataURL(file);
}

// Handle feature extraction
async function handleExtraction(event) {
    event.preventDefault();
    
    const imageFile = document.getElementById('imageFile').files[0];
    if (!imageFile) {
        showError('Please select an image file');
        return;
    }
    
    const category = document.getElementById('categorySelect').value;
    if (!category) {
        showError('Please select a category');
        return;
    }
    
    const formData = new FormData();
    formData.append('image_file', imageFile);
    formData.append('category', category);
    
    try {
        showLoading('extractionResults');
        
        const response = await fetch('/api/extract', {
            method: 'POST',
            body: formData
        });
        
        const results = await response.json();
        renderExtractionResults(results);
        
        hideLoading('extractionResults');
        showSuccess('Feature extraction completed');
    } catch (error) {
        hideLoading('extractionResults');
        handleApiError(error);
    }
}

// Render extraction results
function renderExtractionResults(results) {
    const resultsTable = document.getElementById('resultsTable');
    
    let html = '';
    results.features.forEach(feature => {
        html += `
            <tr>
                <td>${feature.name}</td>
                <td>${feature.value}</td>
                <td>${formatConfidence(feature.confidence)}</td>
                <td>
                    <button class="btn btn-sm btn-outline-primary me-1" 
                            onclick="editFeature(${feature.id})">
                        Edit
                    </button>
                    <button class="btn btn-sm btn-outline-secondary"
                            onclick="submitFeedback(${feature.id})">
                        Feedback
                    </button>
                </td>
            </tr>
        `;
    });
    
    resultsTable.innerHTML = html;
}

// Edit extracted feature
async function editFeature(featureId) {
    try {
        const response = await fetch(`/api/features/${featureId}`);
        const feature = await response.json();
        
        // Show edit modal (implement as needed)
        console.log('Edit feature:', feature);
    } catch (error) {
        handleApiError(error);
    }
}

// Submit feedback for a feature
async function submitFeedback(featureId) {
    try {
        // Redirect to feedback page with feature ID
        window.location.href = `/feedback?feature=${featureId}`;
    } catch (error) {
        handleApiError(error);
    }
}
