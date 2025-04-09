document.addEventListener('DOMContentLoaded', function() {
    // Initialize Date pickers
    const startDateInput = document.getElementById('start_date');
    const endDateInput = document.getElementById('end_date');
    
    // Form validation
    const form = document.getElementById('scraper-form');
    if (form) {
        form.addEventListener('submit', function(event) {
            const ticker = document.getElementById('ticker').value.trim();
            if (!ticker) {
                event.preventDefault();
                showAlert('Please enter a ticker symbol', 'danger');
                return false;
            }
            
            // Show loading indicator
            document.getElementById('loading-indicator').classList.remove('d-none');
            document.getElementById('submit-btn').disabled = true;
            
            return true;
        });
    }
    
    // Initialize DataTable if results table exists
    const resultsTable = document.getElementById('results-table');
    if (resultsTable) {
        const dataTable = new DataTable('#results-table', {
            order: [[0, 'desc']], // Sort by date (first column) in descending order
            responsive: true,
            pageLength: 50, // Default to 50 records per page
            lengthMenu: [10, 20, 50, 100, 250, 500], // Available options for records per page
            language: {
                search: "Filter records:",
                lengthMenu: "Show _MENU_ records per page",
                zeroRecords: "No matching records found",
                info: "Showing _START_ to _END_ of _TOTAL_ records",
                infoEmpty: "Showing 0 to 0 of 0 records",
                infoFiltered: "(filtered from _MAX_ total records)"
            }
        });
    }
    
    // Initialize Chart if canvas exists
    const chartCanvas = document.getElementById('price-chart');
    if (chartCanvas) {
        createStockChart();
    }
});

function showAlert(message, type = 'info') {
    const alertContainer = document.getElementById('alert-container');
    if (!alertContainer) return;
    
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    alertContainer.appendChild(alertDiv);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        alertDiv.classList.remove('show');
        setTimeout(() => {
            alertDiv.remove();
        }, 500);
    }, 5000);
}

function createStockChart() {
    const chartCanvas = document.getElementById('price-chart');
    if (!chartCanvas) return;
    
    const labels = chartData.map(item => item.Date);
    const closeData = chartData.map(item => item.Close);
    const highData = chartData.map(item => item.High);
    const lowData = chartData.map(item => item.Low);
    
    const ctx = chartCanvas.getContext('2d');
    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Close',
                    data: closeData,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    tension: 0.1,
                    fill: false
                },
                {
                    label: 'High',
                    data: highData,
                    borderColor: 'rgba(54, 162, 235, 1)',
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    tension: 0.1,
                    fill: false,
                    hidden: true
                },
                {
                    label: 'Low',
                    data: lowData,
                    borderColor: 'rgba(255, 99, 132, 1)',
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    tension: 0.1,
                    fill: false,
                    hidden: true
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: `${ticker} Price History`,
                    font: {
                        size: 16
                    }
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed.y !== null) {
                                label += new Intl.NumberFormat('en-US', { 
                                    style: 'currency', 
                                    currency: 'USD',
                                    minimumFractionDigits: 2
                                }).format(context.parsed.y);
                            }
                            return label;
                        }
                    }
                }
            },
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Date'
                    },
                    ticks: {
                        maxTicksLimit: 10
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Price ($)'
                    }
                }
            }
        }
    });
}

function toggleDataTable() {
    const tableSection = document.getElementById('data-table-section');
    const chartSection = document.getElementById('chart-section');
    
    if (tableSection.classList.contains('d-none')) {
        tableSection.classList.remove('d-none');
        chartSection.classList.add('d-none');
        document.getElementById('toggle-view-btn').innerText = 'Show Chart';
    } else {
        tableSection.classList.add('d-none');
        chartSection.classList.remove('d-none');
        document.getElementById('toggle-view-btn').innerText = 'Show Table';
    }
}
