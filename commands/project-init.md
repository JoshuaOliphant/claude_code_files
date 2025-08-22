---
description: Initialize project-specific knowledge structure for persistent context management
---

# Project Knowledge Initialization

I will set up a comprehensive knowledge management system for this project to enable persistent context, pattern recognition, and intelligent session management.

## Pre-Initialization Analysis

First, I'll analyze your project to determine:
1. **Project Type**: Python (with uv), JavaScript (for FastAPI frontends), or other
2. **Current Structure**: Existing .claude directory and configuration
3. **Git Integration**: Repository status and branching strategy
4. **Development Patterns**: Testing framework, linting tools, build process

## Initialization Process

### Phase 1: Project Detection
```python
# Detect project type based on indicators
- Python-uv: pyproject.toml with uv configuration
- JavaScript-frontend: package.json with React/Vue/Svelte
- Python-generic: *.py files without package management
```

### Phase 2: Directory Structure Creation

I will create the following knowledge structure:

```
<project-root>/
├── CLAUDE.md                     # Project-specific configuration
├── .claude/                      # Claude Code settings only
│   └── settings.local.json      # Permissions configuration
└── knowledge/                    # Main knowledge directory
    ├── doc/                     # Documentation and plans
    │   ├── plans/               # Implementation plans
    │   ├── research/            # Research and exploration
    │   └── implementation/      # Implementation notes
    ├── sessions/                # Session management
    │   ├── active/              # Current session contexts
    │   └── archive/             # Historical sessions
    ├── patterns/                # Code patterns and solutions
    ├── decisions/               # Technical decisions
    ├── testing/                 # Test strategies
    └── context/                 # Context files
        ├── TODO.md              # Active tasks
        └── CONTEXT.md           # Project context
```

### Phase 3: Configuration Files

**CLAUDE.md** will contain:
- Project type and technology stack
- Key commands and workflows
- Testing and quality requirements
- Development patterns
- Integration points

**Context Files** will track:
- Active tasks and priorities
- Current implementation context
- Known issues and solutions
- Performance considerations

### Phase 4: Git Integration

Update `.gitignore` appropriately:
```gitignore
# Claude Code knowledge management
knowledge/sessions/
knowledge/private/
knowledge/*.log
```

Note: Patterns and decisions are valuable team assets and should be committed.

## Benefits of Initialization

Once initialized, you'll have:

1. **Persistent Context**: Sessions survive Claude Code restarts
2. **Knowledge Accumulation**: Patterns and solutions build over time
3. **Smart Session Management**: Automatic context loading and archiving
4. **Agent Integration**: All agents can access shared knowledge
5. **Project Intelligence**: Claude Code understands your project deeply

## Execution Steps

1. Detect project type and structure
2. Create directory hierarchy
3. Generate CLAUDE.md with project-specific configuration
4. Initialize first session context
5. Update .gitignore for privacy
6. Create initial TODO.md and CONTEXT.md
7. Set up knowledge categories
8. Configure agent overrides if needed

## Post-Initialization

After initialization:
- Session start hook will automatically load context
- Agents will store insights in knowledge directories
- Patterns will accumulate for reuse
- Context will persist across sessions

## Error Handling

If already initialized:
- Preserve existing knowledge
- Update configuration only
- Merge new structure carefully
- Backup existing data first

Ready to initialize your project's knowledge structure. This will enable intelligent context management and knowledge accumulation.