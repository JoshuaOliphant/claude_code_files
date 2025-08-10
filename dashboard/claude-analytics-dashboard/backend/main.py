#!/usr/bin/env python3
"""
ABOUTME: FastAPI backend for Claude Code analytics dashboard.
ABOUTME: Provides REST API endpoints for log analysis and real-time monitoring.
"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import asyncio
from collections import defaultdict, Counter

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Claude Code Analytics Dashboard",
    description="Real-time analytics for Claude Code hook logs",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state for WebSocket connections and data caching
websocket_connections: List[WebSocket] = []
cached_analytics: Dict[str, Any] = {}
last_update: Optional[datetime] = None

# Configuration
LOGS_PATH = Path("/workdir/dashboard/logs")
SAMPLE_LOGS_PATH = Path("/workdir/dashboard/logs/sample")


class LogFileHandler(FileSystemEventHandler):
    """Handles log file changes for real-time updates."""
    
    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith('.json'):
            logger.info(f"Log file modified: {event.src_path}")
            asyncio.create_task(self.notify_clients())
    
    async def notify_clients(self):
        """Notify all connected WebSocket clients of data updates."""
        if websocket_connections:
            analytics = await get_analytics_data()
            message = {
                "type": "data_update",
                "timestamp": datetime.now().isoformat(),
                "data": analytics
            }
            
            disconnected = []
            for websocket in websocket_connections:
                try:
                    await websocket.send_json(message)
                except:
                    disconnected.append(websocket)
            
            # Remove disconnected clients
            for ws in disconnected:
                websocket_connections.remove(ws)


def load_log_files() -> Dict[str, List[Dict]]:
    """Load all log files from the logs directory."""
    logs = {}
    
    # Check both main logs and sample logs
    log_dirs = [LOGS_PATH, SAMPLE_LOGS_PATH]
    
    for log_dir in log_dirs:
        if not log_dir.exists():
            continue
            
        for log_file in log_dir.glob("*.json"):
            try:
                with open(log_file, 'r') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        logs[log_file.stem] = data
                    else:
                        logs[log_file.stem] = [data]
            except (json.JSONDecodeError, FileNotFoundError) as e:
                logger.error(f"Error loading log file {log_file}: {e}")
                continue
    
    return logs


def calculate_session_metrics(logs: Dict[str, List[Dict]]) -> Dict[str, Any]:
    """Calculate session-based metrics."""
    sessions = {}
    
    # Process session starts
    for session_data in logs.get('session_start', []):
        session_id = session_data.get('session_id')
        if session_id:
            sessions[session_id] = {
                'start_time': session_data.get('timestamp'),
                'source': session_data.get('source'),
                'project_path': session_data.get('project_path'),
                'tools_used': [],
                'prompts': [],
                'errors': 0,
                'total_execution_time': 0.0
            }
    
    # Process tool usage
    for tool_data in logs.get('post_tool_use', []):
        session_id = tool_data.get('session_id')
        if session_id in sessions:
            sessions[session_id]['tools_used'].append({
                'tool_name': tool_data.get('tool_name'),
                'success': tool_data.get('success'),
                'execution_time': tool_data.get('execution_time', 0),
                'timestamp': tool_data.get('timestamp')
            })
            
            if not tool_data.get('success', True):
                sessions[session_id]['errors'] += 1
            
            sessions[session_id]['total_execution_time'] += tool_data.get('execution_time', 0)
    
    # Process prompts
    for prompt_data in logs.get('user_prompt_submit', []):
        session_id = prompt_data.get('session_id')
        if session_id in sessions:
            sessions[session_id]['prompts'].append({
                'timestamp': prompt_data.get('timestamp'),
                'length': prompt_data.get('prompt_length'),
                'response_time': prompt_data.get('response_time'),
                'tokens_used': prompt_data.get('tokens_used')
            })
    
    return sessions


def calculate_tool_metrics(logs: Dict[str, List[Dict]]) -> Dict[str, Any]:
    """Calculate tool usage metrics."""
    tools = defaultdict(list)
    
    for tool_data in logs.get('post_tool_use', []):
        tool_name = tool_data.get('tool_name', 'unknown')
        tools[tool_name].append({
            'success': tool_data.get('success', True),
            'execution_time': tool_data.get('execution_time', 0),
            'timestamp': tool_data.get('timestamp'),
            'session_id': tool_data.get('session_id')
        })
    
    tool_stats = {}
    for tool_name, tool_data in tools.items():
        success_count = sum(1 for t in tool_data if t['success'])
        total_count = len(tool_data)
        avg_time = np.mean([t['execution_time'] for t in tool_data]) if tool_data else 0
        
        tool_stats[tool_name] = {
            'usage_count': total_count,
            'success_rate': success_count / total_count if total_count > 0 else 0,
            'avg_execution_time': avg_time,
            'total_execution_time': sum(t['execution_time'] for t in tool_data),
            'recent_usage': sorted(tool_data, key=lambda x: x['timestamp'])[-10:]  # Last 10 uses
        }
    
    return tool_stats


def calculate_error_patterns(logs: Dict[str, List[Dict]]) -> Dict[str, Any]:
    """Analyze error patterns and trends."""
    errors = []
    
    for tool_data in logs.get('post_tool_use', []):
        if not tool_data.get('success', True):
            errors.append({
                'timestamp': tool_data.get('timestamp'),
                'tool_name': tool_data.get('tool_name'),
                'error': tool_data.get('error'),
                'session_id': tool_data.get('session_id'),
                'execution_time': tool_data.get('execution_time', 0)
            })
    
    error_by_tool = Counter(error['tool_name'] for error in errors)
    error_by_time = defaultdict(int)
    
    # Group errors by hour
    for error in errors:
        if error['timestamp']:
            try:
                dt = datetime.fromisoformat(error['timestamp'].replace('Z', '+00:00'))
                hour_key = dt.strftime('%Y-%m-%d %H:00')
                error_by_time[hour_key] += 1
            except:
                continue
    
    return {
        'total_errors': len(errors),
        'errors_by_tool': dict(error_by_tool),
        'errors_by_time': dict(error_by_time),
        'recent_errors': sorted(errors, key=lambda x: x['timestamp'])[-20:]  # Last 20 errors
    }


def calculate_performance_metrics(logs: Dict[str, List[Dict]]) -> Dict[str, Any]:
    """Calculate performance metrics and trends."""
    tool_times = []
    response_times = []
    
    # Collect tool execution times
    for tool_data in logs.get('post_tool_use', []):
        if tool_data.get('execution_time'):
            tool_times.append({
                'tool_name': tool_data.get('tool_name'),
                'execution_time': tool_data.get('execution_time'),
                'timestamp': tool_data.get('timestamp'),
                'success': tool_data.get('success', True)
            })
    
    # Collect prompt response times
    for prompt_data in logs.get('user_prompt_submit', []):
        if prompt_data.get('response_time'):
            response_times.append({
                'response_time': prompt_data.get('response_time'),
                'timestamp': prompt_data.get('timestamp'),
                'tokens_used': prompt_data.get('tokens_used'),
                'prompt_length': prompt_data.get('prompt_length')
            })
    
    # Calculate percentiles
    exec_times = [t['execution_time'] for t in tool_times if t['execution_time']]
    resp_times = [r['response_time'] for r in response_times if r['response_time']]
    
    performance_stats = {
        'tool_execution': {
            'mean': np.mean(exec_times) if exec_times else 0,
            'median': np.median(exec_times) if exec_times else 0,
            'p95': np.percentile(exec_times, 95) if exec_times else 0,
            'p99': np.percentile(exec_times, 99) if exec_times else 0,
            'count': len(exec_times)
        },
        'response_times': {
            'mean': np.mean(resp_times) if resp_times else 0,
            'median': np.median(resp_times) if resp_times else 0,
            'p95': np.percentile(resp_times, 95) if resp_times else 0,
            'p99': np.percentile(resp_times, 99) if resp_times else 0,
            'count': len(resp_times)
        },
        'slowest_tools': sorted(
            [{'tool': t['tool_name'], 'time': t['execution_time']} for t in tool_times],
            key=lambda x: x['time'], reverse=True
        )[:10]
    }
    
    return performance_stats


async def get_analytics_data() -> Dict[str, Any]:
    """Get comprehensive analytics data."""
    global cached_analytics, last_update
    
    # Check if cache is still valid (update every 30 seconds)
    if (last_update and 
        datetime.now() - last_update < timedelta(seconds=30) and 
        cached_analytics):
        return cached_analytics
    
    logs = load_log_files()
    
    if not logs:
        return {
            "error": "No log files found",
            "sessions": {},
            "tools": {},
            "errors": {},
            "performance": {},
            "summary": {
                "total_sessions": 0,
                "total_tools_used": 0,
                "total_errors": 0,
                "avg_session_duration": 0
            }
        }
    
    sessions = calculate_session_metrics(logs)
    tools = calculate_tool_metrics(logs)
    errors = calculate_error_patterns(logs)
    performance = calculate_performance_metrics(logs)
    
    # Calculate summary stats
    summary = {
        "total_sessions": len(sessions),
        "total_tools_used": sum(len(s['tools_used']) for s in sessions.values()),
        "total_errors": errors['total_errors'],
        "avg_session_duration": np.mean([s['total_execution_time'] for s in sessions.values()]) if sessions else 0
    }
    
    analytics = {
        "timestamp": datetime.now().isoformat(),
        "sessions": sessions,
        "tools": tools,
        "errors": errors,
        "performance": performance,
        "summary": summary
    }
    
    cached_analytics = analytics
    last_update = datetime.now()
    
    return analytics


@app.get("/")
async def read_root():
    """Serve the main dashboard page."""
    return FileResponse("/workdir/dashboard/claude-analytics-dashboard/frontend/index.html")


@app.get("/api/analytics")
async def get_analytics():
    """Get comprehensive analytics data."""
    try:
        return await get_analytics_data()
    except Exception as e:
        logger.error(f"Error getting analytics data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/sessions")
async def get_sessions():
    """Get session data."""
    try:
        analytics = await get_analytics_data()
        return analytics.get("sessions", {})
    except Exception as e:
        logger.error(f"Error getting sessions data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/tools")
async def get_tools():
    """Get tool usage data."""
    try:
        analytics = await get_analytics_data()
        return analytics.get("tools", {})
    except Exception as e:
        logger.error(f"Error getting tools data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/errors")
async def get_errors():
    """Get error analysis data."""
    try:
        analytics = await get_analytics_data()
        return analytics.get("errors", {})
    except Exception as e:
        logger.error(f"Error getting error data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/performance")
async def get_performance():
    """Get performance metrics."""
    try:
        analytics = await get_analytics_data()
        return analytics.get("performance", {})
    except Exception as e:
        logger.error(f"Error getting performance data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates."""
    await websocket.accept()
    websocket_connections.append(websocket)
    
    try:
        # Send initial data
        analytics = await get_analytics_data()
        await websocket.send_json({
            "type": "initial_data",
            "timestamp": datetime.now().isoformat(),
            "data": analytics
        })
        
        # Keep connection alive
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        websocket_connections.remove(websocket)


# Mount static files
app.mount("/static", StaticFiles(directory="/workdir/dashboard/claude-analytics-dashboard/frontend"), name="static")


# Initialize file watcher
def setup_file_watcher():
    """Set up file system watcher for real-time updates."""
    if LOGS_PATH.exists() or SAMPLE_LOGS_PATH.exists():
        event_handler = LogFileHandler()
        observer = Observer()
        
        if LOGS_PATH.exists():
            observer.schedule(event_handler, str(LOGS_PATH), recursive=True)
        if SAMPLE_LOGS_PATH.exists():
            observer.schedule(event_handler, str(SAMPLE_LOGS_PATH), recursive=True)
        
        observer.start()
        logger.info("File watcher started")
        return observer
    return None


@app.on_event("startup")
async def startup_event():
    """Initialize the application."""
    logger.info("Starting Claude Code Analytics Dashboard")
    
    # Ensure directories exist
    LOGS_PATH.mkdir(parents=True, exist_ok=True)
    SAMPLE_LOGS_PATH.mkdir(parents=True, exist_ok=True)
    
    # Setup file watcher
    observer = setup_file_watcher()
    if observer:
        app.state.observer = observer
    
    # Pre-load analytics data
    await get_analytics_data()
    logger.info("Dashboard initialized successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources."""
    if hasattr(app.state, 'observer'):
        app.state.observer.stop()
        app.state.observer.join()
    logger.info("Dashboard shutdown complete")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)