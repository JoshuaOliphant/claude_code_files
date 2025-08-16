# Project Initialization System - Implementation Plan

## Overview
Implement a project-specific knowledge management system that automatically detects and initializes `.claude/` structure for Python and JavaScript projects, using the existing `session_start.py` hook and a new `/project-init` command.

## Key Design Decisions

### 1. Project Detection Strategy
- Claude Code already creates `.claude/` automatically
- We need to check for our specific knowledge structure, not just directory existence
- Use `PROJECT_CLAUDE.md` as initialization marker
- Focus on Python (primary) and JavaScript (for FastAPI frontends)

### 2. Project Type Detection
```python
Priority order:
1. Python-modern (pyproject.toml)
2. Python-legacy (requirements.txt or setup.py)
3. JavaScript-frontend (package.json with React/Vue/Svelte)
4. JavaScript-fastapi (package.json with FastAPI references)
5. Python-generic (*.py files exist)
```

### 3. Directory Structure
```
<project-root>/
├── .claude/                      # Created by Claude Code
│   ├── PROJECT_CLAUDE.md        # Our initialization marker
│   ├── doc/
│   │   ├── plans/
│   │   ├── research/
│   │   └── implementation/
│   ├── sessions/
│   │   ├── active/
│   │   └── archive/
│   ├── knowledge/
│   │   ├── patterns/
│   │   ├── decisions/
│   │   └── testing/
│   └── templates/
```

## Implementation Tasks

### Phase 1: Core Functions
- [x] Create helper functions module (`hooks/utils/project_init.py`)
  - [x] `get_project_root()` - Detect project root directory
  - [x] `get_project_type()` - Identify Python/JavaScript project type (simplified for python-uv)
  - [x] `is_project_initialized()` - Check for knowledge structure
  - [x] `initialize_project_structure()` - Create directories
  - [x] `create_project_claude_md()` - Generate project-specific config
  - [x] `create_initial_session()` - Initialize first session context
  - [x] `update_gitignore()` - Add appropriate .claude/ entries
  - [x] Created specialized project-init agent instead of templates

### Phase 2: Hook Enhancement
- [x] Update `session_start.py` hook
  - [x] Import project initialization utilities
  - [x] Add initialization check after line 162
  - [x] Add context notifications for uninitialized projects
  - [x] Load active session context if exists
  - [x] Test with Python project
  - [ ] Test with JavaScript project

### Phase 3: Slash Command
- [x] Create `/commands/project-init.md`
  - [x] Project type detection logic
  - [x] Initialization workflow
  - [x] Template selection based on type
  - [x] Success confirmation messaging
  - [x] Error handling for existing structures

### Phase 4: Agent Updates
- [ ] Update high-priority agents with context awareness
  - [ ] `investigator.md` - Add project context loading
  - [ ] `planner.md` - Add knowledge retrieval
  - [ ] `coder.md` - Add session tracking
  - [ ] `test-writer.md` - Add test pattern storage
  - [ ] `committer.md` - Add decision logging

### Phase 5: Testing & Validation
- [ ] Test scenarios
  - [ ] Fresh Python project with pyproject.toml
  - [ ] Legacy Python project with requirements.txt
  - [ ] JavaScript React project
  - [ ] FastAPI with frontend
  - [ ] Project with existing .claude/ directory
  - [ ] Non-git project
  - [ ] Monorepo structure

- [ ] Validation criteria
  - [ ] Hook detects uninitialized projects correctly
  - [ ] /project-init creates all required directories
  - [ ] Templates are appropriate for project type
  - [ ] .gitignore updated correctly
  - [ ] Sessions persist across Claude Code restarts
  - [ ] Knowledge accumulates properly

## Code Snippets

### Core Detection Functions
```python
def is_project_initialized(project_root):
    """Check if the knowledge structure is initialized."""
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

def get_project_type(project_root):
    """Detect if this is Python or JavaScript project."""
    project_path = Path(project_root)
    
    # Python indicators (ordered by specificity)
    if (project_path / "pyproject.toml").exists():
        return "python-modern"
    elif (project_path / "requirements.txt").exists():
        return "python-legacy"
    elif (project_path / "package.json").exists():
        # Check package.json content for framework
        try:
            with open(project_path / "package.json") as f:
                content = json.load(f)
                deps = content.get("dependencies", {})
                if "react" in deps or "vue" in deps:
                    return "javascript-frontend"
        except:
            pass
        return "javascript"
    elif list(project_path.glob("*.py")):
        return "python-generic"
    
    return "unknown"
```

### Hook Integration Point
```python
# In session_start.py, after line 162
project_root = get_project_root()
project_type = get_project_type(project_root)

if not is_project_initialized(project_root):
    context_parts.append(f"\n📍 Project detected: {project_type}")
    context_parts.append("📂 Project knowledge structure not initialized")
    context_parts.append("💡 Run /project-init to enable:")
    context_parts.append("  - Persistent session contexts")
    context_parts.append("  - Knowledge accumulation")
    context_parts.append("  - Agent output management")
else:
    # Load latest active session
    active_sessions = Path(project_root) / ".claude" / "sessions" / "active"
    if active_sessions.exists():
        sessions = list(active_sessions.glob("session_*.md"))
        if sessions:
            latest_session = max(sessions, key=lambda p: p.stat().st_mtime)
            context_parts.append(f"\n📂 Active session: {latest_session.name}")
```

## Success Metrics

1. **Automatic Detection**: Hook identifies project type correctly 100% of time
2. **Clean Initialization**: /project-init creates structure without errors
3. **Session Persistence**: Context maintained across Claude Code restarts
4. **Knowledge Growth**: Patterns and decisions accumulate over time
5. **No Conflicts**: Works alongside Claude Code's default .claude/ usage

## Timeline Estimate

- Phase 1 (Core Functions): 1 hour
- Phase 2 (Hook Enhancement): 30 minutes  
- Phase 3 (Slash Command): 30 minutes
- Phase 4 (Agent Updates): 2 hours
- Phase 5 (Testing): 1 hour

**Total: ~4-5 hours of implementation**

## Next Steps

1. Start with Phase 1 - Create helper functions
2. Test functions in isolation
3. Integrate into session_start.py
4. Create /project-init command
5. Test end-to-end workflow
6. Update agents incrementally

## Notes

- Keep Python as primary focus (since that's main use case)
- JavaScript support mainly for FastAPI frontends
- PROJECT_CLAUDE.md serves as both config and initialization marker
- Session contexts should be in .gitignore (private)
- Knowledge patterns should be committed (valuable team asset)

---
**Created**: 2024-11-16
**Status**: Ready to implement
**Priority**: High
**Location**: `/Users/joshuaoliphant/.claude/doc/project-init-implementation-plan.md`