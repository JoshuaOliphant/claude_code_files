# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Container-Use Instructions

ALWAYS use ONLY Environments for ANY and ALL file, code, or shell operations—NO EXCEPTIONS—even for simple or generic requests.

DO NOT install or use the git cli with the environment_run_cmd tool. All environment tools will handle git operations for you. Changing ".git" yourself will compromise the integrity of your environment.

You MUST inform the user how to view your work using `container-use log <env_id>` AND `container-use checkout <env_id>`. Failure to do this will make your work inaccessible to others.

1. First, create a new isolated development environment:
   ```
   environment_create(
     environment_source="<repository_path>",
     title="<feature_name> Development"
   )
   ```
2. **CRITICAL**: Store the returned environment ID and source path
3. Use these values for ALL subsequent operations and sub-agent instructions

## Repository Overview

This is LaBoeuf's personal Claude Code configuration repository containing custom commands, hooks, and the Claude Analytics Dashboard project. The repository manages Claude Code's behavior through deterministic hooks and provides analytics visualization for Claude Code usage patterns.

## Key Commands

### Dashboard Development
```bash
# Navigate to dashboard
cd dashboard/claude-analytics-dashboard

# Install/sync dependencies using uv
uv sync

# Run the analytics dashboard
uv run python run_dashboard.py

# Run tests (when implemented)
uv run pytest
```

### Hook Management
```bash
# Test hooks locally
uv run python hooks/pre_tool_use.py
uv run python hooks/post_tool_use.py

# View hook logs
ls -la logs/
```

## Architecture

### Core Components

1. **Hooks System** (`/hooks/`): Python-based lifecycle hooks that control Claude Code behavior
   - `pre_tool_use.py`: Validates commands before execution
   - `post_tool_use.py`: Logs tool usage and validates completion
   - `user_prompt_submit.py`: Captures user interactions
   - `session_start.py`: Initializes new sessions
   - `notifications.py`: Handles AI notifications with optional alerts
   - `stop.py` & `subagent_stop.py`: Manage response/task completion

2. **Analytics Dashboard** (`/dashboard/claude-analytics-dashboard/`): FastAPI + Chart.js web application
   - Backend: `backend/main.py` - FastAPI server with WebSocket support
   - Frontend: `frontend/index.html` & `frontend/dashboard.js` - Interactive visualizations
   - Data processing: Reads JSON logs from hooks, calculates metrics, provides real-time updates

3. **Custom Commands** (`/commands/`): Pre-written markdown templates for common workflows
   - Planning: `plan.md`, `plan-tdd.md`, `plan-gh.md`
   - GitHub: `gh-issue.md`, `pr-comments.md`
   - Development: `tdd.md`, `epcc.md` (explore-plan-code-commit)
   - Analysis: `security-review.md`, `analyze-logs.md`

4. **Configuration**:
   - `settings.json`: Hook configurations and tool permissions
   - Global CLAUDE.md: User preferences and coding standards
   - Project-specific overrides via local CLAUDE.md files

### Data Flow

1. User interacts with Claude Code
2. Hooks intercept and log events to JSON files in `/logs/`
3. Dashboard monitors log files using watchdog
4. Real-time updates sent via WebSocket to connected browsers
5. Visualizations update automatically with new data

## Development Workflow

### For Dashboard Features
1. Use TDD approach - write tests first in `dashboard/claude-analytics-dashboard/tests/`
2. Implement features in appropriate backend/frontend files
3. Test locally with `uv run python run_dashboard.py`
4. Verify WebSocket updates work correctly
5. Check responsive design on different screen sizes

### For Hook Development
1. Create/modify hook in `/hooks/` directory
2. Add configuration to `settings.json`
3. Test hook locally with sample input
4. Verify logging works correctly
5. Test integration with Claude Code

### For Custom Commands
1. Create markdown file in `/commands/`
2. Use clear instructions and examples
3. Test command availability with `/` prefix in Claude Code

## Important Patterns

- All Python development uses `uv` for package management (no pip/poetry)
- Hook logs are JSON format in `/logs/` directory
- Dashboard runs on port 8000 by default
- WebSocket fallback to polling for compatibility
- File monitoring uses watchdog for real-time updates

## Testing Requirements

Per the global CLAUDE.md requirements:
- Practice TDD (Test-Driven Development)
- Write failing tests first
- Implement minimal code to pass
- Refactor while keeping tests green
- All projects must have unit, integration, and end-to-end tests

## Security Considerations

- Hooks execute with full user permissions
- Pre-execution validation in `pre_tool_use.py`
- Comprehensive logging for audit trails
- Never store sensitive data in configuration files
- Tool permissions configured in `settings.json`

## Troubleshooting

### Dashboard Issues
- Check dependencies: `uv sync`
- Verify Python 3.11+ installed
- Check port 8000 availability
- Verify log files exist and are valid JSON

### Hook Issues
- Check `settings.json` configuration
- Verify hook scripts are executable
- Review logs for error messages
- Test hooks with sample input data

### WebSocket Issues
- Dashboard automatically falls back to polling
- Check browser console for errors
- Verify firewall settings allow WebSocket connections
- When using the Puppeteer MCP, remember to take screenshots to verify the look and feel of the expected output.