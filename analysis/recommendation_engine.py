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
ABOUTME: Recommendation engine for automatically improving Claude Code commands, agents, and prompts.
ABOUTME: Uses pattern analysis and machine learning to suggest optimizations based on historical performance.
"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter
import re

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity

from log_analyzer import LogAnalyzer, LogEvent


@dataclass
class Recommendation:
    """Represents a recommendation for improvement."""
    recommendation_type: str  # 'command_optimization', 'agent_improvement', 'prompt_enhancement'
    target: str  # The specific command, agent, or prompt file
    priority: str  # 'low', 'medium', 'high', 'critical'
    title: str
    description: str
    rationale: str
    implementation_steps: List[str]
    expected_impact: str
    confidence_score: float  # 0.0 to 1.0
    supporting_data: Dict[str, Any]
    timestamp: str
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class CommandOptimizer:
    """Optimizes slash commands based on usage patterns and performance."""
    
    def __init__(self):
        self.command_performance_history = defaultdict(list)
        self.command_usage_patterns = defaultdict(list)
        
    def analyze_commands(self, log_events: List[LogEvent]) -> List[Recommendation]:
        """Analyze command usage and generate optimization recommendations."""
        recommendations = []
        
        # Group events by command
        command_events = defaultdict(list)
        for event in log_events:
            if event.event_type == 'command_execution':
                command_name = event.data.get('command_name', 'unknown')
                command_events[command_name].append(event)
        
        for command_name, events in command_events.items():
            recommendations.extend(self._analyze_single_command(command_name, events))
        
        return recommendations
    
    def _analyze_single_command(self, command_name: str, events: List[LogEvent]) -> List[Recommendation]:
        """Analyze a single command's performance and usage."""
        recommendations = []
        
        # Calculate performance metrics
        execution_times = [
            event.metrics.get('execution_time', 0) 
            for event in events 
            if event.metrics and 'execution_time' in event.metrics
        ]
        
        success_rate = sum(1 for event in events if not event.data.get('error')) / len(events)
        
        # Performance optimization recommendations
        if execution_times:
            avg_execution_time = np.mean(execution_times)
            if avg_execution_time > 30:  # Commands taking more than 30 seconds
                recommendations.append(Recommendation(
                    recommendation_type='command_optimization',
                    target=command_name,
                    priority='high' if avg_execution_time > 60 else 'medium',
                    title=f'Optimize slow command: {command_name}',
                    description=f'Command {command_name} averages {avg_execution_time:.1f} seconds execution time',
                    rationale='Long execution times reduce user productivity and may indicate inefficiencies',
                    implementation_steps=[
                        'Profile command execution to identify bottlenecks',
                        'Optimize heavy operations or add parallelization',
                        'Consider breaking down complex commands into smaller steps',
                        'Add progress indicators for long-running operations'
                    ],
                    expected_impact=f'Could reduce execution time by 30-50%',
                    confidence_score=0.8,
                    supporting_data={
                        'avg_execution_time': avg_execution_time,
                        'max_execution_time': max(execution_times),
                        'sample_size': len(execution_times)
                    },
                    timestamp=datetime.now().isoformat()
                ))
        
        # Success rate optimization recommendations
        if success_rate < 0.8:  # Less than 80% success rate
            error_patterns = self._analyze_error_patterns(events)
            
            recommendations.append(Recommendation(
                recommendation_type='command_optimization',
                target=command_name,
                priority='high',
                title=f'Improve reliability of {command_name}',
                description=f'Command {command_name} has {success_rate:.1%} success rate',
                rationale='Low success rates indicate reliability issues that frustrate users',
                implementation_steps=[
                    'Analyze common error patterns and root causes',
                    'Add better error handling and recovery logic',
                    'Improve input validation and user guidance',
                    'Add retry mechanisms for transient failures'
                ],
                expected_impact=f'Could improve success rate to >90%',
                confidence_score=0.9,
                supporting_data={
                    'success_rate': success_rate,
                    'total_executions': len(events),
                    'error_patterns': error_patterns
                },
                timestamp=datetime.now().isoformat()
            ))
        
        # Usage pattern recommendations
        usage_recommendations = self._analyze_usage_patterns(command_name, events)
        recommendations.extend(usage_recommendations)
        
        return recommendations
    
    def _analyze_error_patterns(self, events: List[LogEvent]) -> List[Dict[str, Any]]:
        """Analyze error patterns in command executions."""
        errors = [event.data.get('error', '') for event in events if event.data.get('error')]
        
        if not errors:
            return []
        
        # Group similar errors
        error_groups = defaultdict(list)
        for error in errors:
            # Simple grouping by first few words
            error_key = ' '.join(error.split()[:5])
            error_groups[error_key].append(error)
        
        patterns = []
        for error_key, error_list in error_groups.items():
            if len(error_list) > 1:  # Only report recurring errors
                patterns.append({
                    'error_pattern': error_key,
                    'occurrence_count': len(error_list),
                    'percentage': len(error_list) / len(errors) * 100
                })
        
        return patterns
    
    def _analyze_usage_patterns(self, command_name: str, events: List[LogEvent]) -> List[Recommendation]:
        """Analyze usage patterns and suggest improvements."""
        recommendations = []
        
        # Analyze time-based usage patterns
        timestamps = [event.datetime for event in events]
        if len(timestamps) > 5:
            # Check for clustering of usage times
            hours = [ts.hour for ts in timestamps]
            hour_counts = Counter(hours)
            peak_hours = [hour for hour, count in hour_counts.most_common(3)]
            
            if len(set(peak_hours)) <= 2:  # Usage concentrated in specific hours
                recommendations.append(Recommendation(
                    recommendation_type='command_optimization',
                    target=command_name,
                    priority='low',
                    title=f'Optimize {command_name} for peak usage times',
                    description=f'Command usage concentrated during hours {peak_hours}',
                    rationale='Commands used during specific times might benefit from time-aware optimizations',
                    implementation_steps=[
                        'Consider pre-warming caches during off-peak hours',
                        'Optimize for common use cases during peak times',
                        'Add time-based performance monitoring'
                    ],
                    expected_impact='Improved performance during peak usage',
                    confidence_score=0.6,
                    supporting_data={
                        'peak_hours': peak_hours,
                        'usage_distribution': dict(hour_counts)
                    },
                    timestamp=datetime.now().isoformat()
                ))
        
        return recommendations


class AgentOptimizer:
    """Optimizes agent prompts and configurations based on success patterns."""
    
    def __init__(self, agents_dir: str = "agents"):
        self.agents_dir = Path(agents_dir)
        self.success_patterns = defaultdict(list)
        self.failure_patterns = defaultdict(list)
        
    def analyze_agents(self, log_events: List[LogEvent]) -> List[Recommendation]:
        """Analyze agent performance and generate improvement recommendations."""
        recommendations = []
        
        # Group events by agent
        agent_events = defaultdict(list)
        for event in log_events:
            if event.event_type == 'agent_execution':
                agent_name = event.data.get('agent_name', 'unknown')
                agent_events[agent_name].append(event)
        
        for agent_name, events in agent_events.items():
            recommendations.extend(self._analyze_single_agent(agent_name, events))
        
        return recommendations
    
    def _analyze_single_agent(self, agent_name: str, events: List[LogEvent]) -> List[Recommendation]:
        """Analyze a single agent's performance."""
        recommendations = []
        
        # Calculate success metrics
        successful_events = [e for e in events if not e.data.get('error')]
        failed_events = [e for e in events if e.data.get('error')]
        
        success_rate = len(successful_events) / len(events) if events else 0
        
        # Analyze prompt patterns
        if self.agents_dir.exists():
            agent_file = self.agents_dir / f"{agent_name}.md"
            if agent_file.exists():
                recommendations.extend(self._analyze_agent_prompt(agent_name, agent_file, success_rate, events))
        
        # Performance-based recommendations
        if success_rate < 0.7:  # Less than 70% success rate
            recommendations.append(self._create_success_improvement_recommendation(
                agent_name, success_rate, successful_events, failed_events
            ))
        
        return recommendations
    
    def _analyze_agent_prompt(self, agent_name: str, agent_file: Path, success_rate: float, events: List[LogEvent]) -> List[Recommendation]:
        """Analyze agent prompt for improvement opportunities."""
        recommendations = []
        
        try:
            with open(agent_file) as f:
                content = f.read()
            
            # Extract prompt sections
            prompt_sections = self._extract_prompt_sections(content)
            
            # Analyze prompt quality
            quality_issues = self._analyze_prompt_quality(prompt_sections)
            
            if quality_issues:
                recommendations.append(Recommendation(
                    recommendation_type='agent_improvement',
                    target=agent_name,
                    priority='medium',
                    title=f'Improve prompt quality for {agent_name}',
                    description='Detected potential improvements in agent prompt structure',
                    rationale='Better prompts lead to more consistent and accurate agent performance',
                    implementation_steps=self._generate_prompt_improvement_steps(quality_issues),
                    expected_impact='Could improve success rate by 10-20%',
                    confidence_score=0.7,
                    supporting_data={
                        'current_success_rate': success_rate,
                        'quality_issues': quality_issues,
                        'total_executions': len(events)
                    },
                    timestamp=datetime.now().isoformat()
                ))
        
        except FileNotFoundError:
            pass
        
        return recommendations
    
    def _extract_prompt_sections(self, content: str) -> Dict[str, str]:
        """Extract different sections of an agent prompt."""
        sections = {}
        
        # Extract sections based on markdown headers
        current_section = 'header'
        current_content = []
        
        for line in content.split('\n'):
            if line.startswith('#'):
                if current_content:
                    sections[current_section] = '\n'.join(current_content)
                current_section = line.strip('# ').lower().replace(' ', '_')
                current_content = []
            else:
                current_content.append(line)
        
        if current_content:
            sections[current_section] = '\n'.join(current_content)
        
        return sections
    
    def _analyze_prompt_quality(self, sections: Dict[str, str]) -> List[str]:
        """Analyze prompt quality and identify issues."""
        issues = []
        
        # Check for common prompt quality issues
        full_text = ' '.join(sections.values())
        
        # Check length
        if len(full_text) < 200:
            issues.append('prompt_too_short')
        elif len(full_text) > 5000:
            issues.append('prompt_too_long')
        
        # Check for specific instructions
        if 'example' not in full_text.lower():
            issues.append('lacks_examples')
        
        if not any(word in full_text.lower() for word in ['must', 'should', 'always', 'never']):
            issues.append('lacks_clear_directives')
        
        # Check for output format specification
        if not any(word in full_text.lower() for word in ['format', 'structure', 'output', 'response']):
            issues.append('unclear_output_format')
        
        # Check for role definition
        if 'you are' not in full_text.lower() and 'your role' not in full_text.lower():
            issues.append('unclear_role_definition')
        
        return issues
    
    def _generate_prompt_improvement_steps(self, quality_issues: List[str]) -> List[str]:
        """Generate improvement steps based on quality issues."""
        steps = []
        
        issue_to_steps = {
            'prompt_too_short': 'Add more detailed instructions and context',
            'prompt_too_long': 'Simplify and focus on core requirements',
            'lacks_examples': 'Add concrete examples of expected input/output',
            'lacks_clear_directives': 'Add clear must/should statements for behavior',
            'unclear_output_format': 'Specify expected output format and structure',
            'unclear_role_definition': 'Clearly define the agent\'s role and expertise'
        }
        
        for issue in quality_issues:
            if issue in issue_to_steps:
                steps.append(issue_to_steps[issue])
        
        return steps
    
    def _create_success_improvement_recommendation(self, agent_name: str, success_rate: float, 
                                                 successful_events: List[LogEvent], failed_events: List[LogEvent]) -> Recommendation:
        """Create recommendation to improve agent success rate."""
        
        # Analyze failure patterns
        failure_analysis = self._analyze_failure_patterns(failed_events)
        
        return Recommendation(
            recommendation_type='agent_improvement',
            target=agent_name,
            priority='high',
            title=f'Improve {agent_name} success rate',
            description=f'Agent has {success_rate:.1%} success rate with {len(failed_events)} failures',
            rationale='Low success rates indicate issues with agent prompt or configuration',
            implementation_steps=[
                'Analyze failure patterns and common error types',
                'Review and refine agent prompt based on failure analysis',
                'Add better error handling and fallback strategies',
                'Test improvements with historical failure cases'
            ],
            expected_impact=f'Could improve success rate to >85%',
            confidence_score=0.8,
            supporting_data={
                'current_success_rate': success_rate,
                'failure_count': len(failed_events),
                'success_count': len(successful_events),
                'failure_analysis': failure_analysis
            },
            timestamp=datetime.now().isoformat()
        )
    
    def _analyze_failure_patterns(self, failed_events: List[LogEvent]) -> Dict[str, Any]:
        """Analyze patterns in agent failures."""
        if not failed_events:
            return {}
        
        error_messages = [event.data.get('error', '') for event in failed_events]
        error_types = Counter()
        
        for error_msg in error_messages:
            # Categorize errors
            if 'timeout' in error_msg.lower():
                error_types['timeout'] += 1
            elif 'permission' in error_msg.lower():
                error_types['permission'] += 1
            elif 'not found' in error_msg.lower():
                error_types['not_found'] += 1
            elif 'invalid' in error_msg.lower():
                error_types['invalid_input'] += 1
            else:
                error_types['other'] += 1
        
        return {
            'error_type_distribution': dict(error_types),
            'most_common_error_type': error_types.most_common(1)[0][0] if error_types else 'none'
        }


class PromptOptimizer:
    """Optimizes prompts based on success patterns and NLP analysis."""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.successful_prompts = []
        self.failed_prompts = []
        
    def analyze_prompts(self, log_events: List[LogEvent]) -> List[Recommendation]:
        """Analyze prompt patterns and generate optimization recommendations."""
        recommendations = []
        
        # Extract prompts from user submissions
        prompt_events = [
            event for event in log_events 
            if event.event_type == 'prompt_submit' and event.data.get('prompt')
        ]
        
        if len(prompt_events) < 10:  # Need sufficient data
            return recommendations
        
        # Analyze prompt patterns
        successful_prompts, failed_prompts = self._categorize_prompts(prompt_events)
        
        if successful_prompts and failed_prompts:
            recommendations.extend(self._analyze_prompt_differences(successful_prompts, failed_prompts))
        
        # Analyze prompt structure patterns
        recommendations.extend(self._analyze_prompt_structures(prompt_events))
        
        return recommendations
    
    def _categorize_prompts(self, prompt_events: List[LogEvent]) -> Tuple[List[str], List[str]]:
        """Categorize prompts as successful or failed based on subsequent events."""
        successful_prompts = []
        failed_prompts = []
        
        # Group events by session to determine success
        session_groups = defaultdict(list)
        for event in prompt_events:
            session_groups[event.session_id].append(event)
        
        for session_id, events in session_groups.items():
            for event in events:
                prompt_text = event.data.get('prompt', '')
                if len(prompt_text) < 20:  # Skip very short prompts
                    continue
                
                # Determine success based on subsequent events or session outcome
                # This is a simplification - in practice, you'd need more sophisticated success detection
                session_success = self._determine_session_success(session_id, event)
                
                if session_success:
                    successful_prompts.append(prompt_text)
                else:
                    failed_prompts.append(prompt_text)
        
        return successful_prompts, failed_prompts
    
    def _determine_session_success(self, session_id: str, prompt_event: LogEvent) -> bool:
        """Determine if a session was successful (simplified heuristic)."""
        # This is a placeholder - real implementation would analyze subsequent events
        # For now, use a simple heuristic based on prompt characteristics
        prompt = prompt_event.data.get('prompt', '')
        
        # Heuristics for success (these would be refined based on actual data)
        success_indicators = [
            len(prompt) > 50,  # Detailed prompts tend to be more successful
            any(word in prompt.lower() for word in ['specific', 'example', 'detailed']),
            '?' in prompt,  # Questions tend to get better responses
        ]
        
        return sum(success_indicators) >= 2
    
    def _analyze_prompt_differences(self, successful_prompts: List[str], failed_prompts: List[str]) -> List[Recommendation]:
        """Analyze differences between successful and failed prompts."""
        recommendations = []
        
        if len(successful_prompts) < 5 or len(failed_prompts) < 5:
            return recommendations
        
        try:
            # Vectorize prompts
            all_prompts = successful_prompts + failed_prompts
            vectors = self.vectorizer.fit_transform(all_prompts)
            
            # Split vectors
            successful_vectors = vectors[:len(successful_prompts)]
            failed_vectors = vectors[len(successful_prompts):]
            
            # Find distinctive features
            successful_mean = np.mean(successful_vectors.toarray(), axis=0)
            failed_mean = np.mean(failed_vectors.toarray(), axis=0)
            
            # Calculate feature differences
            feature_diff = successful_mean - failed_mean
            feature_names = self.vectorizer.get_feature_names_out()
            
            # Get top distinctive features for successful prompts
            top_success_features = np.argsort(feature_diff)[-10:]
            top_success_words = [feature_names[i] for i in top_success_features]
            
            recommendations.append(Recommendation(
                recommendation_type='prompt_enhancement',
                target='general_prompts',
                priority='medium',
                title='Optimize prompt patterns for better success',
                description='Identified words and patterns associated with successful prompts',
                rationale='Successful prompts share common patterns that can be applied more broadly',
                implementation_steps=[
                    f'Include words like: {", ".join(top_success_words[:5])}',
                    'Use more specific and detailed language',
                    'Structure prompts with clear questions',
                    'Provide context and examples when possible'
                ],
                expected_impact='Could improve prompt success rate by 15-25%',
                confidence_score=0.6,
                supporting_data={
                    'successful_prompt_count': len(successful_prompts),
                    'failed_prompt_count': len(failed_prompts),
                    'top_success_words': top_success_words,
                    'analysis_method': 'tf_idf_comparison'
                },
                timestamp=datetime.now().isoformat()
            ))
        
        except Exception as e:
            logging.error(f"Error in prompt difference analysis: {e}")
        
        return recommendations
    
    def _analyze_prompt_structures(self, prompt_events: List[LogEvent]) -> List[Recommendation]:
        """Analyze structural patterns in prompts."""
        recommendations = []
        
        # Analyze prompt length patterns
        prompt_lengths = [len(event.data.get('prompt', '')) for event in prompt_events]
        avg_length = np.mean(prompt_lengths)
        
        if avg_length < 50:  # Very short prompts
            recommendations.append(Recommendation(
                recommendation_type='prompt_enhancement',
                target='general_prompts',
                priority='medium',
                title='Increase prompt detail and specificity',
                description=f'Average prompt length is {avg_length:.1f} characters, which is quite short',
                rationale='More detailed prompts typically yield better results',
                implementation_steps=[
                    'Add more context and background information',
                    'Include specific requirements and constraints',
                    'Provide examples of desired outputs',
                    'Break down complex requests into steps'
                ],
                expected_impact='More detailed prompts lead to better responses',
                confidence_score=0.7,
                supporting_data={
                    'average_prompt_length': avg_length,
                    'sample_size': len(prompt_events)
                },
                timestamp=datetime.now().isoformat()
            ))
        
        return recommendations


class RecommendationEngine:
    """Main recommendation engine that coordinates all optimization components."""
    
    def __init__(self, agents_dir: str = "agents", commands_dir: str = "commands"):
        self.command_optimizer = CommandOptimizer()
        self.agent_optimizer = AgentOptimizer(agents_dir)
        self.prompt_optimizer = PromptOptimizer()
        self.log_analyzer = LogAnalyzer()
        
    def generate_recommendations(self, log_file_path: Optional[str] = None, 
                               cross_project: bool = False) -> List[Recommendation]:
        """Generate all types of recommendations based on log analysis."""
        recommendations = []
        
        # Get log events
        if cross_project:
            # Analyze across all projects
            cross_project_patterns = self.log_analyzer.analyze_cross_project_patterns()
            log_events = self._extract_events_from_patterns(cross_project_patterns)
        elif log_file_path:
            # Analyze specific log file
            analysis_result = self.log_analyzer.analyze_log_file(log_file_path)
            log_events = self._extract_events_from_analysis(analysis_result)
        else:
            # Default to current directory logs
            log_events = self._load_recent_events()
        
        if not log_events:
            return recommendations
        
        # Generate recommendations from each optimizer
        recommendations.extend(self.command_optimizer.analyze_commands(log_events))
        recommendations.extend(self.agent_optimizer.analyze_agents(log_events))
        recommendations.extend(self.prompt_optimizer.analyze_prompts(log_events))
        
        # Sort by priority and confidence
        recommendations.sort(key=lambda r: (
            {'critical': 4, 'high': 3, 'medium': 2, 'low': 1}[r.priority],
            r.confidence_score
        ), reverse=True)
        
        return recommendations
    
    def _extract_events_from_patterns(self, patterns: Dict[str, Any]) -> List[LogEvent]:
        """Extract LogEvent objects from cross-project patterns."""
        # This would need to be implemented based on the actual pattern structure
        # For now, return empty list as placeholder
        return []
    
    def _extract_events_from_analysis(self, analysis_result: Dict[str, Any]) -> List[LogEvent]:
        """Extract LogEvent objects from analysis results."""
        events = []
        
        if 'patterns' in analysis_result:
            for pattern in analysis_result['patterns']:
                if 'event' in pattern:
                    event_data = pattern['event']
                    event = LogEvent(
                        event_type=event_data.get('event_type', 'unknown'),
                        session_id=event_data.get('session_id', 'unknown'),
                        timestamp=event_data.get('timestamp', datetime.now().isoformat()),
                        data=event_data.get('data', {}),
                        metrics=event_data.get('metrics', {})
                    )
                    events.append(event)
        
        return events
    
    def _load_recent_events(self) -> List[LogEvent]:
        """Load recent events from standard log files."""
        events = []
        log_files = ['logs/post_tool_use.json', 'logs/user_prompt_submit.json']
        
        for log_file in log_files:
            try:
                analysis = self.log_analyzer.analyze_log_file(log_file)
                events.extend(self._extract_events_from_analysis(analysis))
            except:
                continue
        
        return events
    
    def save_recommendations(self, recommendations: List[Recommendation], output_file: str):
        """Save recommendations to a file."""
        recommendations_data = {
            'timestamp': datetime.now().isoformat(),
            'recommendation_count': len(recommendations),
            'recommendations': [r.to_dict() for r in recommendations]
        }
        
        with open(output_file, 'w') as f:
            json.dump(recommendations_data, f, indent=2)


def main():
    """Main entry point for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate optimization recommendations')
    parser.add_argument('--log-file', help='Specific log file to analyze')
    parser.add_argument('--cross-project', action='store_true', 
                       help='Analyze across all projects')
    parser.add_argument('--output', help='Output file for recommendations')
    parser.add_argument('--agents-dir', default='agents', help='Agents directory')
    parser.add_argument('--commands-dir', default='commands', help='Commands directory')
    
    args = parser.parse_args()
    
    engine = RecommendationEngine(args.agents_dir, args.commands_dir)
    
    recommendations = engine.generate_recommendations(
        log_file_path=args.log_file,
        cross_project=args.cross_project
    )
    
    if args.output:
        engine.save_recommendations(recommendations, args.output)
        print(f"Generated {len(recommendations)} recommendations, saved to {args.output}")
    else:
        # Print to console
        for i, rec in enumerate(recommendations, 1):
            print(f"\n{i}. [{rec.priority.upper()}] {rec.title}")
            print(f"   Target: {rec.target}")
            print(f"   {rec.description}")
            print(f"   Confidence: {rec.confidence_score:.2f}")


if __name__ == '__main__':
    main()