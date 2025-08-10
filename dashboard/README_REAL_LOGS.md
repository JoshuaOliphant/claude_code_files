# Connecting Dashboard to Real Claude Code Logs

## Quick Start (Easiest Method)

Since your logs are in `/Users/joshuaoliphant/.claude/logs/` and contain uncommitted changes, here's the simplest approach:

### Option 1: Direct Copy (Immediate)

```bash
# From your terminal (outside container)
cp ~/.claude/logs/*.json ~/path/to/dashboard/logs/
```

### Option 2: Live Sync Script

Run this in your terminal to keep logs synced:

```bash
# Create a simple sync script
cat > ~/sync_claude_logs.sh << 'EOF'
#!/bin/bash
while true; do
    cp ~/.claude/logs/*.json ~/dashboard/logs/ 2>/dev/null
    echo "$(date): Logs synced"
    sleep 30
done
EOF

chmod +x ~/sync_claude_logs.sh
./sync_claude_logs.sh &
```

### Option 3: Use the Python Connector

From within the container environment:

```bash
# One-time copy
python /workdir/dashboard/connect_to_real_logs.py -s ~/.claude/logs -m copy

# Or watch for changes
python /workdir/dashboard/connect_to_real_logs.py -s ~/.claude/logs -m watch
```

## Running Dashboard Locally with Real Logs

### Step 1: Export and Run Locally

```bash
# Check out the dashboard code
container-use checkout fair-raven

# Navigate to dashboard
cd /path/to/checked-out/dashboard/claude-analytics-dashboard

# Install dependencies
pip install -r backend/requirements.txt

# Update the logs path in backend/main.py
# Change: LOGS_PATH = Path("/workdir/dashboard/logs")
# To: LOGS_PATH = Path.home() / ".claude" / "logs"

# Run the backend
cd backend
python main.py

# Open frontend in browser
open frontend/index.html
```

### Step 2: Docker Deployment (Production)

```yaml
# docker-compose.yml
version: '3.8'
services:
  dashboard:
    build: ./dashboard
    ports:
      - "8000:8000"
    volumes:
      - ~/.claude/logs:/app/logs:ro
    environment:
      - LOGS_PATH=/app/logs
```

Run with:
```bash
docker-compose up -d
```

## Configuration Options

### Environment Variables

Create `.env` file in dashboard directory:

```env
# Real logs location
LOGS_PATH=/Users/joshuaoliphant/.claude/logs

# Update interval (seconds)
UPDATE_INTERVAL=30

# Enable file watching
WATCH_LOGS=true

# WebSocket port
WS_PORT=8000
```

### Backend Configuration

Edit `/workdir/dashboard/claude-analytics-dashboard/backend/main.py`:

```python
import os
from pathlib import Path

# Read from environment or use default
LOGS_PATH = Path(os.getenv('LOGS_PATH', Path.home() / '.claude' / 'logs'))
```

## Handling Uncommitted Logs

Since your logs are uncommitted, you have two options:

1. **Commit them first** (if not sensitive):
   ```bash
   cd ~/.claude
   git add logs/
   git commit -m "Add Claude Code logs for analysis"
   ```

2. **Work with them outside Git**:
   - Copy logs to a separate directory
   - Point dashboard to that directory
   - Keep logs out of version control

## Real-Time Monitoring

For real-time updates when new logs are written:

1. The dashboard already has WebSocket support
2. File watching is built into the backend
3. Just ensure the logs directory is accessible

## Troubleshooting

### Logs not showing?
- Check file permissions: `ls -la ~/.claude/logs/`
- Ensure JSON files are valid: `python -m json.tool ~/.claude/logs/session_start.json`
- Check dashboard logs: Look at browser console for errors

### Dashboard not updating?
- Check WebSocket connection in browser console
- Verify file watching is enabled in backend
- Try manual refresh with Ctrl+F5

### Performance issues?
- Limit log retention (archive old logs)
- Use pagination in API endpoints
- Enable caching in backend

## Next Steps

1. Set up automated log rotation
2. Create backup strategy for logs
3. Implement log filtering by date/project
4. Add export functionality for reports
5. Set up alerts for anomalies

## Security Considerations

- Never commit sensitive data in logs
- Use read-only mounts in Docker
- Implement authentication for production
- Sanitize logs before sharing