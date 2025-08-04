---
description: Create a TDD implementation plan from a specification, breaking it into GitHub issue-sized tasks
argument-hint: <spec file path>
---

# Plan TDD Implementation

Create a comprehensive Test-Driven Development plan for the specification in: $ARGUMENTS

## Workflow Overview

### Phase 1: Analyze Specification
Use the `investigator` sub-agent to:
- Read and thoroughly understand the specification file
- Identify all functional requirements, constraints, and edge cases
- Research any unfamiliar concepts or technologies mentioned
- Note dependencies and integration points

### Phase 2: Create High-Level Architecture
Use the `planner` sub-agent to:
- Design the overall system architecture
- Identify major components and their relationships
- Define clear boundaries between modules
- Consider scalability and maintainability

### Phase 3: Break Down into Issues
Transform the plan into GitHub issue-sized tasks:
- Each task should be implementable in 2-4 hours
- Each task should have clear acceptance criteria
- Tasks should build incrementally (no orphaned code)
- Earlier tasks create foundation for later ones
- Include both implementation and testing in each task

### Phase 4: Create TDD Prompts
For each task, create a structured prompt that includes:
1. **Context**: What was built in previous tasks
2. **Objective**: What this task accomplishes
3. **Test Requirements**: Specific tests to write first
4. **Implementation Hints**: Approach without giving away the solution
5. **Integration**: How to connect with existing code

### Phase 5: Generate Deliverables
Create the following files:
- `plan.md`: Complete implementation plan with architecture and task breakdown
- `todo.md`: Task tracking with status and dependencies
- `prompts/`: Directory with individual prompt files for each task

## Task Sizing Guidelines

Each task should be:
- **Small enough to**: Complete in one focused session, test thoroughly, review easily
- **Large enough to**: Make meaningful progress, be worth tracking as an issue
- **Self-contained**: Has clear inputs/outputs and can be tested independently
- **Incremental**: Builds on previous work without large complexity jumps

## Example Task Structure

```markdown
## Task 3: Implement User Authentication Service

**Dependencies**: Tasks 1-2 (Database models, Basic API setup)

**Acceptance Criteria**:
- [ ] JWT token generation and validation
- [ ] Password hashing with bcrypt
- [ ] Login endpoint returns valid token
- [ ] Protected routes require valid token

**TDD Approach**:
1. Write tests for token generation/validation
2. Write tests for password hashing
3. Write integration tests for login flow
4. Implement minimal code to pass tests

**Estimated effort**: 3 hours
```

## Output Format

The plan should produce:
1. **Issue-ready tasks** with titles, descriptions, and acceptance criteria
2. **TDD prompts** that guide implementation without revealing solutions
3. **Dependency graph** showing task relationships
4. **Testing strategy** for each component

Begin by analyzing the specification file.