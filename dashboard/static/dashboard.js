let gpuChart = null;
let tempChart = null;

async function fetchHistory() {
    const res = await fetch('/history?limit=500');
    return await res.json();
}

function formatTimestamp(ts) {
    // Convert "2025-11-28T11:58:33.863445" → "11:58:33"
    return ts.split("T")[1].slice(0, 8);
}

function renderCards(latest) {
    document.getElementById('metricCards').innerHTML = `
        <div class="col-md-4 mb-3">
            <div class="card bg-secondary p-3 text-center">
                <h5>GPU Utilization</h5>
                <h2>${latest.gpu_util}%</h2>
            </div>
        </div>

        <div class="col-md-4 mb-3">
            <div class="card bg-secondary p-3 text-center">
                <h5>Memory Used</h5>
                <h2>${(latest.mem_used / 1024 / 1024).toFixed(1)} MB</h2>
            </div>
        </div>

        <div class="col-md-4 mb-3">
            <div class="card bg-secondary p-3 text-center">
                <h5>Temperature</h5>
                <h2>${latest.temperature}°C</h2>
            </div>
        </div>
    `;
}

function renderGpuChart(labels, gpuUtil) {
    const ctx = document.getElementById('gpuUtilChart').getContext('2d');

    if (gpuChart) gpuChart.destroy();

    gpuChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels.map(formatTimestamp),
            datasets: [{
                label: 'GPU Util (%)',
                data: gpuUtil,
                borderColor: 'rgba(0,150,255,0.9)',
                backgroundColor: 'rgba(0,150,255,0.2)',
                fill: false,
                tension: 0.35
            }]
        },
        options: {
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false // hides box
                }
            },
            layout: {
                padding: { left: 20, right: 20, top: 10, bottom: 10 }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Time',
                        color: '#ccc',
                        font: { size: 16}
                    },
                    ticks: {
                        color: '#aaa',
                        font: { size: 14 },
                        maxTicksLimit: 6
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: '%',
                        color: '#ccc',
                        font: { size: 16 }
                    },
                    ticks: { 
                        color: '#aaa',
                        font: { size: 14 } 

                    }
                }
            }
        }
    });
}

function renderTempChart(labels, temps) {
    const ctx = document.getElementById('tempChart').getContext('2d');

     if (tempChart) tempChart.destroy();

     tempChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels.map(formatTimestamp),
            datasets: [{
                label: 'Temperature (°C)',
                data: temps,
                borderColor: 'rgba(255,120,60,0.9)',
                backgroundColor: 'rgba(255,120,60,0.2)',
                fill: false,
                tension: 0.35
            }]
        },
        options: {
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false // hides box
                }
            },
            layout: {
                padding: { left: 20, right: 20, top: 10, bottom: 10 }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Time',
                        color: '#ccc',
                        font: { size: 16 }
                    },
                    ticks: {
                        color: '#aaa',
                        font: { size: 14 },
                        maxTicksLimit: 6
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: '°C',
                        color: '#ccc',
                        font: { size: 16 }
                    },
                    ticks: { 
                        color: '#aaa',
                        font: { size: 14 } 
                    }
                }
            }
        }
    });
}

async function loadDashboard() {
    const data = await fetchHistory();
    if (data.length === 0) return;

    const labels = data.map(x => x.ts);
    const gpuUtil = data.map(x => x.gpu_util);
    const temps = data.map(x => x.temperature);

    renderCards(data[data.length - 1]);
    renderGpuChart(labels, gpuUtil);
    renderTempChart(labels, temps);
}

// Initial load
loadDashboard();

// Auto-refresh every 30 seconds
setInterval(loadDashboard, 30000);
