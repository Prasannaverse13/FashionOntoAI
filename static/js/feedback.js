// Feedback system functionality

document.addEventListener('DOMContentLoaded', () => {
    loadRecentExtractions();
    initializeFeedbackChart();
});

// Load recent extractions
async function loadRecentExtractions() {
    try {
        showLoading('extractionsTable');
        const response = await fetch('/api/extractions/recent');
        const data = await response.json();
        
        renderExtractionTable(data);
        hideLoading('extractionsTable');
    } catch (error) {
        hideLoading('extractionsTable');
        handleApiError(error);
    }
}

// Render extraction table
function renderExtractionTable(extractions) {
    const tbody = document.getElementById('extractionsTable');
    tbody.innerHTML = extractions.length ? 
        extractions.map(extraction => `
            <tr>
                <td>${extraction.product_id}</td>
                <td>${extraction.feature_name}</td>
                <td>${extraction.feature_value}</td>
                <td>${appUtils.formatConfidence(extraction.confidence_score)}</td>
                <td>
                    <button class="btn btn-sm btn-primary" 
                            onclick="openFeedbackModal(${extraction.id})">
                        Provide Feedback
                    </button>
                </td>
            </tr>
        `).join('') :
        '<tr><td colspan="5" class="text-center">No recent extractions</td></tr>';
}

// Initialize feedback chart
function initializeFeedbackChart() {
    const ctx = document.getElementById('feedbackChart').getContext('2d');
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Correct', 'Needs Correction', 'Missing Features'],
            datasets: [{
                data: [70, 20, 10],
                backgroundColor: [
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)'
                ],
                borderColor: [
                    'rgba(75, 192, 192, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

// Open feedback modal
async function openFeedbackModal(featureId) {
    try {
        const response = await fetch(`/api/features/${featureId}`);
        const feature = await response.json();
        
        document.getElementById('featureId').value = feature.id;
        document.getElementById('currentValue').value = feature.feature_value;
        
        const modal = new bootstrap.Modal(document.getElementById('feedbackModal'));
        modal.show();
    } catch (error) {
        handleApiError(error);
    }
}

// Submit feedback
async function submitFeedback() {
    const featureId = document.getElementById('featureId').value;
    const correctedValue = document.getElementById('correctedValue').value;
    const feedbackType = document.getElementById('feedbackType').value;
    const comments = document.getElementById('feedbackComments').value;
    
    if (!correctedValue) {
        appUtils.showError('Please provide a corrected value');
        return;
    }
    
    try {
        const response = await fetch('/api/feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                feature_id: featureId,
                corrected_value: correctedValue,
                feedback_type: feedbackType,
                comments: comments
            })
        });
        
        if (response.ok) {
            bootstrap.Modal.getInstance(document.getElementById('feedbackModal')).hide();
            appUtils.showSuccess('Feedback submitted successfully');
            loadRecentExtractions();  // Reload the table
        } else {
            throw new Error('Failed to submit feedback');
        }
    } catch (error) {
        handleApiError(error);
    }
}
