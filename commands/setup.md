---
description: Initialize project setup and verify configuration
---

# Project Setup & Configuration

I will systematically set up and verify the project configuration.

## Pre-Setup Verification

First, I'll check for essential configuration:
1. **CLAUDE.md Existence**: Verify project has Claude configuration
2. **Project Structure**: Understand the codebase organization
3. **Dependencies**: Check package management setup
4. **Testing Framework**: Identify test runner and configuration

## Setup Actions

### Step 1: Configuration Check
Verify CLAUDE.md exists:
- If missing: Exit and instruct user to run `/init` first
- If present: Proceed with setup enhancements

### Step 2: Python Environment Configuration
If Python project detected, configure `uv` package manager:

```bash
# Package management with uv
uv add <package>           # Add new packages
uv run <script.py>         # Run Python scripts
uv sync                    # Sync dependencies
```

Key points:
- Packages stored in `pyproject.toml` (not requirements.txt)
- Virtual environment managed automatically by uv
- All Python execution through `uv run`

### Step 3: Workflow Integration
Update project workflow files:

**Todo Management**:
- Check for `todo.md` file
- Mark completed items as done
- Add any new tasks discovered during setup

**Documentation**:
- Update CLAUDE.md with project-specific patterns
- Document key commands and workflows
- Note testing and linting requirements

### Step 4: Quality Gates Setup
Establish quality requirements:

**Testing**:
- Identify test command (pytest, npm test, cargo test, etc.)
- Ensure all tests pass before marking tasks complete
- Document test running instructions

**Linting**:
- Identify linting tools (ruff, eslint, etc.)
- Ensure linting passes before task completion
- Configure pre-commit hooks if applicable

### Step 5: Validation Checklist
Confirm setup is complete:

- [ ] CLAUDE.md exists and is configured
- [ ] Package management is set up correctly
- [ ] Test command is documented and working
- [ ] Linting command is documented and working
- [ ] Todo.md is updated if present
- [ ] All dependencies are installed
- [ ] Development environment is ready

## Post-Setup Summary

After setup, I will provide:
1. **Environment Status**: What's configured and ready
2. **Available Commands**: Key development commands
3. **Next Steps**: Recommended actions to begin development
4. **Potential Issues**: Any warnings or setup concerns

## Success Criteria

Setup is complete when:
- Developer can immediately start coding
- All quality gates are functional
- Documentation reflects current state
- No configuration blockers exist

Begin with Pre-Setup Verification.