#!/bin/bash

# ABOUTME: Convenient startup script for the Claude Code Analytics Dashboard.
# ABOUTME: Sets up environment and starts the dashboard server with proper configuration.

set -e

echo "🚀 Starting Claude Code Analytics Dashboard..."
echo ""

# Check if we're in the right directory
DASHBOARD_DIR="/workdir/dashboard/claude-analytics-dashboard"
if [ ! -d "$DASHBOARD_DIR" ]; then
    echo "❌ Dashboard directory not found: $DASHBOARD_DIR"
    exit 1
fi

# Add uv to PATH
export PATH="/root/.local/bin:$PATH"

# Check if uv is available
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed or not in PATH"
    echo "Please install uv first: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Navigate to dashboard directory
cd "$DASHBOARD_DIR"

# Install/sync dependencies
echo "📦 Installing dependencies..."
uv sync --quiet

# Create logs directory if it doesn't exist
mkdir -p logs/sample

# Start the dashboard
echo ""
echo "🎯 Dashboard starting on http://localhost:8000"
echo "📊 Sample data is available for demonstration"
echo "🔄 Real-time updates via WebSocket on ws://localhost:8000/ws"
echo ""
echo "API Endpoints:"
echo "  • GET  /api/analytics    - Complete analytics data"
echo "  • GET  /api/sessions     - Session data"
echo "  • GET  /api/tools        - Tool usage statistics"
echo "  • GET  /api/errors       - Error analysis"
echo "  • GET  /api/performance  - Performance metrics"
echo ""
echo "Press Ctrl+C to stop the dashboard"
echo "=" * 60

# Run the dashboard
uv run python run_dashboard.py