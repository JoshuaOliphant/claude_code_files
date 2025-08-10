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
- Each task should be sized by complexity, not time
- Each task should have clear acceptance criteria
- Tasks should build incrementally (no orphaned code)
- Earlier tasks create foundation for later ones
- Include both implementation and testing in each task

### Phase 4: Create TDD Prompts
For each task, create a complete AI agent prompt that includes:
1. **Context**: What was built in previous tasks
2. **Objective**: What this task accomplishes
3. **Test Requirements**: Specific tests to write first
4. **Implementation Hints**: Approach without giving away the solution
5. **Integration**: How to connect with existing code

Each prompt should be formatted as a standalone instruction that can be given to an AI agent, wrapped in markdown code blocks tagged as `text`. The prompts should:
- Be self-contained with all necessary context
- Build incrementally on previous prompts
- Include specific TDD instructions (write tests first, then implementation)
- End with integration steps to connect to existing code
- Avoid orphaned code that isn't wired into the system

### Phase 5: Generate Deliverables
Create the following files:
- `plan.md`: Complete implementation plan with architecture, task breakdown, and all AI prompts
- `todo.md`: Task tracking with status and dependencies
- Each prompt in `plan.md` should be clearly separated and tagged for easy extraction

## Task Sizing Guidelines

Each task should be:
- **Small enough to**: Complete in one focused session, test thoroughly, review easily
- **Large enough to**: Make meaningful progress, be worth tracking as an issue
- **Self-contained**: Has clear inputs/outputs and can be tested independently
- **Incremental**: Builds on previous work without large complexity jumps

## Effort Estimation Metrics

Instead of time estimates, use these AI-friendly metrics:

### Complexity Points (1-5 scale)
- **1**: Single-file change, clear requirements
- **2**: Multi-file changes, straightforward logic
- **3**: New component with moderate integration
- **4**: Complex architecture, multiple system interactions
- **5**: Research-heavy, experimental approach

### AI Rounds
Estimated interaction cycles needed:
- Count prompt → implementation → refinement cycles
- More complex tasks require more iterations

### Test Coverage Units (TCU)
Count distinct behaviors to verify:
- Each unit represents a specific test scenario
- More predictable than time estimates
- Focuses on completeness rather than duration

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

**Effort Estimates**:
- **Complexity**: 2/5 (straightforward auth logic)
- **AI Rounds**: ~3 (tests → implementation → integration)
- **Test Coverage**: 4 units (token, hash, login, protected routes)

### AI Agent Prompt for Task 3:

```text
You are implementing a user authentication service following Test-Driven Development (TDD) principles.

**Context from Previous Tasks:**
- Task 1: Database models have been created with User table containing id, email, password_hash, created_at, updated_at
- Task 2: Basic Express API setup is complete with routing structure and middleware configuration

**Your Objective:**
Implement JWT-based authentication with secure password handling.

**TDD Requirements - Write These Tests FIRST:**
1. Test that password hashing produces different hashes for the same password (salting)
2. Test that password verification correctly validates matching passwords
3. Test that JWT token generation includes user ID and expiration
4. Test that JWT token validation accepts valid tokens and rejects invalid/expired ones
5. Test that login endpoint returns 401 for invalid credentials
6. Test that login endpoint returns valid JWT for correct credentials
7. Test that protected routes reject requests without tokens
8. Test that protected routes accept requests with valid tokens

**Implementation Approach:**
- Use bcrypt for password hashing (10 salt rounds)
- Use jsonwebtoken library for JWT operations
- Create /auth/login POST endpoint
- Create authentication middleware for protected routes
- Store JWT secret in environment variables
- Set appropriate token expiration (e.g., 24 hours)

**Integration Steps:**
1. Add authentication middleware to the Express app
2. Update User model to include password comparison method
3. Wire login endpoint into existing router structure
4. Apply authentication middleware to routes that need protection
5. Ensure all tests pass before considering the task complete

Remember: Write tests first, then implement only enough code to make them pass.
```
```

## Output Format

The plan should produce in `plan.md`:
1. **Overview section** with high-level architecture and approach
2. **Task breakdown** with issue-ready tasks including:
   - Title, description, and acceptance criteria
   - Dependencies and effort estimates
   - TDD approach for each task
3. **AI Agent Prompts** for each task:
   - Each prompt wrapped in ````text` code blocks
   - Self-contained with all necessary context
   - Clear TDD instructions (tests first, then implementation)
   - Integration steps to connect with previous work
4. **Dependency graph** showing task relationships
5. **Testing strategy** for overall system

Additionally create `todo.md` with:
- Checklist of all tasks with status tracking
- Dependencies clearly marked
- Ready for tracking progress

The prompts should be formatted exactly like this:
```markdown
### Task N: [Task Title]

[Task description and metadata...]

#### AI Agent Prompt:

```text
[Complete, self-contained prompt that can be given directly to an AI agent]
```
```

Begin by analyzing the specification file.
