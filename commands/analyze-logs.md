Analyze Claude Code hook logs to identify performance issues, error patterns, and optimization opportunities. Generate actionable recommendations for improving commands, agents, and prompts.

## Usage Options

### Analyze Recent Activity
```
/analyze-logs
```
Analyzes recent log files from the current project's logs directory.

### Analyze Specific Log File
```
/analyze-logs --file logs/post_tool_use.json
```
Analyzes a specific log file for patterns and issues.

### Cross-Project Analysis
```
/analyze-logs --cross-project
```
Analyzes logs from all projects in the digital garden logs directory to identify patterns across projects.

### Generate Recommendations
```
/analyze-logs --recommendations
```
Generates specific improvement recommendations based on log analysis.

### Real-Time Monitoring
```
/analyze-logs --monitor
```
Starts real-time monitoring of log files with immediate feedback on issues.

## Analysis Features

The log analyzer provides:

1. **Performance Analysis**: Identifies slow commands, tools, and agents
2. **Error Pattern Detection**: Finds recurring errors and failure patterns  
3. **Success Pattern Recognition**: Identifies what works well to replicate success
4. **Anomaly Detection**: Spots unusual patterns that may indicate issues
5. **Cross-Project Learning**: Learns from patterns across all your projects
6. **Automated Recommendations**: Suggests specific improvements with implementation steps

## Output

The analysis provides:
- Performance metrics and bottlenecks
- Error frequency and patterns
- Success indicators and best practices
- Specific recommendations with priority levels
- Implementation steps for improvements
- Confidence scores for recommendations

Use this command regularly to continuously improve your Claude Code setup based on actual usage patterns.