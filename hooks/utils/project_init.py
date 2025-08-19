#!/usr/bin/env python3
"""
Project initialization utilities for Claude Code.
Handles detection and setup of project-specific knowledge structures.
"""

import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple


def get_project_root() -> str:
    """
    Detect project root directory.
    
    Returns:
        Path to project root as string
    """
    # Try git first
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--show-toplevel'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.SubprocessError, FileNotFoundError):
        pass
    
    # Look for project markers
    current = Path.cwd()
    markers = ['package.json', 'pyproject.toml', 'Cargo.toml', 'go.mod', '.git']
    
    while current != current.parent:
        for marker in markers:
            if (current / marker).exists():
                return str(current)
        current = current.parent
    
    # Default to current directory
    return str(Path.cwd())


def get_project_type(project_root: str) -> str:
    """
    Detect project type - simplified for Python/uv and JavaScript.
    
    Args:
        project_root: Path to project root
        
    Returns:
        Project type string: python-uv, javascript-frontend, or unknown
    """
    project_path = Path(project_root)
    
    # Check for Python project (always assume modern uv setup)
    if (project_path / "pyproject.toml").exists() or list(project_path.glob("*.py")):
        return "python-uv"
    
    # JavaScript indicators (for FastAPI frontends)
    elif (project_path / "package.json").exists():
        # Check if it's a frontend project
        try:
            with open(project_path / "package.json") as f:
                content = json.load(f)
                deps = {**content.get("dependencies", {}), **content.get("devDependencies", {})}
                
                # Check for frontend frameworks
                if any(framework in deps for framework in ["react", "vue", "svelte", "next", "@angular/core"]):
                    return "javascript-frontend"
        except (json.JSONDecodeError, FileNotFoundError):
            pass
        return "javascript"
    
    return "unknown"


def is_project_initialized(project_root: str) -> bool:
    """
    Check if the knowledge structure is initialized, not just .claude/ directory.
    
    Args:
        project_root: Path to project root
        
    Returns:
        True if project knowledge structure exists
    """
    required_dirs = [
        ".claude/doc",
        ".claude/sessions/active",
        ".claude/knowledge/patterns"
    ]
    
    for dir_path in required_dirs:
        if not (Path(project_root) / dir_path).exists():
            return False
    
    # Check for our marker file
    project_claude = Path(project_root) / ".claude" / "PROJECT_CLAUDE.md"
    return project_claude.exists()


def initialize_project_structure(project_root: str, project_type: str) -> bool:
    """
    Initialize knowledge structure based on project type.
    
    Args:
        project_root: Path to project root
        project_type: Type of project (python-modern, javascript-frontend, etc.)
        
    Returns:
        True if initialization successful
    """
    try:
        # Create the knowledge directories
        directories = [
            ".claude/doc/plans",
            ".claude/doc/research", 
            ".claude/doc/implementation",
            ".claude/sessions/active",
            ".claude/sessions/archive",
            ".claude/knowledge/patterns",
            ".claude/knowledge/decisions",
            ".claude/knowledge/testing",
            ".claude/templates"
        ]
        
        for dir_path in directories:
            (Path(project_root) / dir_path).mkdir(parents=True, exist_ok=True)
        
        # Create PROJECT_CLAUDE.md based on project type
        create_project_claude_md(project_root, project_type)
        
        # Create appropriate templates
        create_project_templates(project_root, project_type)
        
        # Initialize first session
        create_initial_session(project_root, project_type)
        
        # Update .gitignore
        update_gitignore(project_root)
        
        return True
    except Exception as e:
        print(f"Error initializing project structure: {e}")
        return False


def update_primary_claude_md() -> None:
    """
    Update the primary CLAUDE.md file with knowledge management information.
    This adds a section about the knowledge management system if not already present.
    """
    primary_claude_path = Path.home() / ".claude" / "CLAUDE.md"
    
    if not primary_claude_path.exists():
        return
    
    try:
        content = primary_claude_path.read_text()
        
        # Check if knowledge management section already exists
        if "Knowledge Management System" in content:
            return
        
        # Add knowledge management section
        km_section = """

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
"""
        
        # Append to the file
        with open(primary_claude_path, 'a') as f:
            f.write(km_section)
            
        print(f"Updated {primary_claude_path} with knowledge management information")
        
    except Exception as e:
        print(f"Error updating primary CLAUDE.md: {e}")


def create_project_claude_md(project_root: str, project_type: str) -> None:
    """
    Create project-specific PROJECT_CLAUDE.md file.
    Also updates the primary CLAUDE.md with knowledge management info.
    
    Args:
        project_root: Path to project root
        project_type: Type of project
    """
    # First, update the primary CLAUDE.md if needed
    update_primary_claude_md()
    
    templates = {
        "python-uv": """# Project-Specific Claude Configuration

## Project Type
Python project using pyproject.toml and uv

## Development Workflow
- Package manager: uv
- Test framework: pytest
- Code formatter: ruff
- Type checking: mypy (optional)

## Key Commands
```bash
uv run python <script>     # Run Python scripts
uv add <package>           # Add dependencies
uv sync                    # Sync dependencies
uv run pytest              # Run tests
uv run ruff check .        # Lint code
uv run ruff format .       # Format code
```

## Project Knowledge Location
- Plans: .claude/doc/plans/
- Research: .claude/doc/research/
- Session Context: .claude/sessions/active/
- Patterns: .claude/knowledge/patterns/

## Testing Strategy
- Write tests first (TDD)
- Use pytest fixtures for setup
- Aim for 80%+ coverage
- Test files in tests/ directory

## Code Quality Standards
- Follow PEP 8 style guide
- Use type hints where beneficial
- Write docstrings for public functions
- Keep functions focused and small

## FastAPI Specific (if applicable)
- Use Pydantic for data validation
- Implement proper error handling
- Write integration tests for endpoints
- Use dependency injection
""",
        "javascript-frontend": """# Project-Specific Claude Configuration

## Project Type
JavaScript frontend project (likely FastAPI frontend)

## Development Workflow
- Package manager: pnpm (preferred) or npm
- Test framework: Jest or Vitest
- Build tool: Vite
- Linter: ESLint
- Formatter: Prettier

## Key Commands
```bash
pnpm install              # Install dependencies
pnpm dev                  # Start dev server
pnpm test                 # Run tests
pnpm build                # Build for production
pnpm lint                 # Lint code
pnpm format               # Format code
```

## Project Knowledge Location
- Plans: .claude/doc/plans/
- Research: .claude/doc/research/
- Session Context: .claude/sessions/active/
- Patterns: .claude/knowledge/patterns/

## Component Structure
- Components in src/components/
- Use functional components with hooks
- Separate logic from presentation
- Write tests alongside components

## FastAPI Integration
- API client in src/api/
- Environment variables for API URL
- Error handling for API calls
- Type definitions for API responses
"""
    }
    
    content = templates.get(project_type, templates["python-uv"])
    
    # Add timestamp and auto-generated note
    content = f"""<!-- Auto-generated by Claude Code on {datetime.now().isoformat()} -->
<!-- Project Type: {project_type} -->

{content}

## Notes
- This file is project-specific and should be committed to version control
- Update this file as project conventions evolve
- Global settings are in ~/.claude/CLAUDE.md
"""
    
    project_claude_path = Path(project_root) / ".claude" / "PROJECT_CLAUDE.md"
    project_claude_path.write_text(content)


def create_project_templates(project_root: str, project_type: str) -> None:
    """
    Create project-specific templates.
    
    Args:
        project_root: Path to project root
        project_type: Type of project
    """
    template_dir = Path(project_root) / ".claude" / "templates"
    
    # Plan template
    plan_template = """# Implementation Plan: [Feature Name]
**Created**: [Timestamp]
**Agent**: [Agent Name]
**Session**: [Session ID]

## Executive Summary
[2-3 sentence overview]

## Architecture Overview
[High-level design description]

## Implementation Phases
### Phase 1: [Name]
- **Objective**: [Goal]
- **Tasks**:
  - [ ] [Task 1]
  - [ ] [Task 2]
- **Validation**: [Success criteria]

### Phase 2: [Name]
- **Objective**: [Goal]
- **Tasks**:
  - [ ] [Task 1]
  - [ ] [Task 2]
- **Validation**: [Success criteria]

## Risk Analysis
| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| [Risk] | High/Medium/Low | High/Medium/Low | [Strategy] |

## Success Criteria
- [ ] All tests passing
- [ ] Documentation updated
- [ ] Code reviewed
- [ ] Performance acceptable

## Next Steps
1. [Immediate next action]
2. [Following action]
"""
    
    (template_dir / "plan-template.md").write_text(plan_template)
    
    # Test template for Python
    if "python" in project_type:
        test_template = '''"""Test module for [feature]."""

import pytest
from unittest.mock import Mock, patch


class Test[FeatureName]:
    """Test cases for [feature]."""
    
    def test_happy_path(self):
        """Test normal operation."""
        # Arrange
        
        # Act
        
        # Assert
        assert True
    
    def test_edge_case(self):
        """Test edge cases."""
        pass
    
    def test_error_handling(self):
        """Test error conditions."""
        pass
'''
        (template_dir / "test-template.py").write_text(test_template)
    
    # Test template for JavaScript
    elif "javascript" in project_type:
        test_template = """describe('[Feature]', () => {
  beforeEach(() => {
    // Setup
  });

  it('should handle happy path', () => {
    // Arrange
    
    // Act
    
    // Assert
    expect(true).toBe(true);
  });

  it('should handle edge cases', () => {
    // Test edge cases
  });

  it('should handle errors gracefully', () => {
    // Test error conditions
  });
});
"""
        (template_dir / "test-template.js").write_text(test_template)


def create_initial_session(project_root: str, project_type: str) -> Path:
    """
    Create the first session context file.
    
    Args:
        project_root: Path to project root
        project_type: Type of project
        
    Returns:
        Path to created session file
    """
    session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_path = Path(project_root) / ".claude" / "sessions" / "active" / f"session_{session_id}.md"
    
    content = f"""# Session Context: {session_id}
**Created**: {datetime.now().isoformat()}
**Project Type**: {project_type}
**Project Root**: {project_root}

## Session Objective
[To be defined by first task]

## Current State
- **Active Task**: Initialization
- **Progress**: 0%
- **Blockers**: None

## Key Decisions
- Project knowledge structure initialized
- Templates created for {project_type}

## File References
- Plans: []
- Research: []
- Implementation: []

## Agent Activity Log
| Timestamp | Agent | Action | Output File |
|-----------|-------|--------|-------------|
| {datetime.now().strftime('%H:%M:%S')} | System | Session initialized | - |

## Notes
- Project knowledge structure initialized
- Ready for agent workflows
"""
    
    session_path.write_text(content)
    return session_path


def update_gitignore(project_root: str) -> None:
    """
    Update .gitignore to handle .claude/ directories appropriately.
    
    Args:
        project_root: Path to project root
    """
    gitignore_path = Path(project_root) / ".gitignore"
    
    # Patterns to add
    claude_patterns = [
        "\n# Claude Code knowledge management",
        ".claude/sessions/",  # Always private
        ".claude/doc/*.tmp",  # Temporary files
        ".claude/**/*.log",   # Log files
    ]
    
    # Check if .gitignore exists
    if gitignore_path.exists():
        content = gitignore_path.read_text()
        
        # Check if we've already added our patterns
        if ".claude/sessions/" not in content:
            # Append our patterns
            with open(gitignore_path, 'a') as f:
                f.write('\n')
                for pattern in claude_patterns:
                    f.write(f"{pattern}\n")
    else:
        # Create new .gitignore
        with open(gitignore_path, 'w') as f:
            for pattern in claude_patterns:
                f.write(f"{pattern}\n")


def get_session_context(project_root: str) -> Optional[str]:
    """
    Get the latest active session context.
    
    Args:
        project_root: Path to project root
        
    Returns:
        Content of latest session or None
    """
    active_sessions = Path(project_root) / ".claude" / "sessions" / "active"
    
    if not active_sessions.exists():
        return None
    
    sessions = list(active_sessions.glob("session_*.md"))
    if not sessions:
        return None
    
    # Get most recent session
    latest_session = max(sessions, key=lambda p: p.stat().st_mtime)
    
    try:
        return latest_session.read_text()
    except Exception:
        return None


def archive_old_sessions(project_root: str, days_old: int = 7) -> None:
    """
    Archive sessions older than specified days.
    
    Args:
        project_root: Path to project root
        days_old: Number of days before archiving
    """
    from datetime import timedelta
    
    active_dir = Path(project_root) / ".claude" / "sessions" / "active"
    archive_dir = Path(project_root) / ".claude" / "sessions" / "archive"
    
    if not active_dir.exists():
        return
    
    cutoff_time = datetime.now() - timedelta(days=days_old)
    
    for session_file in active_dir.glob("session_*.md"):
        # Check file modification time
        mtime = datetime.fromtimestamp(session_file.stat().st_mtime)
        if mtime < cutoff_time:
            # Move to archive
            archive_dir.mkdir(parents=True, exist_ok=True)
            session_file.rename(archive_dir / session_file.name)


if __name__ == "__main__":
    # Test the functions
    root = get_project_root()
    project_type = get_project_type(root)
    initialized = is_project_initialized(root)
    
    print(f"Project root: {root}")
    print(f"Project type: {project_type}")
    print(f"Initialized: {initialized}")