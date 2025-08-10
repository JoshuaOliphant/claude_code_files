#!/bin/bash
# Setup script to connect the dashboard to real Claude Code logs

echo "Claude Code Analytics Dashboard - Real Logs Setup"
echo "=================================================="

# Option 1: Symlink to actual logs (if accessible)
setup_symlink() {
    echo "Setting up symlink to real logs..."
    LOG_SOURCE="$1"
    LOG_DEST="/workdir/dashboard/logs"
    
    # Remove existing logs directory
    rm -rf "$LOG_DEST"
    
    # Create symlink
    ln -s "$LOG_SOURCE" "$LOG_DEST"
    
    if [ $? -eq 0 ]; then
        echo "✅ Symlink created: $LOG_DEST -> $LOG_SOURCE"
        echo "   Dashboard will now read from your actual logs"
    else
        echo "❌ Failed to create symlink"
        return 1
    fi
}

# Option 2: Copy logs periodically
setup_sync() {
    echo "Setting up periodic log sync..."
    LOG_SOURCE="$1"
    LOG_DEST="/workdir/dashboard/logs"
    
    # Initial copy
    mkdir -p "$LOG_DEST"
    cp -r "$LOG_SOURCE"/*.json "$LOG_DEST/" 2>/dev/null
    
    echo "✅ Initial logs copied"
    echo "   Creating sync script..."
    
    # Create sync script
    cat > /workdir/dashboard/sync_logs.sh << 'EOF'
#!/bin/bash
while true; do
    cp -r SOURCE/*.json DEST/ 2>/dev/null
    echo "$(date): Logs synced"
    sleep 60  # Sync every minute
done
EOF
    
    sed -i "s|SOURCE|$LOG_SOURCE|g" /workdir/dashboard/sync_logs.sh
    sed -i "s|DEST|$LOG_DEST|g" /workdir/dashboard/sync_logs.sh
    chmod +x /workdir/dashboard/sync_logs.sh
    
    echo "✅ Sync script created: /workdir/dashboard/sync_logs.sh"
    echo "   Run it in background: nohup /workdir/dashboard/sync_logs.sh &"
}

# Option 3: Mount volume (Docker)
setup_docker_mount() {
    echo "For Docker deployment, add this to your docker-compose.yml:"
    echo ""
    cat << 'EOF'
version: '3.8'
services:
  dashboard:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ~/.claude/logs:/workdir/dashboard/logs:ro
    environment:
      - LOGS_PATH=/workdir/dashboard/logs
EOF
}

# Option 4: Environment variable configuration
setup_env_config() {
    echo "Setting up environment configuration..."
    cat > /workdir/dashboard/.env << EOF
# Claude Code Dashboard Configuration
LOGS_PATH=$1
WATCH_LOGS=true
UPDATE_INTERVAL=30
EOF
    echo "✅ Environment configuration created"
}

# Main menu
echo ""
echo "Choose setup method:"
echo "1) Symlink (best for local development)"
echo "2) Periodic sync (for isolated environments)"
echo "3) Docker mount (for containerized deployment)"
echo "4) Environment config (flexible path configuration)"
echo ""
echo "Or run directly with path:"
echo "  ./setup_real_logs.sh /path/to/logs"
echo ""

# Handle command line argument
if [ $# -eq 1 ]; then
    LOG_PATH="$1"
    echo "Using log path: $LOG_PATH"
    
    if [ -d "$LOG_PATH" ]; then
        setup_symlink "$LOG_PATH"
        setup_env_config "$LOG_PATH"
    else
        echo "❌ Directory not found: $LOG_PATH"
        exit 1
    fi
else
    echo "Usage: ./setup_real_logs.sh /Users/joshuaoliphant/.claude/logs"
fi