#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "numpy>=1.24.0",
#     "scikit-learn>=1.3.0",
#     "pandas>=2.0.0",
#     "python-dateutil>=2.8.0",
# ]
# ///

"""
ABOUTME: Core log analysis engine for Claude Code hook logs.
ABOUTME: Provides pattern detection, performance analysis, and cross-project learning capabilities.
"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
import hashlib

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


@dataclass
class LogEvent:
    """Structured representation of a log event."""
    event_type: str
    session_id: str
    timestamp: str
    data: Dict[str, Any]
    metrics: Optional[Dict[str, float]] = None
    project_path: Optional[str] = None
    
    def __post_init__(self):
        if self.metrics is None:
            self.metrics = {}
    
    @property
    def datetime(self) -> datetime:
        """Convert timestamp to datetime object."""
        try:
            return datetime.fromisoformat(self.timestamp.replace('Z', '+00:00'))
        except:
            return datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)


class PatternDetector:
    """Detects patterns in log events for optimization opportunities."""
    
    def __init__(self):
        self.command_timings = defaultdict(list)
        self.agent_success_rates = defaultdict(list)
        self.session_patterns = defaultdict(list)
        self.recent_events = deque(maxlen=1000)  # Keep recent events for real-time analysis
        
    def analyze_event(self, event: LogEvent) -> Dict[str, Any]:
        """Analyze a single event for patterns."""
        self.recent_events.append(event)
        
        analysis = {
            'performance_issues': self._detect_performance_issues(event),
            'error_patterns': self._detect_error_patterns(event),
            'success_indicators': self._detect_success_indicators(event),
            'anomalies': self._detect_anomalies(event)
        }
        
        return analysis
    
    def _detect_performance_issues(self, event: LogEvent) -> List[Dict[str, Any]]:
        """Detect performance-related issues."""
        issues = []
        
        # Check tool execution time
        if event.event_type == 'tool_use' and event.metrics:
            execution_time = event.metrics.get('execution_time', 0)
            tool_name = event.data.get('tool_name', 'unknown')
            
            # Track historical timings
            self.command_timings[tool_name].append(execution_time)
            
            # Calculate baseline (median of recent executions)
            recent_timings = self.command_timings[tool_name][-20:]  # Last 20 executions
            if len(recent_timings) > 5:
                baseline = np.median(recent_timings)
                if execution_time > baseline * 2:  # More than 2x slower than baseline
                    issues.append({
                        'type': 'slow_tool_execution',
                        'tool_name': tool_name,
                        'execution_time': execution_time,
                        'baseline': baseline,
                        'severity': 'high' if execution_time > baseline * 3 else 'medium'
                    })
        
        return issues
    
    def _detect_error_patterns(self, event: LogEvent) -> List[Dict[str, Any]]:
        """Detect recurring error patterns."""
        errors = []
        
        if event.event_type == 'tool_use' and event.data.get('error'):
            error_msg = event.data['error']
            tool_name = event.data.get('tool_name', 'unknown')
            
            # Check for repeated errors in recent events
            similar_errors = [
                e for e in self.recent_events 
                if (e.event_type == 'tool_use' and 
                    e.data.get('error') and
                    self._similarity_score(e.data['error'], error_msg) > 0.8)
            ]
            
            if len(similar_errors) > 3:  # Same error occurred 3+ times recently
                errors.append({
                    'type': 'recurring_error',
                    'tool_name': tool_name,
                    'error_message': error_msg,
                    'occurrence_count': len(similar_errors),
                    'severity': 'high'
                })
        
        return errors
    
    def _detect_success_indicators(self, event: LogEvent) -> List[Dict[str, Any]]:
        """Detect patterns that indicate success."""
        successes = []
        
        # Detect successful agent completions
        if event.event_type == 'agent_complete':
            agent_name = event.data.get('agent_name', 'unknown')
            success = event.data.get('success', False)
            
            self.agent_success_rates[agent_name].append(success)
            
            # If agent has consistently high success rate, mark as successful pattern
            recent_successes = self.agent_success_rates[agent_name][-10:]
            if len(recent_successes) >= 5:
                success_rate = sum(recent_successes) / len(recent_successes)
                if success_rate > 0.8:
                    successes.append({
                        'type': 'high_success_agent',
                        'agent_name': agent_name,
                        'success_rate': success_rate,
                        'sample_size': len(recent_successes)
                    })
        
        return successes
    
    def _detect_anomalies(self, event: LogEvent) -> List[Dict[str, Any]]:
        """Detect anomalous patterns using statistical methods."""
        anomalies = []
        
        # Simple anomaly detection based on session length
        if event.event_type == 'session_end':
            session_duration = event.metrics.get('session_duration', 0)
            
            # Collect recent session durations
            recent_durations = [
                e.metrics.get('session_duration', 0) 
                for e in self.recent_events 
                if e.event_type == 'session_end' and e.metrics
            ]
            
            if len(recent_durations) > 10:
                durations_array = np.array(recent_durations).reshape(-1, 1)
                
                # Use Isolation Forest for anomaly detection
                iso_forest = IsolationForest(contamination=0.1, random_state=42)
                iso_forest.fit(durations_array)
                
                is_anomaly = iso_forest.predict([[session_duration]])[0] == -1
                
                if is_anomaly:
                    anomalies.append({
                        'type': 'unusual_session_duration',
                        'session_duration': session_duration,
                        'baseline_median': np.median(recent_durations),
                        'severity': 'medium'
                    })
        
        return anomalies
    
    def _similarity_score(self, text1: str, text2: str) -> float:
        """Calculate similarity between two text strings."""
        # Simple hash-based similarity for error messages
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0


class CrossProjectLearner:
    """Learns patterns across multiple projects for better recommendations."""
    
    def __init__(self, global_logs_path: str):
        self.global_logs_path = Path(global_logs_path)
        self.project_patterns = {}
        self.global_success_patterns = []
        
    def discover_project_logs(self) -> List[Path]:
        """Discover log directories across all projects."""
        log_dirs = []
        
        # Check the main digital garden logs
        if self.global_logs_path.exists():
            log_dirs.append(self.global_logs_path)
        
        # Look for other project log directories
        # This could be enhanced to search more broadly
        for path in self.global_logs_path.parent.rglob('logs'):
            if path.is_dir() and path != self.global_logs_path:
                log_dirs.append(path)
        
        return log_dirs
    
    def learn_from_all_projects(self) -> Dict[str, Any]:
        """Extract patterns from all discovered projects."""
        all_patterns = {
            'successful_command_sequences': [],
            'effective_agent_combinations': [],
            'optimal_prompt_patterns': [],
            'performance_benchmarks': {}
        }
        
        for log_dir in self.discover_project_logs():
            project_patterns = self._analyze_project_logs(log_dir)
            self._merge_patterns(all_patterns, project_patterns)
        
        return all_patterns
    
    def _analyze_project_logs(self, log_dir: Path) -> Dict[str, Any]:
        """Analyze logs from a single project."""
        patterns = {
            'successful_command_sequences': [],
            'effective_agent_combinations': [],
            'optimal_prompt_patterns': [],
            'performance_benchmarks': {}
        }
        
        # Read various log files
        for log_file in log_dir.glob('*.json'):
            try:
                with open(log_file) as f:
                    log_data = json.load(f)
                
                if log_file.name == 'user_prompt_submit.json':
                    patterns['optimal_prompt_patterns'].extend(
                        self._extract_prompt_patterns(log_data)
                    )
                elif log_file.name == 'post_tool_use.json':
                    patterns['successful_command_sequences'].extend(
                        self._extract_command_sequences(log_data)
                    )
                    
            except (json.JSONDecodeError, FileNotFoundError):
                continue
        
        return patterns
    
    def _extract_prompt_patterns(self, log_data: List[Dict]) -> List[Dict[str, Any]]:
        """Extract successful prompt patterns."""
        patterns = []
        
        # Group prompts by session and analyze success
        session_groups = defaultdict(list)
        for entry in log_data:
            if isinstance(entry, dict) and 'session_id' in entry:
                session_groups[entry['session_id']].append(entry)
        
        # Analyze each session for success indicators
        for session_id, session_entries in session_groups.items():
            if len(session_entries) > 1:  # Multi-turn sessions
                # Look for patterns in successful sessions
                # (This would need more sophisticated analysis)
                patterns.append({
                    'session_id': session_id,
                    'prompt_count': len(session_entries),
                    'patterns': self._identify_prompt_patterns(session_entries)
                })
        
        return patterns
    
    def _extract_command_sequences(self, log_data: List[Dict]) -> List[Dict[str, Any]]:
        """Extract successful command sequences."""
        sequences = []
        
        # Group by session and extract command sequences
        session_groups = defaultdict(list)
        for entry in log_data:
            if isinstance(entry, dict) and 'session_id' in entry:
                session_groups[entry['session_id']].append(entry)
        
        for session_id, session_entries in session_groups.items():
            if len(session_entries) >= 3:  # Meaningful sequences
                command_sequence = [
                    entry.get('tool_name', 'unknown') 
                    for entry in session_entries
                ]
                
                sequences.append({
                    'session_id': session_id,
                    'command_sequence': command_sequence,
                    'success_indicators': self._calculate_success_score(session_entries)
                })
        
        return sequences
    
    def _identify_prompt_patterns(self, session_entries: List[Dict]) -> List[str]:
        """Identify patterns in prompt structure."""
        patterns = []
        
        for entry in session_entries:
            prompt = entry.get('prompt', '')
            
            # Look for common successful patterns
            if len(prompt) > 100 and 'specific' in prompt.lower():
                patterns.append('detailed_specific_request')
            if 'example' in prompt.lower():
                patterns.append('includes_example')
            if any(word in prompt.lower() for word in ['test', 'verify', 'validate']):
                patterns.append('includes_validation')
        
        return list(set(patterns))
    
    def _calculate_success_score(self, session_entries: List[Dict]) -> float:
        """Calculate a success score for a session."""
        # Simple heuristic: fewer errors and shorter overall time = higher success
        error_count = sum(1 for entry in session_entries if entry.get('error'))
        total_time = sum(entry.get('execution_time', 0) for entry in session_entries)
        
        # Normalize scores (this would need more sophisticated scoring)
        error_penalty = error_count * 0.2
        time_penalty = min(total_time / 10.0, 1.0)  # Penalize very long sessions
        
        return max(0.0, 1.0 - error_penalty - time_penalty)
    
    def _merge_patterns(self, all_patterns: Dict, project_patterns: Dict):
        """Merge patterns from a single project into global patterns."""
        for key in all_patterns:
            if key in project_patterns:
                if isinstance(all_patterns[key], list):
                    all_patterns[key].extend(project_patterns[key])
                elif isinstance(all_patterns[key], dict):
                    all_patterns[key].update(project_patterns[key])


class LogAnalyzer:
    """Main log analyzer that coordinates all analysis components."""
    
    def __init__(self, global_logs_path: str = "/Users/joshuaoliphant/Library/CloudStorage/Dropbox/python_workspace/digital_garden/logs"):
        self.pattern_detector = PatternDetector()
        self.cross_project_learner = CrossProjectLearner(global_logs_path)
        self.analysis_history = []
        
    def analyze_log_file(self, log_file_path: str) -> Dict[str, Any]:
        """Analyze a single log file."""
        log_path = Path(log_file_path)
        
        if not log_path.exists():
            return {'error': f'Log file not found: {log_file_path}'}
        
        try:
            with open(log_path) as f:
                log_data = json.load(f)
            
            # Convert log entries to LogEvent objects
            events = []
            for entry in log_data:
                if isinstance(entry, dict):
                    event = LogEvent(
                        event_type=entry.get('event_type', 'unknown'),
                        session_id=entry.get('session_id', 'unknown'),
                        timestamp=entry.get('timestamp', datetime.now().isoformat()),
                        data=entry,
                        metrics=entry.get('metrics', {})
                    )
                    events.append(event)
            
            # Analyze all events
            analysis_results = {
                'file_path': str(log_path),
                'event_count': len(events),
                'analysis_timestamp': datetime.now().isoformat(),
                'patterns': [],
                'recommendations': []
            }
            
            for event in events:
                event_analysis = self.pattern_detector.analyze_event(event)
                if any(event_analysis.values()):  # If any analysis found issues
                    analysis_results['patterns'].append({
                        'event': event.to_dict(),
                        'analysis': event_analysis
                    })
            
            # Generate recommendations based on patterns
            analysis_results['recommendations'] = self._generate_recommendations(
                analysis_results['patterns']
            )
            
            return analysis_results
            
        except (json.JSONDecodeError, Exception) as e:
            return {'error': f'Failed to analyze log file: {str(e)}'}
    
    def analyze_cross_project_patterns(self) -> Dict[str, Any]:
        """Analyze patterns across all projects."""
        return self.cross_project_learner.learn_from_all_projects()
    
    def _generate_recommendations(self, patterns: List[Dict]) -> List[Dict[str, Any]]:
        """Generate actionable recommendations based on detected patterns."""
        recommendations = []
        
        # Group patterns by type
        pattern_groups = defaultdict(list)
        for pattern in patterns:
            analysis = pattern['analysis']
            for category, issues in analysis.items():
                if issues:
                    pattern_groups[category].extend(issues)
        
        # Generate recommendations for each pattern type
        for category, issues in pattern_groups.items():
            if category == 'performance_issues':
                recommendations.extend(self._recommend_performance_fixes(issues))
            elif category == 'error_patterns':
                recommendations.extend(self._recommend_error_fixes(issues))
            elif category == 'success_indicators':
                recommendations.extend(self._recommend_success_amplification(issues))
        
        return recommendations
    
    def _recommend_performance_fixes(self, issues: List[Dict]) -> List[Dict[str, Any]]:
        """Generate recommendations for performance issues."""
        recommendations = []
        
        for issue in issues:
            if issue['type'] == 'slow_tool_execution':
                recommendations.append({
                    'type': 'performance_optimization',
                    'priority': issue['severity'],
                    'tool_name': issue['tool_name'],
                    'recommendation': f"Tool '{issue['tool_name']}' is running {issue['execution_time']:.2f}s, "
                                    f"which is {issue['execution_time']/issue['baseline']:.1f}x slower than baseline. "
                                    "Consider optimizing parameters or investigating system constraints.",
                    'action_items': [
                        f"Review {issue['tool_name']} configuration",
                        "Check system resource usage during execution",
                        "Consider caching or optimization strategies"
                    ]
                })
        
        return recommendations
    
    def _recommend_error_fixes(self, issues: List[Dict]) -> List[Dict[str, Any]]:
        """Generate recommendations for error patterns."""
        recommendations = []
        
        for issue in issues:
            if issue['type'] == 'recurring_error':
                recommendations.append({
                    'type': 'error_resolution',
                    'priority': 'high',
                    'tool_name': issue['tool_name'],
                    'recommendation': f"Tool '{issue['tool_name']}' has failed {issue['occurrence_count']} times "
                                    "with similar errors. This suggests a systematic issue.",
                    'error_pattern': issue['error_message'][:200] + "..." if len(issue['error_message']) > 200 else issue['error_message'],
                    'action_items': [
                        "Investigate root cause of recurring error",
                        "Update tool configuration or prompts",
                        "Add error handling or retry logic"
                    ]
                })
        
        return recommendations
    
    def _recommend_success_amplification(self, successes: List[Dict]) -> List[Dict[str, Any]]:
        """Generate recommendations to amplify successful patterns."""
        recommendations = []
        
        for success in successes:
            if success['type'] == 'high_success_agent':
                recommendations.append({
                    'type': 'success_amplification',
                    'priority': 'medium',
                    'agent_name': success['agent_name'],
                    'recommendation': f"Agent '{success['agent_name']}' has a {success['success_rate']:.1%} success rate. "
                                    "Consider applying its patterns to other agents.",
                    'action_items': [
                        f"Analyze {success['agent_name']} prompts and configuration",
                        "Identify transferable success patterns",
                        "Update other agents with similar patterns"
                    ]
                })
        
        return recommendations


def main():
    """Main entry point for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Analyze Claude Code hook logs')
    parser.add_argument('--log-file', help='Specific log file to analyze')
    parser.add_argument('--cross-project', action='store_true', 
                       help='Analyze patterns across all projects')
    parser.add_argument('--output', help='Output file for analysis results')
    
    args = parser.parse_args()
    
    analyzer = LogAnalyzer()
    
    if args.cross_project:
        results = analyzer.analyze_cross_project_patterns()
    elif args.log_file:
        results = analyzer.analyze_log_file(args.log_file)
    else:
        print("Please specify either --log-file or --cross-project")
        return
    
    # Output results
    output_text = json.dumps(results, indent=2)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output_text)
        print(f"Analysis results written to {args.output}")
    else:
        print(output_text)


if __name__ == '__main__':
    main()