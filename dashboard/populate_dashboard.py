#!/usr/bin/env python3
"""
Script to populate the Claude Code Analytics Dashboard with data
Can either use sample data or connect to actual log files
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path
import sys

def generate_sample_data():
    """Generate realistic sample data for the dashboard"""
    
    base_path = Path("/workdir/logs")
    base_path.mkdir(exist_ok=True)
    
    # Generate session data
    sessions = []
    session_starts = []
    current_time = datetime.now()
    
    for i in range(10):
        session_id = f"session_{i+1}"
        start_time = current_time - timedelta(days=random.randint(0, 7), hours=random.randint(0, 23))
        
        # Session start log
        session_starts.append({
            "timestamp": start_time.isoformat(),
            "session_id": session_id,
            "git_status": {
                "branch": random.choice(["main", "feature/test", "fix/bug"]),
                "uncommitted_changes": random.randint(0, 10)
            }
        })
    
    # Generate tool usage data
    tools = ["Read", "Write", "Edit", "Bash", "Grep", "Task", "WebSearch", "MultiEdit"]
    pre_tool_uses = []
    post_tool_uses = []
    
    for _ in range(100):
        session_id = f"session_{random.randint(1, 10)}"
        tool = random.choice(tools)
        timestamp = current_time - timedelta(
            days=random.randint(0, 7),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        
        pre_tool_uses.append({
            "timestamp": timestamp.isoformat(),
            "session_id": session_id,
            "tool_name": tool,
            "input": {"example": "data"}
        })
        
        # 90% success rate
        success = random.random() > 0.1
        execution_time = random.uniform(0.1, 5.0) if success else random.uniform(5.0, 30.0)
        
        post_tool_uses.append({
            "timestamp": (timestamp + timedelta(seconds=execution_time)).isoformat(),
            "session_id": session_id,
            "tool_name": tool,
            "success": success,
            "execution_time": execution_time,
            "error": None if success else f"Error in {tool}: Sample error message"
        })
    
    # Generate user prompts
    user_prompts = []
    prompt_examples = [
        "Fix the TypeScript error in the main component",
        "Add a new feature for user authentication",
        "Refactor the database connection module",
        "Write tests for the API endpoints",
        "Update the documentation",
        "Debug the performance issue",
        "Implement caching for better performance",
        "Review and optimize the code"
    ]
    
    for _ in range(50):
        session_id = f"session_{random.randint(1, 10)}"
        timestamp = current_time - timedelta(
            days=random.randint(0, 7),
            hours=random.randint(0, 23)
        )
        
        user_prompts.append({
            "timestamp": timestamp.isoformat(),
            "session_id": session_id,
            "prompt": random.choice(prompt_examples)
        })
    
    # Write all log files
    logs = {
        "session_start.json": session_starts,
        "pre_tool_use.json": pre_tool_uses,
        "post_tool_use.json": post_tool_uses,
        "user_prompt_submit.json": user_prompts,
        "notification.json": [],
        "stop.json": [],
        "subagent_stop.json": []
    }
    
    for filename, data in logs.items():
        file_path = base_path / filename
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    print(f"✅ Generated sample data in {base_path}")
    print(f"   - {len(session_starts)} sessions")
    print(f"   - {len(pre_tool_uses)} tool executions")
    print(f"   - {len(user_prompts)} user prompts")
    print(f"   - {sum(1 for p in post_tool_uses if not p['success'])} errors")
    
    return base_path

def copy_actual_logs(source_path):
    """Copy actual log files to the dashboard location"""
    source = Path(source_path)
    dest = Path("/workdir/logs")
    dest.mkdir(exist_ok=True)
    
    if not source.exists():
        print(f"❌ Source path {source} does not exist")
        return None
    
    copied = 0
    for log_file in source.glob("*.json"):
        dest_file = dest / log_file.name
        try:
            with open(log_file, 'r') as f:
                data = json.load(f)
            with open(dest_file, 'w') as f:
                json.dump(data, f, indent=2)
            copied += 1
            print(f"✅ Copied {log_file.name}")
        except Exception as e:
            print(f"⚠️ Failed to copy {log_file.name}: {e}")
    
    if copied > 0:
        print(f"\n✅ Successfully copied {copied} log files to {dest}")
        return dest
    else:
        print(f"❌ No log files were copied")
        return None

def main():
    print("Claude Code Analytics Dashboard - Data Setup")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        # Use provided path to actual logs
        source = sys.argv[1]
        print(f"Attempting to copy logs from: {source}")
        result = copy_actual_logs(source)
        if not result:
            print("\nFalling back to sample data generation...")
            generate_sample_data()
    else:
        # Generate sample data
        print("Generating sample data for dashboard...")
        generate_sample_data()
    
    print("\n" + "=" * 50)
    print("Dashboard data is ready!")
    print("The dashboard should now display the data.")
    print("\nIf running locally, ensure the dashboard backend is")
    print("configured to read from: /workdir/logs/")

if __name__ == "__main__":
    main()