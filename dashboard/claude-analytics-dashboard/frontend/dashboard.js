/**
 * ABOUTME: Frontend JavaScript for Claude Code Analytics Dashboard.
 * ABOUTME: Handles real-time data visualization, WebSocket connections, and chart rendering.
 */

class AnalyticsDashboard {
    constructor() {
        this.websocket = null;
        this.charts = {};
        this.data = null;
        this.isConnected = false;
        
        this.initializeWebSocket();
        this.initializeCharts();
        this.setupEventListeners();
        
        // Fallback: fetch data every 30 seconds if WebSocket fails
        this.fallbackInterval = setInterval(() => {
            if (!this.isConnected) {
                this.fetchAnalyticsData();
            }
        }, 30000);
    }
    
    initializeWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws`;
        
        try {
            this.websocket = new WebSocket(wsUrl);
            
            this.websocket.onopen = () => {
                console.log('WebSocket connected');
                this.updateConnectionStatus(true);
                this.isConnected = true;
            };
            
            this.websocket.onmessage = (event) => {
                const message = JSON.parse(event.data);
                if (message.type === 'initial_data' || message.type === 'data_update') {
                    this.updateDashboard(message.data);
                }
            };
            
            this.websocket.onclose = () => {
                console.log('WebSocket disconnected');
                this.updateConnectionStatus(false);
                this.isConnected = false;
                
                // Attempt to reconnect after 5 seconds
                setTimeout(() => {
                    this.initializeWebSocket();
                }, 5000);
            };
            
            this.websocket.onerror = (error) => {
                console.error('WebSocket error:', error);
                this.updateConnectionStatus(false);
                this.isConnected = false;
            };
        } catch (error) {
            console.error('Failed to create WebSocket connection:', error);
            this.updateConnectionStatus(false);
            this.fetchAnalyticsData(); // Fall back to HTTP
        }
    }
    
    updateConnectionStatus(connected) {
        const statusDot = document.getElementById('connectionStatus');
        const statusText = document.getElementById('connectionText');
        
        if (connected) {
            statusDot.classList.add('connected');
            statusText.textContent = 'Connected (Live Updates)';
        } else {
            statusDot.classList.remove('connected');
            statusText.textContent = 'Disconnected (Polling Mode)';
        }
    }
    
    async fetchAnalyticsData() {
        try {
            const response = await fetch('/api/analytics');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            this.updateDashboard(data);
        } catch (error) {
            console.error('Error fetching analytics data:', error);
            this.showError('Failed to load analytics data');
        }
    }
    
    initializeCharts() {
        // Session activity chart
        const sessionCtx = document.getElementById('sessionChart').getContext('2d');
        this.charts.session = new Chart(sessionCtx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Sessions',
                    data: [],
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
        
        // Tool usage chart
        const toolCtx = document.getElementById('toolChart').getContext('2d');
        this.charts.tool = new Chart(toolCtx, {
            type: 'doughnut',
            data: {
                labels: [],
                datasets: [{
                    data: [],
                    backgroundColor: [
                        '#3b82f6', '#ef4444', '#10b981', '#f59e0b',
                        '#8b5cf6', '#06b6d4', '#f97316', '#84cc16'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
        
        // Error rates chart
        const errorCtx = document.getElementById('errorChart').getContext('2d');
        this.charts.error = new Chart(errorCtx, {
            type: 'bar',
            data: {
                labels: [],
                datasets: [{
                    label: 'Errors',
                    data: [],
                    backgroundColor: '#ef4444',
                    borderColor: '#dc2626',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
        
        // Performance chart
        const performanceCtx = document.getElementById('performanceChart').getContext('2d');
        this.charts.performance = new Chart(performanceCtx, {
            type: 'bar',
            data: {
                labels: ['Mean', 'Median', 'P95', 'P99'],
                datasets: [{
                    label: 'Tool Execution Time (s)',
                    data: [0, 0, 0, 0],
                    backgroundColor: '#10b981',
                    borderColor: '#059669',
                    borderWidth: 1
                }, {
                    label: 'Response Time (s)',
                    data: [0, 0, 0, 0],
                    backgroundColor: '#8b5cf6',
                    borderColor: '#7c3aed',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
    
    updateDashboard(data) {
        if (!data) return;
        
        this.data = data;
        this.updateSummaryCards(data);
        this.updateCharts(data);
        this.updateRecentToolsTable(data);
    }
    
    updateSummaryCards(data) {
        const summary = data.summary || {};
        
        document.getElementById('totalSessions').textContent = summary.total_sessions || 0;
        document.getElementById('totalTools').textContent = summary.total_tools_used || 0;
        document.getElementById('totalErrors').textContent = summary.total_errors || 0;
        
        const avgDuration = summary.avg_session_duration || 0;
        document.getElementById('avgDuration').textContent = avgDuration.toFixed(1);
    }
    
    updateCharts(data) {
        this.updateSessionChart(data);
        this.updateToolChart(data);
        this.updateErrorChart(data);
        this.updatePerformanceChart(data);
    }
    
    updateSessionChart(data) {
        const sessions = data.sessions || {};
        const sessionsByHour = {};
        
        // Group sessions by hour
        Object.values(sessions).forEach(session => {
            if (session.start_time) {
                try {
                    const date = new Date(session.start_time);
                    const hourKey = date.toISOString().slice(0, 13) + ':00';
                    sessionsByHour[hourKey] = (sessionsByHour[hourKey] || 0) + 1;
                } catch (e) {
                    console.warn('Invalid session timestamp:', session.start_time);
                }
            }
        });
        
        // Sort by time and get last 24 hours
        const sortedHours = Object.keys(sessionsByHour).sort().slice(-24);
        const counts = sortedHours.map(hour => sessionsByHour[hour] || 0);
        const labels = sortedHours.map(hour => new Date(hour).toLocaleTimeString([], {hour: '2-digit', minute: '2-digit'}));
        
        this.charts.session.data.labels = labels;
        this.charts.session.data.datasets[0].data = counts;
        this.charts.session.update();
    }
    
    updateToolChart(data) {
        const tools = data.tools || {};
        const toolUsage = Object.entries(tools)
            .sort((a, b) => b[1].usage_count - a[1].usage_count)
            .slice(0, 8); // Top 8 tools
        
        const labels = toolUsage.map(([tool, _]) => tool);
        const counts = toolUsage.map(([_, stats]) => stats.usage_count);
        
        this.charts.tool.data.labels = labels;
        this.charts.tool.data.datasets[0].data = counts;
        this.charts.tool.update();
    }
    
    updateErrorChart(data) {
        const errors = data.errors || {};
        const errorsByTool = errors.errors_by_tool || {};
        
        const labels = Object.keys(errorsByTool);
        const counts = Object.values(errorsByTool);
        
        this.charts.error.data.labels = labels;
        this.charts.error.data.datasets[0].data = counts;
        this.charts.error.update();
    }
    
    updatePerformanceChart(data) {
        const performance = data.performance || {};
        const toolExec = performance.tool_execution || {};
        const responseTime = performance.response_times || {};
        
        const toolData = [
            toolExec.mean || 0,
            toolExec.median || 0,
            toolExec.p95 || 0,
            toolExec.p99 || 0
        ];
        
        const responseData = [
            responseTime.mean || 0,
            responseTime.median || 0,
            responseTime.p95 || 0,
            responseTime.p99 || 0
        ];
        
        this.charts.performance.data.datasets[0].data = toolData;
        this.charts.performance.data.datasets[1].data = responseData;
        this.charts.performance.update();
    }
    
    updateRecentToolsTable(data) {
        const tbody = document.getElementById('recentToolsTable');
        const tools = data.tools || {};
        
        // Collect all recent tool uses
        const recentTools = [];
        Object.entries(tools).forEach(([toolName, stats]) => {
            if (stats.recent_usage) {
                stats.recent_usage.forEach(usage => {
                    recentTools.push({
                        tool_name: toolName,
                        ...usage
                    });
                });
            }
        });
        
        // Sort by timestamp (most recent first)
        recentTools.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
        
        // Take top 20
        const topRecent = recentTools.slice(0, 20);
        
        if (topRecent.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="loading">No recent tool usage</td></tr>';
            return;
        }
        
        tbody.innerHTML = topRecent.map(tool => `
            <tr ${!tool.success ? 'class="error-row"' : ''}>
                <td><strong>${tool.tool_name}</strong></td>
                <td>
                    <span class="${tool.success ? 'success-badge' : 'error-badge'}">
                        ${tool.success ? 'Success' : 'Error'}
                    </span>
                </td>
                <td>${tool.execution_time.toFixed(2)}s</td>
                <td class="timestamp">${tool.session_id}</td>
                <td class="timestamp">${this.formatTimestamp(tool.timestamp)}</td>
            </tr>
        `).join('');
    }
    
    formatTimestamp(timestamp) {
        if (!timestamp) return 'Unknown';
        
        try {
            const date = new Date(timestamp);
            return date.toLocaleString();
        } catch (e) {
            return timestamp;
        }
    }
    
    showError(message) {
        const container = document.querySelector('.container');
        const existingError = container.querySelector('.error');
        
        if (existingError) {
            existingError.remove();
        }
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error';
        errorDiv.textContent = message;
        container.insertBefore(errorDiv, container.firstChild);
        
        // Remove error after 5 seconds
        setTimeout(() => {
            errorDiv.remove();
        }, 5000);
    }
    
    setupEventListeners() {
        // Refresh button (could be added to header)
        document.addEventListener('keydown', (e) => {
            if (e.key === 'r' && (e.ctrlKey || e.metaKey)) {
                e.preventDefault();
                this.fetchAnalyticsData();
            }
        });
        
        // Handle visibility change to pause/resume updates
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                if (this.websocket) {
                    this.websocket.close();
                }
            } else {
                if (!this.websocket || this.websocket.readyState === WebSocket.CLOSED) {
                    this.initializeWebSocket();
                }
            }
        });
    }
    
    destroy() {
        if (this.websocket) {
            this.websocket.close();
        }
        
        if (this.fallbackInterval) {
            clearInterval(this.fallbackInterval);
        }
        
        Object.values(this.charts).forEach(chart => {
            chart.destroy();
        });
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.dashboard = new AnalyticsDashboard();
});

// Clean up on page unload
window.addEventListener('beforeunload', () => {
    if (window.dashboard) {
        window.dashboard.destroy();
    }
});