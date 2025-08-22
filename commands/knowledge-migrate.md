---
description: Migrate existing project from old knowledge structure to new two-tier knowledge management system
---

# Migrate to Two-Tier Knowledge Management System

I will upgrade this project from the old knowledge management structure to the new two-tier system with specialized agents and consolidation workflow.

## Migration Analysis

First, I'll check the current knowledge structure to understand what needs to be migrated:
1. Detect if using old structure (knowledge directories under `.claude/`)
2. Identify existing knowledge content to preserve
3. Check for any custom patterns or modifications

## Migration Process

### Phase 1: Backup Existing Knowledge
```bash
# Create backup of existing knowledge
cp -r .claude/ .claude.backup.$(date +%Y%m%d_%H%M%S)/
```

### Phase 2: Create New Structure

I will create the new two-tier knowledge directories:

```
<project-root>/
├── CLAUDE.md                    # Project-specific configuration
├── knowledge/                   # Main knowledge directory (NEW LOCATION)
│   ├── capture/                # Tier 1: Raw, immediate insights
│   │   ├── daily/             # Daily capture logs
│   │   ├── insights.md        # Current session insights
│   │   └── observations.md    # Immediate observations
│   ├── refined/                # Tier 2: Processed, validated knowledge
│   │   ├── patterns/          # Generalizable patterns
│   │   ├── principles/        # Core principles  
│   │   └── solutions/         # Proven solutions
│   └── archive/                # Historical processed knowledge
└── .claude/                     # Claude Code settings only
    └── settings.local.json      # Permissions configuration
```

### Phase 3: Migrate Existing Content

I will intelligently migrate existing knowledge:

**From Old Structure → New Structure:**
- `.claude/knowledge/patterns/` → `knowledge/refined/patterns/`
- `.claude/knowledge/decisions/` → `knowledge/refined/principles/`
- `.claude/knowledge/testing/` → `knowledge/refined/solutions/testing/`
- `.claude/doc/research/` → `knowledge/capture/research/`
- `.claude/doc/plans/` → `knowledge/capture/plans/`
- `.claude/doc/implementation/` → `knowledge/capture/implementation/`

**Preserve/Move:**
- `CLAUDE.md` in project root (will be updated)
- `.claude/sessions/` → keep for legacy, create new `knowledge/sessions/`
- `.claude/context/` → move to `knowledge/context/`

### Phase 4: Update CLAUDE.md

I will update the project's CLAUDE.md file with the new knowledge management protocol:

```markdown
## Knowledge Management Protocol

This project uses a two-tier knowledge management system with specialized agents.

### Two-Tier Architecture

**Tier 1: Raw Capture** (`knowledge/capture/`)
- Immediate insights and observations during tasks
- Daily logs and session notes
- Unprocessed patterns and learnings

**Tier 2: Refined Knowledge** (`knowledge/refined/`)
- Validated, generalizable patterns
- Core principles and best practices
- Proven solutions and implementations

### Knowledge Workflow

1. **During Tasks**: Knowledge is automatically captured by agents
2. **After Tasks**: Use `/knowledge-capture` to explicitly capture insights
3. **Periodically**: Use `/knowledge-consolidate` to refine raw knowledge

### Specialized Knowledge Agents

- **knowledge-capturer**: Captures raw insights during or after tasks
- **knowledge-refiner**: Consolidates and refines raw knowledge into patterns

### Quality Gates for Refinement

Knowledge moves from capture to refined only if it is:
- ✓ Generalizable beyond single instance
- ✓ Actionable with clear application
- ✓ Validated through successful use
- ✓ Non-redundant with existing knowledge

### Using Knowledge in Development

Agents automatically consult refined knowledge for:
- **Planner**: Architectural patterns and decisions
- **Coder**: Implementation patterns and solutions
- **Test-writer**: Testing strategies and patterns
- **Investigator**: Research findings and explorations
```

### Phase 5: Update .gitignore

Ensure `.gitignore` properly handles new structure:

```gitignore
# Claude Code knowledge management
knowledge/capture/daily/
knowledge/archive/*.log
.claude/sessions/
.claude/private/
.claude.backup.*/
```

### Phase 6: Create Initial Knowledge Files

Initialize key knowledge files if they don't exist:

**knowledge/capture/insights.md**
```markdown
# Current Insights
<!-- Raw insights from current work -->
```

**knowledge/refined/patterns/README.md**
```markdown
# Validated Patterns
<!-- Proven, reusable patterns -->
```

**knowledge/refined/principles/README.md**
```markdown
# Core Principles
<!-- Fundamental project principles -->
```

### Phase 7: Validation

After migration:
1. Verify all knowledge content is preserved
2. Check that new structure is created correctly
3. Ensure CLAUDE.md is updated
4. Test knowledge agents can access new locations
5. Confirm old backup is intact

## Post-Migration Instructions

After migration is complete:

1. **Immediate**: Review migrated content in new structure
2. **First Session**: Use `/knowledge-capture` after completing tasks
3. **Weekly**: Run `/knowledge-consolidate` to refine captured knowledge
4. **Ongoing**: Agents will use the new structure automatically

## Benefits of New System

- **Better Organization**: Clear separation of raw vs refined knowledge
- **Quality Control**: Only validated knowledge gets refined
- **Easier Maintenance**: Two-tier structure prevents clutter
- **Agent Integration**: Specialized agents for knowledge operations
- **Manual Control**: Explicit consolidation via slash commands

Ready to migrate your project to the new two-tier knowledge management system.