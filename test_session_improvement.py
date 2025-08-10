#!/usr/bin/env python3
"""Test the session_improvement hook with sample data"""

import json
import subprocess
import sys
from pathlib import Path

def test_hook():
    """Test the session improvement hook"""
    
    # Sample event data that would come from Claude Code
    test_event = {
        "session_id": "test_session_123",
        "timestamp": "2025-01-10T10:00:00Z",
        "source": "test",
        "event_type": "stop"
    }
    
    # Call the hook
    result = subprocess.run(
        ["uv", "run", "/Users/joshuaoliphant/.claude/hooks/session_improvement.py"],
        input=json.dumps(test_event),
        capture_output=True,
        text=True
    )
    
    print("Hook exit code:", result.returncode)
    print("\nStdout:")
    print(result.stdout)
    
    if result.stderr:
        print("\nStderr:")
        print(result.stderr)
    
    # Try to parse the output
    try:
        output = json.loads(result.stdout)
        print("\nParsed output:")
        print(json.dumps(output, indent=2))
    except json.JSONDecodeError as e:
        print(f"\nCould not parse output as JSON: {e}")

if __name__ == "__main__":
    test_hook()