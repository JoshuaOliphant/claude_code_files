# Claude Code Analytics Dashboard

A simple, functional web-based analytics dashboard for visualizing Claude Code hook logs. Provides real-time insights into session activity, tool usage, error patterns, and performance metrics.

## Features

### 📊 Real-time Analytics
- **Session Activity**: Track session starts over time
- **Tool Usage**: Monitor which tools are used most frequently
- **Error Patterns**: Identify and analyze error trends
- **Performance Metrics**: Monitor execution times and response rates

### 🔄 Live Updates
- WebSocket connection for real-time data updates
- Automatic fallback to polling mode if WebSocket fails
- File system monitoring for instant log updates

### 📈 Visualizations
- Interactive charts using Chart.js
- Summary cards with key metrics
- Detailed tables with recent activity
- Responsive design for mobile and desktop

## Quick Start

1. **Install Dependencies**
   ```bash
   cd /workdir/dashboard/claude-analytics-dashboard
   export PATH="/root/.local/bin:$PATH"
   uv sync
   ```

2. **Start the Dashboard**
   ```bash
   uv run python run_dashboard.py
   ```

3. **Open Your Browser**
   Navigate to: `http://localhost:8000`

## Architecture

### Backend (FastAPI)
- **`backend/main.py`**: Main FastAPI application
- RESTful API endpoints (`/api/*`)
- WebSocket support for real-time updates
- File system monitoring with watchdog
- Data processing with pandas and scikit-learn

### Frontend (HTML/JS)
- **`frontend/index.html`**: Main dashboard interface
- **`frontend/dashboard.js`**: Client-side logic and charts
- Chart.js for data visualization
- WebSocket client for live updates

### Log Processing
- Reads JSON log files from `/workdir/dashboard/logs/`
- Processes session starts, tool usage, and user prompts
- Calculates metrics, trends, and performance statistics

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | Main dashboard page |
| `GET /api/analytics` | Complete analytics data |
| `GET /api/sessions` | Session-specific data |
| `GET /api/tools` | Tool usage statistics |
| `GET /api/errors` | Error analysis data |
| `GET /api/performance` | Performance metrics |
| `WS /ws` | WebSocket for real-time updates |

## Sample Data

The dashboard includes sample log files in `/workdir/dashboard/logs/sample/`:
- `session_start.json`: Session initialization events
- `post_tool_use.json`: Tool execution records
- `user_prompt_submit.json`: User interaction logs

## Configuration

### Log File Locations
The dashboard monitors these directories for log files:
- `/workdir/dashboard/logs/` (main logs)
- `/workdir/dashboard/logs/sample/` (sample data)

### Environment Variables
- `LOGS_PATH`: Override default log directory
- `PORT`: Change server port (default: 8000)

## Metrics Calculated

### Session Metrics
- Total sessions
- Session duration
- Tools used per session
- Error count per session

### Tool Metrics
- Usage frequency
- Success rates
- Average execution times
- Recent usage patterns

### Performance Metrics
- Mean, median, P95, P99 execution times
- Response time statistics
- Slowest tool operations

### Error Analysis
- Error count by tool
- Error patterns over time
- Recent error details

## Real-time Updates

The dashboard uses WebSocket connections for live updates:
1. File system watcher detects log changes
2. Server processes new data
3. Updates sent to all connected clients
4. Charts and tables refresh automatically

## Browser Compatibility

- Chrome/Chromium 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## Development

### Adding New Metrics
1. Update log processing functions in `backend/main.py`
2. Add new API endpoints if needed
3. Update frontend charts and tables in `frontend/dashboard.js`

### Customizing Visualizations
- Charts are built with Chart.js
- Modify chart configurations in `initializeCharts()`
- Add new chart types in `updateCharts()`

## Troubleshooting

### Common Issues

**Dashboard won't start:**
- Check that all dependencies are installed: `uv sync`
- Verify Python version: Python 3.11+
- Check port availability: `lsof -i :8000`

**No data showing:**
- Verify log files exist in `/workdir/dashboard/logs/`
- Check log file format (must be valid JSON)
- Look for errors in server logs

**WebSocket connection fails:**
- Dashboard falls back to polling mode automatically
- Check browser console for connection errors
- Verify firewall settings

### Logging
Server logs provide detailed information about:
- File processing errors
- WebSocket connections
- API request handling

## License

This dashboard is part of the Claude Code toolkit and follows the same licensing terms.