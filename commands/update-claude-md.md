---
description: Update project CLAUDE.md with knowledge management instructions
---

# Update Project CLAUDE.md with Knowledge Management Instructions

Update the project's CLAUDE.md file to include instructions about using the knowledge management system. This ensures the main Claude Code agent understands how to leverage persistent context and accumulated knowledge.

## Instructions

### Step 1: Check Prerequisites
First, verify the project has been initialized:
1. Check if `.claude/` directory exists in project root
2. If not, inform user to run `/project-init` first
3. If yes, proceed with CLAUDE.md update

### Step 2: Read Existing CLAUDE.md
Use the Read tool to check for CLAUDE.md in project root:
- If it exists, read its current contents
- If not, you'll create a new one
- Note any existing sections to preserve

### Step 3: Add Knowledge Management Section
Add or update a section titled "Knowledge Management" with the following information adapted to this specific project:

#### Essential Content to Include:

**Knowledge Structure Overview**
Explain the knowledge management directory structure in project root:
- `.claude/` - Project configuration only
  - `PROJECT_CLAUDE.md` - Project-specific Claude instructions
- `knowledge/` - Main knowledge directory
  - `doc/` - Documentation and plans
  - `sessions/` - Work continuity tracking
  - `patterns/` - Code patterns and solutions
  - `decisions/` - Technical decisions
  - `testing/` - Test strategies
  - `templates/` - Project-specific templates
  - `context/` - Context files (TODO.md, CONTEXT.md)

**How to Use Knowledge**
Provide specific instructions for:
1. Checking active sessions on startup
2. Loading relevant context before tasks
3. Updating knowledge during work
4. Archiving completed sessions

**Project-Specific Patterns**
Based on the project type, include relevant examples:
- For Python projects: How to document uv package decisions
- For JavaScript projects: How to track npm dependency choices
- For mixed projects: How to organize by language/framework

**Best Practices**
Include guidelines like:
- Always check `knowledge/sessions/active/` when starting work
- Document significant decisions in `knowledge/decisions/`
- Save reusable code patterns in `knowledge/patterns/`
- Reference previous work to maintain consistency

### Step 4: Integrate with Existing Content
When adding the knowledge management section:
1. Place it after the project overview (if one exists)
2. Before any specific coding guidelines
3. Ensure it complements, not duplicates, existing instructions
4. Use the same formatting style as the rest of the file

### Step 5: Add Cross-References
Include references to:
- The PROJECT_CLAUDE.md file in `.claude/`
- How subagents use the knowledge system
- The `/project-init` command for initialization

### Example Template

Here's a template you can adapt based on the project's specific needs:

```markdown
## Knowledge Management

This project uses Claude Code's knowledge management system to maintain context across sessions and accumulate project-specific knowledge.

### Quick Start
- Check `knowledge/sessions/active/` for any ongoing work
- Review `knowledge/patterns/` for established code patterns
- Consult `knowledge/decisions/` for technical decisions

### During Development
1. **Before starting new work**: Check active sessions and recent decisions
2. **When solving problems**: Document solutions in knowledge/patterns/
3. **When making choices**: Record rationale in knowledge/decisions/
4. **After completing tasks**: Archive sessions and update documentation

### Project-Specific Guidelines
[Adapt based on what you find in the project - languages, frameworks, conventions]

### See Also
- `.claude/PROJECT_CLAUDE.md` - Project-specific configuration
- Run `/project-init` if knowledge structure doesn't exist
```

## Important Notes

- Preserve all existing content in CLAUDE.md
- Adapt the template to match the project's tone and style
- Include concrete examples relevant to the project
- Make instructions actionable and specific
- Don't duplicate information already in PROJECT_CLAUDE.md

Begin by reading the current CLAUDE.md file (if it exists) and then update it appropriately.