#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "psutil>=5.9.0",
# ]
# ///

"""
ABOUTME: Enhanced post-tool-use hook with performance metrics and analysis integration.
ABOUTME: Collects detailed metrics and triggers real-time analysis for optimization insights.
"""

import json
import os
import sys
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
import resource

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False


def collect_performance_metrics(start_time: float) -> Dict[str, Any]:
    """Collect performance metrics for the tool execution."""
    end_time = time.time()
    execution_time = end_time - start_time
    
    metrics = {
        'execution_time': execution_time,
        'timestamp': datetime.now().isoformat(),
    }
    
    # Add system resource metrics if available
    if PSUTIL_AVAILABLE:
        try:
            process = psutil.Process()
            metrics.update({
                'cpu_percent': process.cpu_percent(),
                'memory_mb': process.memory_info().rss / 1024 / 1024,
                'memory_percent': process.memory_percent(),
            })
            
            # System-wide metrics
            metrics.update({
                'system_cpu_percent': psutil.cpu_percent(interval=0.1),
                'system_memory_percent': psutil.virtual_memory().percent,
                'system_disk_io': dict(psutil.disk_io_counters()._asdict()) if psutil.disk_io_counters() else {},
            })
        except:
            pass  # Ignore errors in metric collection
    
    # Add resource usage metrics
    try:
        usage = resource.getrusage(resource.RUSAGE_SELF)
        metrics.update({
            'user_time': usage.ru_utime,
            'system_time': usage.ru_stime,
            'max_memory_kb': usage.ru_maxrss,
        })
    except:
        pass
    
    return metrics


def enhance_log_data(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Enhance log data with additional context and analysis triggers."""
    enhanced_data = input_data.copy()
    
    # Add event type for analysis
    enhanced_data['event_type'] = 'tool_use'
    
    # Add session context
    session_id = input_data.get('session_id', 'unknown')
    enhanced_data['session_id'] = session_id
    
    # Add project context
    cwd = os.getcwd()
    enhanced_data['project_context'] = {
        'working_directory': cwd,
        'project_name': Path(cwd).name,
    }
    
    # Extract tool information
    tool_name = input_data.get('name', 'unknown')
    enhanced_data['tool_name'] = tool_name
    
    # Add error classification
    if input_data.get('error'):
        error_msg = str(input_data['error'])
        enhanced_data['error_classification'] = classify_error(error_msg)
    
    # Add success indicators
    enhanced_data['success'] = not bool(input_data.get('error'))
    
    return enhanced_data


def classify_error(error_message: str) -> Dict[str, Any]:
    """Classify error types for better pattern detection."""
    error_lower = error_message.lower()
    
    classification = {
        'error_type': 'unknown',
        'is_retryable': False,
        'severity': 'medium'
    }
    
    # Classify error types
    if any(word in error_lower for word in ['timeout', 'timed out']):
        classification['error_type'] = 'timeout'
        classification['is_retryable'] = True
        classification['severity'] = 'medium'
    elif any(word in error_lower for word in ['permission', 'unauthorized', 'access denied']):
        classification['error_type'] = 'permission'
        classification['is_retryable'] = False
        classification['severity'] = 'high'
    elif any(word in error_lower for word in ['not found', '404', 'missing']):
        classification['error_type'] = 'not_found'
        classification['is_retryable'] = False
        classification['severity'] = 'medium'
    elif any(word in error_lower for word in ['network', 'connection', 'dns']):
        classification['error_type'] = 'network'
        classification['is_retryable'] = True
        classification['severity'] = 'medium'
    elif any(word in error_lower for word in ['memory', 'out of memory', 'oom']):
        classification['error_type'] = 'resource'
        classification['is_retryable'] = True
        classification['severity'] = 'high'
    elif any(word in error_lower for word in ['syntax', 'invalid', 'malformed']):
        classification['error_type'] = 'validation'
        classification['is_retryable'] = False
        classification['severity'] = 'medium'
    
    return classification


def trigger_analysis(log_data: Dict[str, Any]) -> None:
    """Trigger real-time analysis if conditions are met."""
    # Only trigger analysis for significant events
    should_analyze = (
        log_data.get('error') or  # Any error
        (log_data.get('metrics', {}).get('execution_time', 0) > 30) or  # Long execution
        (log_data.get('tool_name', '') in ['environment_run_cmd', 'Write', 'Edit'])  # Important tools
    )
    
    if should_analyze:
        try:
            # Try to trigger real-time analysis (fire-and-forget)
            analysis_script = Path(__file__).parent.parent / 'analysis' / 'real_time_monitor.py'
            if analysis_script.exists():
                # This would ideally be done via a message queue or async process
                # For now, just log that analysis should be triggered
                log_data['analysis_trigger'] = {
                    'should_analyze': True,
                    'trigger_reason': 'significant_event',
                    'analysis_script': str(analysis_script)
                }
        except Exception:
            pass  # Don't let analysis triggering break the main hook


def main():
    """Main hook execution function."""
    start_time = time.time()
    
    try:
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)
        
        # Collect performance metrics
        metrics = collect_performance_metrics(start_time)
        
        # Enhance log data
        enhanced_data = enhance_log_data(input_data)
        enhanced_data['metrics'] = metrics
        
        # Trigger analysis if needed
        trigger_analysis(enhanced_data)
        
        # Ensure log directory exists
        log_dir = Path.cwd() / 'logs'
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Write to original log file (for compatibility)
        original_log_path = log_dir / 'post_tool_use.json'
        if original_log_path.exists():
            with open(original_log_path, 'r') as f:
                try:
                    log_data = json.load(f)
                except (json.JSONDecodeError, ValueError):
                    log_data = []
        else:
            log_data = []
        
        log_data.append(input_data)  # Original data for compatibility
        
        with open(original_log_path, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        # Write to enhanced log file (for analysis)
        enhanced_log_path = log_dir / 'enhanced_tool_use.json'
        if enhanced_log_path.exists():
            with open(enhanced_log_path, 'r') as f:
                try:
                    enhanced_log_data = json.load(f)
                except (json.JSONDecodeError, ValueError):
                    enhanced_log_data = []
        else:
            enhanced_log_data = []
        
        enhanced_log_data.append(enhanced_data)
        
        with open(enhanced_log_path, 'w') as f:
            json.dump(enhanced_log_data, f, indent=2)
        
        sys.exit(0)
        
    except json.JSONDecodeError:
        # Handle JSON decode errors gracefully
        sys.exit(0)
    except Exception as e:
        # Log error but don't fail the hook
        try:
            error_log = {
                'timestamp': datetime.now().isoformat(),
                'hook_error': str(e),
                'hook_name': 'enhanced_post_tool_use'
            }
            
            error_log_path = Path.cwd() / 'logs' / 'hook_errors.json'
            if error_log_path.exists():
                with open(error_log_path, 'r') as f:
                    try:
                        errors = json.load(f)
                    except:
                        errors = []
            else:
                errors = []
            
            errors.append(error_log)
            
            with open(error_log_path, 'w') as f:
                json.dump(errors, f, indent=2)
        except:
            pass  # If we can't log the error, just continue
        
        sys.exit(0)


if __name__ == '__main__':
    main()