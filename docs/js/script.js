// Initialize date inputs with default values
document.addEventListener('DOMContentLoaded', function() {
    // Set default dates (30 days ago to today)
    const today = new Date();
    const thirtyDaysAgo = new Date();
    thirtyDaysAgo.setDate(today.getDate() - 30);
    
    document.getElementById('start_date').valueAsDate = thirtyDaysAgo;
    document.getElementById('end_date').valueAsDate = today;
    
    // Initialize event listeners
    setupEventListeners();
});

function setupEventListeners() {
    // Form submission
    document.getElementById('scrape-form').addEventListener('submit', function(e) {
        e.preventDefault();
        const ticker = document.getElementById('ticker').value.toUpperCase();
        
        // Check if we have demo data for this ticker
        if (demoStockData[ticker]) {
            showResultsWithDemoData(ticker);
        } else {
            // Show message for unsupported tickers in demo mode
            showAlert(`Demo mode only supports AAPL, MSFT, and GOOG. You entered: ${ticker}`, 'warning');
        }
    });
    
    // View toggle buttons
    document.getElementById('chart-view-btn').addEventListener('click', function() {
        showChartView();
    });
    
    document.getElementById('table-view-btn').addEventListener('click', function() {
        showTableView();
    });
    
    // Download button (demo only)
    document.getElementById('download-btn').addEventListener('click', function() {
        showAlert('Download functionality requires the full application with Python backend.', 'info');
    });
}

function showResultsWithDemoData(ticker) {
    const data = demoStockData[ticker];
    
    // Show results container
    document.getElementById('results-container').classList.remove('hidden');
    
    // Initialize DataTable
    createDataTable(ticker, data);
    
    // Initialize Chart
    createStockChart(ticker, data);
    
    // Default to table view
    showTableView();
    
    // Scroll to results
    document.getElementById('results-container').scrollIntoView({ behavior: 'smooth' });
}

function createDataTable(ticker, data) {
    // Create table rows
    const tableData = [];
    
    for (let i = 0; i < data.dates.length; i++) {
        tableData.push([
            data.dates[i],
            data.open[i].toFixed(2),
            data.high[i].toFixed(2),
            data.low[i].toFixed(2),
            data.close[i].toFixed(2),
            data.adjClose[i].toFixed(2),
            data.volume[i].toLocaleString()
        ]);
    }
    
    // Destroy existing table if it exists
    if ($.fn.DataTable.isDataTable('#stockTable')) {
        $('#stockTable').DataTable().destroy();
    }
    
    // Initialize DataTable
    $('#stockTable').DataTable({
        data: tableData,
        order: [[0, 'desc']], // Sort by date descending
        pageLength: 10,
        lengthMenu: [[10, 20, 50, 100, 250, 500, -1], [10, 20, 50, 100, 250, 500, "All"]],
        responsive: true
    });
}

function createStockChart(ticker, data) {
    const ctx = document.getElementById('stockChart').getContext('2d');
    
    // Destroy existing chart if it exists
    if (window.stockChart) {
        window.stockChart.destroy();
    }
    
    // Create new chart
    window.stockChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.dates,
            datasets: [{
                label: 'Close Price',
                data: data.close,
                borderColor: '#0d6efd',
                backgroundColor: 'rgba(13, 110, 253, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.1
            }, {
                label: 'Open Price',
                data: data.open,
                borderColor: '#20c997',
                borderWidth: 2,
                fill: false,
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: `${ticker} Stock Price History`,
                    font: { size: 16 }
                },
                tooltip: {
                    mode: 'index',
                    intersect: false
                },
                legend: {
                    position: 'top'
                }
            },
            scales: {
                x: {
                    ticks: {
                        maxRotation: 45,
                        minRotation: 45
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Price ($)'
                    }
                }
            }
        }
    });
}

function showChartView() {
    document.getElementById('chart-view').classList.remove('hidden');
    document.getElementById('table-view').classList.add('hidden');
    document.getElementById('chart-view-btn').classList.add('active');
    document.getElementById('table-view-btn').classList.remove('active');
}

function showTableView() {
    document.getElementById('chart-view').classList.add('hidden');
    document.getElementById('table-view').classList.remove('hidden');
    document.getElementById('chart-view-btn').classList.remove('active');
    document.getElementById('table-view-btn').classList.add('active');
}

function showAlert(message, type = 'info') {
    // Create alert element
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    // Add to page
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    // Auto dismiss after 5 seconds
    setTimeout(() => {
        const bsAlert = new bootstrap.Alert(alertDiv);
        bsAlert.close();
    }, 5000);
}