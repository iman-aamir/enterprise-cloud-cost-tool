
// Define the API endpoints
const API_ENDPOINTS = {
    connectOracle: '/api/connect/oracle',
    connectAzure: '/api/connect/azure',
    analyze: '/api/analyze',
    getRecommendations: '/api/recommendations',
    forecast: '/api/forecast'
};

// Define the result containers
const RESULT_CONTAINERS = {
    analysis: document.getElementById('analysis-results'),
    recommendations: document.getElementById('recommendations-results'),
    forecast: document.getElementById('forecast-results')
};

// Function to handle API responses
function handleResponse(response, container) {
    if (response.ok) {
        response.json().then(data => {
            container.innerHTML = JSON.stringify(data, null, 2);
        });
    } else {
        container.innerHTML = 'Error: ' + response.status;
    }
}

// Function to handle API errors
function handleError(error, container) {
    container.innerHTML = 'Error: ' + error;
}

// Function to connect to Oracle Cloud
document.getElementById('connect-oracle').addEventListener('click', () => {
    fetch(API_ENDPOINTS.connectOracle)
        .then(response => handleResponse(response, RESULT_CONTAINERS.analysis))
        .catch(error => handleError(error, RESULT_CONTAINERS.analysis));
});

// Function to connect to Azure
document.getElementById('connect-azure').addEventListener('click', () => {
    fetch(API_ENDPOINTS.connectAzure)
        .then(response => handleResponse(response, RESULT_CONTAINERS.analysis))
        .catch(error => handleError(error, RESULT_CONTAINERS.analysis));
});

// Function to analyze cloud usage
document.getElementById('analyze').addEventListener('click', () => {
    fetch(API_ENDPOINTS.analyze)
        .then(response => handleResponse(response, RESULT_CONTAINERS.analysis))
        .catch(error => handleError(error, RESULT_CONTAINERS.analysis));
});

// Function to get recommendations
document.getElementById('get-recommendations').addEventListener('click', () => {
    fetch(API_ENDPOINTS.getRecommendations)
        .then(response => handleResponse(response, RESULT_CONTAINERS.recommendations))
        .catch(error => handleError(error, RESULT_CONTAINERS.recommendations));
});

// Function to forecast future expenses
document.getElementById('forecast').addEventListener('click', () => {
    fetch(API_ENDPOINTS.forecast)
        .then(response => handleResponse(response, RESULT_CONTAINERS.forecast))
        .catch(error => handleError(error, RESULT_CONTAINERS.forecast));
});

