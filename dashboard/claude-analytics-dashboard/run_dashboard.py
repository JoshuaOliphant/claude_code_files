#!/usr/bin/env python3
"""
ABOUTME: Startup script for the Claude Code Analytics Dashboard.
ABOUTME: Launches the FastAPI server with proper configuration and error handling.
"""

import os
import sys
import logging
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

try:
    import uvicorn
    from backend.main import app
except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("Make sure all dependencies are installed with: uv sync")
    sys.exit(1)

def main():
    """Start the dashboard server."""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Ensure frontend directory exists
    frontend_dir = Path(__file__).parent / "frontend"
    if not frontend_dir.exists():
        logging.error(f"Frontend directory not found: {frontend_dir}")
        sys.exit(1)
    
    # Start the server
    try:
        print("🚀 Starting Claude Code Analytics Dashboard...")
        print("📊 Dashboard will be available at: http://localhost:8000")
        print("🔗 WebSocket endpoint: ws://localhost:8000/ws")
        print("📡 API endpoints: http://localhost:8000/api/*")
        print("Press Ctrl+C to stop the server")
        print("-" * 60)
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            reload=False,  # Disable reload in production
            access_log=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Shutting down dashboard...")
    except Exception as e:
        logging.error(f"Failed to start server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()