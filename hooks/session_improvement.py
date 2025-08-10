#!/usr/bin/env python3
"""
Hook that analyzes session for improvements after completion
Runs on Stop event to capture patterns for batch improvement processing
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from collections import Counter
from typing import Dict, List, Any
import hashlib

def analyze_session(event: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze completed session for improvement opportunities"""
    
    session_id = event.get('session_id')
    if not session_id:
        return {"error": "No session_id provided", "analyzed": False}
    
    logs_path = Path.home() / ".claude" / "logs"
    
    # Load all relevant log files for this session
    session_logs = load_session_logs(session_id, logs_path)
    
    if not session_logs:
        return {
            "analyzed": True, 
            "session_id": session_id,
            "patterns_found": 0,
            "message": "No logs found for session"
        }
    
    # Analyze the session
    analysis = {
        "session_id": session_id,
        "timestamp": datetime.now().isoformat(),
        "total_events": len(session_logs),
        "patterns": detect_patterns(session_logs),
        "tool_sequences": find_tool_sequences(session_logs),
        "error_sequences": find_error_patterns(session_logs),
        "metrics": calculate_session_metrics(session_logs)
    }
    
    # Only save if we found meaningful patterns
    if analysis["patterns"] or analysis["error_sequences"]:
        save_for_batch_processing(analysis, logs_path)
        
        return {
            "analyzed": True,
            "session_id": session_id,
            "patterns_found": len(analysis["patterns"]),
            "tool_sequences_found": len(analysis["tool_sequences"]),
            "errors_found": len(analysis["error_sequences"]),
            "saved_for_improvement": True
        }
    
    return {
        "analyzed": True,
        "session_id": session_id,
        "patterns_found": 0,
        "message": "No significant patterns detected"
    }

def load_session_logs(session_id: str, logs_path: Path) -> List[Dict]:
    """Load all log entries for a specific session"""
    session_logs = []
    
    # Check all log files for this session's data
    log_files = [
        "session_start.json",
        "pre_tool_use.json",
        "post_tool_use.json",
        "user_prompt_submit.json",
        "notifications.json",
        "stop.json"
    ]
    
    for log_file_name in log_files:
        log_file = logs_path / log_file_name
        if log_file.exists():
            try:
                with open(log_file, 'r') as f:
                    logs = json.load(f)
                    # Filter for this session
                    if isinstance(logs, list):
                        session_entries = [
                            {**log, "log_type": log_file_name.replace('.json', '')}
                            for log in logs 
                            if log.get('session_id') == session_id
                        ]
                        session_logs.extend(session_entries)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not read {log_file}: {e}", file=sys.stderr)
                continue
    
    # Sort by timestamp
    session_logs.sort(key=lambda x: x.get('timestamp', ''))
    
    return session_logs

def detect_patterns(logs: List[Dict]) -> List[Dict]:
    """Detect recurring patterns in the session"""
    patterns = []
    
    # Pattern 1: Repeated tool sequences (3+ tools)
    tool_sequences = []
    for i in range(len(logs) - 2):
        if logs[i].get('tool_name') and logs[i+1].get('tool_name') and logs[i+2].get('tool_name'):
            sequence = (
                logs[i]['tool_name'],
                logs[i+1]['tool_name'],
                logs[i+2]['tool_name']
            )
            tool_sequences.append(sequence)
    
    # Count occurrences
    sequence_counts = Counter(tool_sequences)
    
    for sequence, count in sequence_counts.items():
        if count >= 2:  # Pattern appears at least twice
            patterns.append({
                "type": "tool_sequence",
                "sequence": list(sequence),
                "occurrences": count,
                "potential_command": True,
                "suggested_name": f"{sequence[0]}_{sequence[-1]}_flow".lower().replace(" ", "_")
            })
    
    # Pattern 2: Tool followed by error, then retry
    for i in range(len(logs) - 2):
        if (logs[i].get('success') == False and 
            i + 1 < len(logs) and
            logs[i+1].get('tool_name') == logs[i].get('tool_name')):
            
            patterns.append({
                "type": "error_retry",
                "tool": logs[i].get('tool_name'),
                "error": logs[i].get('error', 'Unknown error'),
                "potential_hook": True,
                "suggested_improvement": "Add validation or error prevention"
            })
    
    return patterns

def find_tool_sequences(logs: List[Dict]) -> List[Dict]:
    """Find sequences of tools used together"""
    sequences = []
    current_sequence = []
    
    for log in logs:
        if log.get('tool_name'):
            current_sequence.append({
                "tool": log['tool_name'],
                "success": log.get('success', True),
                "timestamp": log.get('timestamp')
            })
            
            # If we have a sequence of 5+ tools, save it
            if len(current_sequence) >= 5:
                # Create a hash for this sequence to check for duplicates
                sequence_hash = hashlib.md5(
                    json.dumps([t['tool'] for t in current_sequence]).encode()
                ).hexdigest()[:8]
                
                sequences.append({
                    "id": sequence_hash,
                    "length": len(current_sequence),
                    "tools": [t['tool'] for t in current_sequence],
                    "success_rate": sum(1 for t in current_sequence if t['success']) / len(current_sequence),
                    "potential_agent": True
                })
                
                # Start new sequence with last 2 tools (overlap)
                current_sequence = current_sequence[-2:]
    
    return sequences

def find_error_patterns(logs: List[Dict]) -> List[Dict]:
    """Find patterns in errors"""
    error_patterns = []
    error_groups = {}
    
    for log in logs:
        if not log.get('success', True):
            error_key = f"{log.get('tool_name')}:{log.get('error', 'unknown')[:50]}"
            
            if error_key not in error_groups:
                error_groups[error_key] = {
                    "tool": log.get('tool_name'),
                    "error": log.get('error'),
                    "occurrences": 0,
                    "timestamps": []
                }
            
            error_groups[error_key]["occurrences"] += 1
            error_groups[error_key]["timestamps"].append(log.get('timestamp'))
    
    # Convert to list and add recommendations
    for error_key, error_data in error_groups.items():
        if error_data["occurrences"] >= 2:
            error_patterns.append({
                **error_data,
                "potential_hook": True,
                "suggested_hook_type": "PreToolUse",
                "recommendation": f"Add validation to prevent '{error_data['error'][:100]}'"
            })
    
    return error_patterns

def calculate_session_metrics(logs: List[Dict]) -> Dict[str, Any]:
    """Calculate metrics for the session"""
    metrics = {
        "total_tools_used": sum(1 for log in logs if log.get('tool_name')),
        "unique_tools": len(set(log.get('tool_name') for log in logs if log.get('tool_name'))),
        "error_rate": 0.0,
        "total_execution_time": 0.0,
        "average_execution_time": 0.0,
        "longest_operation": None
    }
    
    tool_logs = [log for log in logs if log.get('tool_name')]
    
    if tool_logs:
        error_count = sum(1 for log in tool_logs if not log.get('success', True))
        metrics["error_rate"] = error_count / len(tool_logs)
        
        execution_times = [log.get('execution_time', 0) for log in tool_logs if log.get('execution_time')]
        if execution_times:
            metrics["total_execution_time"] = sum(execution_times)
            metrics["average_execution_time"] = metrics["total_execution_time"] / len(execution_times)
            
            # Find longest operation
            max_time_log = max(tool_logs, key=lambda x: x.get('execution_time', 0))
            metrics["longest_operation"] = {
                "tool": max_time_log.get('tool_name'),
                "time": max_time_log.get('execution_time', 0)
            }
    
    return metrics

def save_for_batch_processing(analysis: Dict, logs_path: Path):
    """Save analysis for later batch processing"""
    improvements_file = logs_path / "pending_improvements.json"
    
    # Load existing improvements
    existing_improvements = []
    if improvements_file.exists():
        try:
            with open(improvements_file, 'r') as f:
                existing_improvements = json.load(f)
        except (json.JSONDecodeError, IOError):
            existing_improvements = []
    
    # Add new analysis
    existing_improvements.append(analysis)
    
    # Keep only last 100 sessions to prevent file from growing too large
    if len(existing_improvements) > 100:
        existing_improvements = existing_improvements[-100:]
    
    # Save back to file
    try:
        with open(improvements_file, 'w') as f:
            json.dump(existing_improvements, f, indent=2)
    except IOError as e:
        print(f"Error saving improvements: {e}", file=sys.stderr)

def main():
    """Main entry point for the hook"""
    try:
        # Read event from stdin
        event = json.loads(sys.stdin.read())
        
        # Analyze the session
        result = analyze_session(event)
        
        # Output result
        print(json.dumps(result))
        
    except Exception as e:
        # Output error in expected format
        error_result = {
            "error": str(e),
            "analyzed": False
        }
        print(json.dumps(error_result))
        sys.exit(1)

if __name__ == "__main__":
    main()