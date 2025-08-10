#!/usr/bin/env python3
"""
View pending improvements collected by the session improvement hook
"""

import json
from pathlib import Path
from datetime import datetime
from collections import Counter
from typing import Dict, List

def view_improvements():
    """Display pending improvements in a readable format"""
    
    improvements_file = Path.home() / ".claude" / "logs" / "pending_improvements.json"
    
    if not improvements_file.exists():
        print("📊 No pending improvements found.")
        print("\nThe session improvement hook will collect patterns as you use Claude Code.")
        print("Patterns are saved when sessions end and include:")
        print("  • Repeated tool sequences (potential commands)")
        print("  • Complex workflows (potential agents)")
        print("  • Error patterns (potential validation hooks)")
        return
    
    try:
        with open(improvements_file, 'r') as f:
            improvements = json.load(f)
    except json.JSONDecodeError:
        print("❌ Error reading improvements file")
        return
    
    if not improvements:
        print("📊 No pending improvements found.")
        return
    
    print(f"📊 Pending Improvements Analysis")
    print(f"{'='*50}")
    print(f"Total sessions analyzed: {len(improvements)}")
    
    # Aggregate patterns across all sessions
    all_patterns = []
    all_tool_sequences = []
    all_error_sequences = []
    total_events = 0
    
    for session in improvements:
        all_patterns.extend(session.get('patterns', []))
        all_tool_sequences.extend(session.get('tool_sequences', []))
        all_error_sequences.extend(session.get('error_sequences', []))
        total_events += session.get('total_events', 0)
    
    print(f"Total events processed: {total_events}")
    print(f"Patterns detected: {len(all_patterns)}")
    print(f"Tool sequences found: {len(all_tool_sequences)}")
    print(f"Error patterns found: {len(all_error_sequences)}")
    
    # Show top patterns
    if all_patterns:
        print(f"\n🔄 Top Repeated Patterns")
        print(f"{'-'*50}")
        
        # Group similar patterns
        pattern_groups = {}
        for pattern in all_patterns:
            if pattern['type'] == 'tool_sequence':
                key = '->'.join(pattern['sequence'])
                if key not in pattern_groups:
                    pattern_groups[key] = {
                        'count': 0,
                        'pattern': pattern,
                        'sessions': []
                    }
                pattern_groups[key]['count'] += pattern.get('occurrences', 1)
        
        # Sort by total occurrences
        sorted_patterns = sorted(pattern_groups.items(), key=lambda x: x[1]['count'], reverse=True)
        
        for i, (key, data) in enumerate(sorted_patterns[:5], 1):
            pattern = data['pattern']
            print(f"\n{i}. {key}")
            print(f"   Occurrences: {data['count']}")
            if pattern.get('suggested_name'):
                print(f"   Suggested command: /{pattern['suggested_name']}")
            print(f"   Type: Could be a command")
    
    # Show complex workflows (potential agents)
    if all_tool_sequences:
        long_sequences = [s for s in all_tool_sequences if s.get('length', 0) >= 5]
        if long_sequences:
            print(f"\n🤖 Complex Workflows (Potential Agents)")
            print(f"{'-'*50}")
            
            for i, seq in enumerate(long_sequences[:3], 1):
                print(f"\n{i}. Workflow with {seq['length']} steps")
                print(f"   Tools: {' -> '.join(seq['tools'][:5])}")
                if len(seq['tools']) > 5:
                    print(f"   ... and {len(seq['tools']) - 5} more")
                print(f"   Success rate: {seq.get('success_rate', 1.0):.1%}")
                print(f"   Recommendation: Create specialized agent")
    
    # Show error patterns (potential hooks)
    if all_error_sequences:
        print(f"\n⚠️ Error Patterns (Potential Validation Hooks)")
        print(f"{'-'*50}")
        
        for i, error in enumerate(all_error_sequences[:3], 1):
            print(f"\n{i}. Tool: {error.get('tool')}")
            print(f"   Error: {error.get('error', 'Unknown')[:100]}")
            print(f"   Occurrences: {error.get('occurrences', 1)}")
            print(f"   Recommendation: {error.get('recommendation', 'Add validation')}")
    
    # Show session metrics summary
    print(f"\n📈 Session Metrics Summary")
    print(f"{'-'*50}")
    
    total_exec_time = 0
    total_error_count = 0
    tool_usage = Counter()
    
    for session in improvements:
        metrics = session.get('metrics', {})
        total_exec_time += metrics.get('total_execution_time', 0)
        
        # Count tool usage
        for pattern in session.get('patterns', []):
            if pattern['type'] == 'tool_sequence':
                for tool in pattern.get('sequence', []):
                    tool_usage[tool] += pattern.get('occurrences', 1)
    
    print(f"Total execution time: {total_exec_time:.2f} seconds")
    print(f"Most used tools:")
    for tool, count in tool_usage.most_common(5):
        print(f"  • {tool}: {count} times")
    
    # Recommendations
    print(f"\n💡 Recommendations")
    print(f"{'-'*50}")
    
    recommendations = []
    
    if len(all_patterns) > 5:
        recommendations.append("• Run /daily-improve to create commands from repeated patterns")
    
    if long_sequences:
        recommendations.append(f"• Consider creating {len(long_sequences)} specialized agents for complex workflows")
    
    if all_error_sequences:
        recommendations.append(f"• Add {len(all_error_sequences)} validation hooks to prevent errors")
    
    if not recommendations:
        recommendations.append("• Continue using Claude Code to collect more patterns")
        recommendations.append("• Patterns are identified when sequences repeat 2+ times")
    
    for rec in recommendations:
        print(rec)
    
    print(f"\n✨ Run /daily-improve to automatically create improvements")

if __name__ == "__main__":
    view_improvements()