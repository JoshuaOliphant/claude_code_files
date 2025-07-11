# Claude Code Configuration & Hooks

My personal Claude Code configuration repository containing custom commands, hooks, and documentation for enhanced AI-powered development workflows.

## Overview

This repository contains my complete Claude Code setup, including:

- Custom hooks for deterministic control over Claude Code behavior
- Personal coding preferences and standards
- Custom commands for common development tasks
- Documentation and reference materials

## What is Claude Code?

[Claude Code](https://docs.anthropic.com/en/docs/claude-code) is Anthropic's agentic coding tool that helps developers:

- Build features by describing them in plain English
- Debug code by analyzing errors and implementing fixes
- Navigate and understand codebases
- Automate routine tasks like linting and merge conflict resolution

## Repository Structure

```
.claude/
├── CLAUDE.md           # Global user instructions and preferences
├── commands/           # Custom Claude Code commands
├── docs/               # Technology-specific documentation
├── hooks/              # Python hooks for Claude Code lifecycle events
├── logs/               # JSON logs of hook executions
├── projects/           # Project-specific configurations
├── settings.json       # Claude Code settings and hook configurations
└── utils/              # Utility scripts for hooks
```

### Key Components

#### 1. CLAUDE.md - Personal Instructions

The main configuration file that defines:

- How Claude should address me (as "LaBoeuf")
- Our working relationship and communication style
- Coding standards and preferences
- Technology-specific guidelines
- Testing requirements (TDD approach)

#### 2. Hooks System

Implements deterministic control through Python scripts:

- **PreToolUse**: Validates commands before execution
- **PostToolUse**: Logs and validates tool completion
- **Notification**: Handles AI notifications with optional alerts
- **Stop**: Manages response completion
- **SubagentStop**: Handles subagent task completion

#### 3. Custom Commands

Pre-written markdown templates for common tasks:

- `brainstorm.md` - Creative problem-solving sessions
- `plan.md`, `plan-tdd.md`, `plan-gh.md` - Different planning approaches
- `gh-issue.md`, `gh_comment.md` - GitHub integration commands
- `security-review.md` - Security analysis tasks
- `setup.md` - Project initialization

#### 4. Documentation

Technology-specific guidelines:

- `python.md` - Python development with UV package manager
- `source-control.md` - Git commit conventions
- `using-uv.md` - Comprehensive UV field manual

## Features

### Security & Safety

- Pre-execution validation of potentially dangerous commands
- Comprehensive logging of all tool interactions
- Configurable permissions system

### Developer Experience

- Consistent coding standards across all projects
- TDD-focused development workflow
- Automated notifications for important events
- Smart context management through CLAUDE.md imports

### Integration

- Works seamlessly with existing development tools
- Supports project-specific overrides
- Compatible with CI/CD workflows

## Installation & Setup

1. Ensure Claude Code is installed:

   ```bash
   npm install -g @anthropic-ai/claude-code
   ```

2. Clone this repository to `~/.claude`:

   ```bash
   git clone [your-repo-url] ~/.claude
   ```

3. The configuration will be automatically loaded when you run `claude` in any project.

## Usage

Simply run `claude` in your project directory. The configurations will:

- Apply personal preferences from CLAUDE.md
- Enable all configured hooks
- Make custom commands available via the `/command` syntax

### Custom Commands

Use commands by typing `/` followed by the command name:

```
/plan          # Create a development plan
/gh-issue      # Create a GitHub issue
/security      # Run security review
```

### Memory Management

- Project-specific instructions: Create `./CLAUDE.md` in your project
- Import additional files: Use `@path/to/file` syntax in CLAUDE.md
- Quick edit: Use `#` shortcut or `/memory` command

## Customization

### Adding New Hooks

1. Create a Python script in `hooks/`
2. Add the hook configuration to `settings.json`
3. Test thoroughly before enabling

### Creating Commands

1. Add markdown files to `commands/`
2. Use clear, instructive templates
3. Include examples where helpful

## References & Inspiration

This configuration was inspired by:

- [claude-code-hooks-mastery](https://github.com/disler/claude-code-hooks-mastery) - Comprehensive hooks implementation
- [harperreed/dotfiles](https://github.com/harperreed/dotfiles/tree/master/.claude) - Clean configuration structure

## Security Notes

⚠️ **Important**: Hooks execute with full user permissions. Always:

- Review hook code before enabling
- Test in safe environments first
- Keep logs for audit purposes
- Never store sensitive data in configuration files

## Contributing

This is a personal configuration repository, but feel free to:

- Fork and adapt for your own use
- Submit issues for bugs or suggestions
- Share your own configurations and improvements

## License

This repository contains personal configurations and is provided as-is for reference and adaptation.

---

*Built with Claude Code - Anthropic's AI-powered coding assistant*