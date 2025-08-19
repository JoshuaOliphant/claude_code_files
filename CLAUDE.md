# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is LaBoeuf's personal Claude Code configuration repository containing custom commands, hooks, and subagents that manage Claude Code's behavior through a deterministic hooks system.

## Key Commands

### Hook Development & Testing
```bash
# Test hooks locally with sample input
uv run python hooks/pre_tool_use.py
uv run python hooks/post_tool_use.py
uv run python hooks/enhanced_post_tool_use.py
uv run python hooks/user_prompt_submit.py --log-only
uv run python hooks/notifications.py --notify
uv run python hooks/stop.py --chat
uv run python hooks/subagent_stop.py

# View hook execution logs (JSON format)
ls -la logs/
tail -f logs/hook_*.json

# Test hook integration with Claude Code
claude --debug  # Run with debug output to see hook execution
```

### Subagent Management
```bash
# List available subagents
ls agents/

# Test subagent with Task tool
# Use Task tool with subagent_type parameter matching agent name
```

## Architecture

### Hooks System (`/hooks/`)
Python-based lifecycle hooks that intercept and control Claude Code operations:

- **pre_tool_use.py**: Validates tool usage before execution, implements safety checks
- **enhanced_post_tool_use.py**: Advanced logging and validation after tool completion
- **user_prompt_submit.py**: Captures and logs user interactions
- **session_start.py**: Initializes new sessions with context
- **notifications.py**: Handles AI notifications with optional system alerts
- **stop.py** & **subagent_stop.py**: Manage response and task completion
- **pre_compact.py**: Handles context compaction events

Hook utilities in `/hooks/utils/`:
- **llm/**: LLM integration helpers (anth.py for Anthropic, oai.py for OpenAI)
- **tts/**: Text-to-speech integration (elevenlabs_tts.py)

### Custom Commands (`/commands/`)
Markdown templates activated via `/command_name`:

**Planning & Development**:
- `epcc.md`: Explore-Plan-Code-Commit workflow with TDD integration
- `plan.md`, `plan-tdd.md`, `plan-gh.md`: Various planning approaches
- `tdd.md`: Test-Driven Development workflow

**GitHub Integration**:
- `gh-issue.md`: Create GitHub issues
- `pr-comments.md`: Analyze and respond to PR comments

**Analysis & Review**:
- `security-review.md`: Security vulnerability analysis
- `analyze-logs.md`: Log file analysis

### Subagents (`/agents/`)
Specialized agents with focused responsibilities and tool permissions:

**Core Development**:
- `coder`: Implementation with container tools
- `test-writer`: TDD test creation with container tools
- `planner`: Strategic planning with read-only tools
- `investigator`: Research and exploration with read-only tools

**Version Control**:
- `committer`: Git operations with git MCP tools
- `pr-drafter`: Pull request creation with git tools

**Quality & Documentation**:
- `linter`: Python linting with Ruff in containers
- `hook-creator`: Claude Code hook development
- `meta-agent`: Creates new subagent configurations

**Specialized**:
- `screenshot`: Browser automation with Puppeteer MCP tools
- `uv-script-creator`: Single-file Python scripts with PEP 723

### Configuration (`settings.json`)
Defines hook bindings and tool permissions:
- Allowed tools include common file operations, uv commands, npm
- Each hook type maps to specific Python scripts
- Permissions system controls tool access

## Development Patterns

### Python Package Management
All Python development uses `uv` exclusively:
```bash
# Install dependencies
uv pip install package_name

# Run Python scripts
uv run python script.py

# Create single-file scripts with inline dependencies (PEP 723)
uv run script.py  # Dependencies auto-installed from script metadata
```

### Hook Development Workflow
1. Create/modify hook in `/hooks/` directory
2. Add hook configuration to `settings.json`
3. Test locally: `uv run python hooks/hook_name.py`
4. Verify JSON logging in `/logs/` directory
5. Test integration with `claude --debug`

### Custom Command Creation
1. Create markdown file in `/commands/`
2. Use `$ARGUMENTS` placeholder for user input
3. Structure with clear phases and instructions
4. Test availability with `/` prefix in Claude Code

### Subagent Development
1. Create agent markdown in `/agents/`
2. Define YAML frontmatter with name, description, tools, color
3. Specify appropriate MCP tools based on agent purpose
4. Use systematic thinking frameworks for complex agents
5. Test with Task tool using subagent_type parameter

## EPCC Workflow (Explore-Plan-Code-Commit)

The primary development workflow defined in `/commands/epcc.md`:

1. **Explore** (investigator agent): Research and understand the problem space
2. **Plan** (planner agent): Create detailed implementation strategy
3. **Test-Driven Development**:
   - Write failing tests (test-writer agent)
   - Implement code (coder agent)
   - Iterate until all tests pass (max 10 iterations)
   - Refactor while maintaining green tests
4. **Lint** (linter agent): Ensure code quality with Ruff
5. **Commit** (committer agent): Create atomic commits with conventional messages
6. **Pull Request** (pr-drafter agent): Create comprehensive PR descriptions

## Hook Execution Flow

1. **UserPromptSubmit**: Logs user input
2. **PreToolUse**: Validates tool safety before execution
3. Tool execution occurs
4. **PostToolUse**: Logs results and validates completion
5. **Notification**: Handles AI notifications
6. **Stop/SubagentStop**: Manages completion
7. **PreCompact**: Handles context management
8. **SessionStart**: Initializes new sessions

## Logging & Debugging

- Hook logs stored in `/logs/` as JSON files
- Each hook execution creates timestamped log entry
- Use `claude --debug` to see real-time hook execution
- Review logs for troubleshooting: `tail -f logs/hook_*.json`

## Security Considerations

- Hooks execute with full user permissions
- Pre-execution validation implemented in `pre_tool_use.py`
- Tool permissions configured in `settings.json`
- Comprehensive audit trail via JSON logging
- Never store credentials in configuration files

## Knowledge Management System

Claude Code now includes an integrated knowledge management system that provides:

### Features
- **Persistent Context**: Session information survives Claude Code restarts
- **Knowledge Accumulation**: Patterns, decisions, and insights build over time
- **Agent Integration**: All agents can read and write to the knowledge base
- **Project Intelligence**: Claude understands your project deeply through accumulated knowledge

### Project Initialization
When starting work on a new project:
1. Claude will detect if the project needs initialization
2. Run `/project-init` to create the knowledge structure
3. The system creates `.claude/` directory with organized subdirectories

### Knowledge Structure
```
<project-root>/.claude/
├── PROJECT_CLAUDE.md    # Project-specific configuration
├── doc/                 # Documentation and plans
│   ├── plans/          # Implementation plans
│   ├── research/       # Research findings
│   └── implementation/ # Implementation notes
├── sessions/           # Session management
│   ├── active/        # Current work sessions
│   └── archive/       # Historical sessions
├── knowledge/         # Accumulated knowledge
│   ├── patterns/      # Code patterns and solutions
│   ├── decisions/     # Technical decisions
│   └── testing/       # Test strategies
└── templates/         # Project templates
```

### How Agents Use Knowledge
- **Investigator**: Stores research findings and discovered patterns
- **Planner**: Saves implementation plans and architectural decisions
- **Coder**: Tracks implementation progress and coding patterns
- **Test-writer**: Documents test patterns and strategies
- **Committer**: Logs technical decisions with commit references
- **Meta-agent**: Includes knowledge instructions in new agents

### Session Management
- Sessions track work progress within a project
- Active sessions load automatically on Claude Code startup
- Old sessions archive automatically after 7 days
- Session contexts persist across Claude Code restarts

### Best Practices
- Commit `.claude/knowledge/` to share team insights
- Keep `.claude/sessions/` in .gitignore for privacy
- Review accumulated patterns periodically
- Update PROJECT_CLAUDE.md as conventions evolve

- Don't leave dangling, unused code behind. If you see something that needs to be cleaned up, then clean it up.
- gpt-5 models exist, including gpt-5-nano.