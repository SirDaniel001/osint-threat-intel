// Threat Type Pie Chart
const typeChart = new Chart(document.getElementById('typeChart'), {
    type: 'doughnut',
    data: {
        labels: ['Ransomware', 'Malware', 'Phishing', 'Fraud'],
        datasets: [{
            data: [25, 20, 15, 10], // Replace with your backend values
            backgroundColor: ['#FF4D4D', '#FFD700', '#007bff', '#4CAF50']
        }]
    }
});

// Analytics Pie Chart
const analyticsChart = new Chart(document.getElementById('analyticsChart'), {
    type: 'pie',
    data: {
        labels: ['Ransomware', 'Malware', 'Phishing', 'Fraud'],
        datasets: [{
            data: [25, 20, 15, 10], // Replace with your backend values
            backgroundColor: ['#FF4D4D', '#FFD700', '#007bff', '#4CAF50']
        }]
    }
});

// Threats Per Day Line Chart
const trendChart = new Chart(document.getElementById('trendChart'), {
    type: 'line',
    data: {
        labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        datasets: [{
            label: 'Threats Per Day',
            data: [5, 7, 6, 10, 8, 9, 12], // Replace with your backend values
            borderColor: '#0A2647',
            backgroundColor: 'rgba(10,38,71,0.1)',
            fill: true,
            tension: 0.4
        }]
    }
});
