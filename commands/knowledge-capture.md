---
description: Capture insights and learnings from the current task
---

# Knowledge Capture

I will systematically capture learnings, patterns, and insights from the current or recently completed task.

## Process

### Step 1: Task Review
First, I'll review what was accomplished:
- What was the main objective?
- What challenges were encountered?
- What solutions were discovered?
- What patterns emerged?

### Step 2: Invoke Knowledge Capturer
I'll use the `knowledge-capturer` agent to:
1. Document discoveries and patterns
2. Record challenges and their resolutions
3. Note successful approaches
4. Extract generalizable principles

### Step 3: Verify Capture
Ensure the knowledge has been properly documented in:
- `knowledge/capture/YYYY-MM-DD.md` for raw insights
- Tagged appropriately for future refinement

## When to Use This Command

Run `/knowledge-capture` when:
- You've completed a complex task
- You've discovered a new pattern or technique
- You've overcome a significant challenge
- You want to ensure learnings aren't lost
- Before context gets compacted

## Example Capture Format

The agent will create entries like:
```markdown
## 14:23 - Task: Implemented JWT refresh logic
**Project/Component**: Authentication System
**Confidence**: High

### Discoveries
- **Pattern**: Token Refresh Strategy
  - Context: When access tokens expire frequently
  - Evidence: 401 responses with token-expired headers
  - Principle: Always refresh before critical operations

### Challenges Resolved
- **Problem**: Race conditions in concurrent refresh
  - Root Cause: Multiple requests triggering refresh
  - Solution: Implement refresh token mutex
  - Prevention: Single refresh orchestrator pattern
```

Begin knowledge capture...