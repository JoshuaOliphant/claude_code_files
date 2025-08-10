#!/usr/bin/env python3
"""
ABOUTME: Script to generate additional sample data for dashboard demonstration.
ABOUTME: Creates realistic log entries to showcase all dashboard features.
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path

def generate_sample_data():
    """Generate comprehensive sample data for the dashboard."""
    
    # Base timestamp (last 24 hours)
    base_time = datetime.now() - timedelta(hours=24)
    
    # Tools and their typical execution times
    tools = {
        'environment_run_cmd': (1.0, 15.0, 0.85),  # (min_time, max_time, success_rate)
        'environment_file_write': (0.2, 2.0, 0.95),
        'environment_file_read': (0.1, 1.5, 0.98),
        'environment_file_list': (0.1, 0.8, 0.99),
        'environment_file_delete': (0.1, 0.5, 0.92),
        'environment_checkpoint': (5.0, 30.0, 0.88),
    }
    
    # Generate sessions
    sessions = []
    tools_used = []
    prompts = []
    
    session_count = random.randint(15, 25)
    
    for i in range(session_count):
        session_id = f"sess_{i:03d}"
        
        # Random session start time
        session_start = base_time + timedelta(
            hours=random.uniform(0, 24),
            minutes=random.randint(0, 59)
        )
        
        # Session data
        sessions.append({
            "session_id": session_id,
            "timestamp": session_start.isoformat() + "Z",
            "event_type": "session_start",
            "source": random.choice(["startup", "resume", "startup", "startup"]),  # Bias toward startup
            "project_path": f"/Users/joshuaoliphant/projects/{random.choice(['webapp', 'api', 'dashboard', 'ml-model', 'docs', 'scripts'])}",
            "user_id": "user_001"
        })
        
        # Generate tools for this session
        session_tool_count = random.randint(3, 12)
        current_time = session_start
        
        for j in range(session_tool_count):
            tool_name = random.choice(list(tools.keys()))
            min_time, max_time, success_rate = tools[tool_name]
            
            # Add some time between tool uses
            current_time += timedelta(minutes=random.randint(1, 10))
            
            success = random.random() < success_rate
            execution_time = random.uniform(min_time, max_time)
            
            # If it's an error, make it take longer
            if not success:
                execution_time *= random.uniform(2.0, 4.0)
            
            tool_data = {
                "session_id": session_id,
                "timestamp": current_time.isoformat() + "Z",
                "event_type": "tool_use",
                "tool_name": tool_name,
                "success": success,
                "execution_time": round(execution_time, 2),
                "output_size": random.randint(100, 5000) if success else 0,
                "error": None if success else f"Command failed: {random.choice(['timeout', 'permission denied', 'file not found', 'syntax error', 'network error'])}"
            }
            
            tools_used.append(tool_data)
        
        # Generate prompts for this session
        session_prompt_count = random.randint(2, 6)
        prompt_time = session_start + timedelta(minutes=random.randint(5, 30))
        
        for k in range(session_prompt_count):
            prompt_time += timedelta(minutes=random.randint(3, 15))
            
            prompt_length = random.randint(20, 300)
            response_time = random.uniform(1.0, 8.0) + (prompt_length / 100)  # Longer prompts = longer responses
            
            prompts.append({
                "session_id": session_id,
                "timestamp": prompt_time.isoformat() + "Z",
                "event_type": "user_prompt",
                "prompt_length": prompt_length,
                "prompt_hash": f"hash_{random.randint(100000, 999999)}",
                "response_time": round(response_time, 1),
                "tokens_used": random.randint(300, 2000)
            })
    
    return sessions, tools_used, prompts

def save_sample_data():
    """Save generated sample data to files."""
    logs_dir = Path("/workdir/dashboard/logs/sample")
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    sessions, tools_used, prompts = generate_sample_data()
    
    # Save to files
    with open(logs_dir / "session_start.json", "w") as f:
        json.dump(sessions, f, indent=2)
    
    with open(logs_dir / "post_tool_use.json", "w") as f:
        json.dump(tools_used, f, indent=2)
    
    with open(logs_dir / "user_prompt_submit.json", "w") as f:
        json.dump(prompts, f, indent=2)
    
    print(f"✅ Generated sample data:")
    print(f"   • {len(sessions)} sessions")
    print(f"   • {len(tools_used)} tool executions")
    print(f"   • {len(prompts)} user prompts")
    print(f"   • {sum(1 for t in tools_used if not t['success'])} errors")
    print(f"📁 Files saved to: {logs_dir}")

if __name__ == "__main__":
    save_sample_data()