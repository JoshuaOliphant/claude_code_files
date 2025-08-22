---
description: Consolidate raw captured knowledge into refined patterns and principles
---

# Knowledge Consolidation

I will review raw captured knowledge and distill it into refined, actionable patterns, principles, and solutions.

## Process

### Step 1: Assess Raw Knowledge
First, I'll check the status of raw knowledge:
- Count unprocessed entries in `knowledge/capture/`
- Identify common themes and patterns
- Determine if consolidation is warranted

### Step 2: Invoke Knowledge Refiner
I'll use the `knowledge-refiner` agent to:
1. Extract generalizable patterns from multiple instances
2. Distill core principles from discoveries
3. Document proven solutions
4. Archive processed raw entries

### Step 3: Generate Consolidation Report
After refinement, I'll provide:
- New patterns identified
- Principles extracted
- Solutions documented
- Knowledge pruned/archived
- Recommendation for next consolidation

## Consolidation Triggers

Consider running `/knowledge-consolidate` when:
- Raw capture folder has 10+ entries
- End of a project phase or sprint
- Before starting similar work
- Weekly/monthly maintenance
- Significant pattern emerges

## Example Refined Output

The refiner will create structured knowledge like:

### Pattern Example
```markdown
# Pattern: Optimistic Locking Strategy
**Category**: Concurrency
**Confidence**: High

## Description
Use version numbers to detect concurrent modifications

## When to Apply
- Multi-user systems
- Distributed updates
- Low conflict probability

## Implementation
1. Include version in read
2. Check version on update
3. Retry on version mismatch
```

### Principle Example
```markdown
# Principle: Fail Fast, Recover Gracefully
**Domain**: Error Handling
**Type**: Fundamental

## Statement
Detect errors early but provide smooth recovery paths

## Applications
- Validate inputs immediately
- Provide clear error messages
- Implement retry mechanisms
```

## Quality Gates

The refiner will ensure:
- Patterns observed in 2+ instances
- Principles are truly generalizable
- Solutions are actionable
- No redundancy with existing refined knowledge

Begin knowledge consolidation...