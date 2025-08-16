---
description: Create a TDD implementation plan from a specification, breaking it into GitHub issue-sized tasks
argument-hint: <spec file path>
---

# Plan TDD Implementation

Think systematically about the specification and create a comprehensive Test-Driven Development plan that decomposes the project into testable, incremental tasks for: $ARGUMENTS

## Pre-Planning Analysis

Before creating the plan, I will analyze:
1. **Specification Completeness**: Are all requirements clear and testable?
2. **Technical Complexity**: What architectural patterns are needed?
3. **Risk Assessment**: What could block or complicate implementation?
4. **Testing Strategy**: How can we ensure comprehensive test coverage?
5. **Decomposition Approach**: How to break this into right-sized chunks?

## Planning Execution Phases

### Phase 1: Specification Deep Dive
**Objective**: Extract and validate all requirements

Use the `investigator` sub-agent to:
- Read specification file thoroughly
- Extract functional and non-functional requirements
- Identify ambiguities or gaps
- Research unfamiliar technologies
- Map dependencies and constraints

**Analysis Questions**:
- What are the core features that must work?
- What are the edge cases and error conditions?
- What external systems does this integrate with?
- What performance requirements exist?
- What security considerations apply?

**Specification Checkpoint**:
- [ ] All requirements documented
- [ ] Ambiguities clarified or noted
- [ ] Technologies researched
- [ ] Constraints identified
- [ ] Success criteria defined

### Phase 2: Architecture Design
**Objective**: Create robust, testable architecture

Use the `planner` sub-agent to:
- Design system architecture with clear boundaries
- Identify components and their responsibilities
- Define interfaces and contracts
- Plan data flow and state management
- Consider scalability and maintainability

**Architecture Principles**:
- Separation of concerns
- Dependency injection for testability
- Interface-based design
- Single responsibility principle
- Minimal coupling, high cohesion

**Architecture Checkpoint**:
- [ ] Components clearly defined
- [ ] Interfaces documented
- [ ] Data flow mapped
- [ ] Dependencies minimized
- [ ] Testability ensured

### Phase 3: Task Decomposition
**Objective**: Break down into optimal work units

Transform architecture into GitHub issues:

**Decomposition Strategy**:
1. **Foundation First**: Start with core infrastructure
2. **Vertical Slices**: Each task delivers working functionality
3. **Incremental Value**: Each task adds measurable progress
4. **Test Coverage**: Every task includes its tests
5. **No Orphans**: All code connects to the system

**Task Sizing Criteria**:
- **Too Small**: If it takes longer to describe than implement
- **Too Large**: If it has multiple unrelated changes
- **Just Right**: Single responsibility, clear testing boundary

**Task Structure Template**:
```markdown
## Task N: [Descriptive Title]

**Dependencies**: [Previous tasks required]
**Complexity**: [1-5 scale]
**Test Units**: [Number of behaviors to test]

**Acceptance Criteria**:
- [ ] Specific, measurable outcome
- [ ] Test coverage requirement
- [ ] Integration point verified
- [ ] Documentation updated

**TDD Approach**:
1. Write failing test for [behavior]
2. Implement minimal solution
3. Refactor if needed
4. Integrate with existing code
```

**Decomposition Checkpoint**:
- [ ] Tasks properly sized
- [ ] Dependencies mapped
- [ ] No circular dependencies
- [ ] Progressive complexity
- [ ] Complete coverage

### Phase 4: TDD Prompt Generation
**Objective**: Create self-contained implementation instructions

For each task, generate AI-ready prompts:

**Prompt Components**:
1. **Context Setting**: What exists from previous tasks
2. **Clear Objective**: What this task accomplishes
3. **Test Requirements**: Specific tests to write FIRST
4. **Implementation Hints**: Approach without spoiling solution
5. **Integration Steps**: How to connect with existing code
6. **Validation Criteria**: How to verify completion

**Prompt Quality Rules**:
- Self-contained with all context
- Explicit about test-first approach
- Clear acceptance criteria
- Integration instructions included
- No assumed knowledge

**Example Prompt Structure**:
````markdown
```text
Think carefully about implementing [feature] using strict TDD principles.

**Previous Context**:
[What was built before]

**Your Task**:
[Clear objective]

**Tests to Write FIRST** (must fail initially):
1. Test that [specific behavior]
2. Test edge case when [condition]
3. Test error handling for [scenario]

**Implementation Approach**:
- Use [pattern/library]
- Follow [principle]
- Consider [constraint]

**Integration Requirements**:
1. Connect to [existing component]
2. Update [configuration]
3. Wire into [system]

**Success Validation**:
- All tests pass
- No regression in existing tests
- Code follows project patterns
- Integration verified

Begin by writing the failing tests.
```
````

**Prompt Generation Checkpoint**:
- [ ] Each prompt self-contained
- [ ] TDD explicitly required
- [ ] Context clearly provided
- [ ] Integration specified
- [ ] Validation criteria included

### Phase 5: Deliverable Creation
**Objective**: Produce comprehensive planning artifacts

Generate required files:

#### 5.1: plan.md Contents
```markdown
# Implementation Plan

## Architecture Overview
[System design and component diagram]

## Technology Stack
[Languages, frameworks, libraries]

## Task Breakdown
[All tasks with metadata]

## AI Implementation Prompts
[All prompts in executable format]

## Dependency Graph
[Visual or textual representation]

## Testing Strategy
[Overall approach to system testing]

## Risk Mitigation
[Identified risks and mitigation plans]
```

#### 5.2: todo.md Contents
```markdown
# Task Tracking

## Phase 1: Foundation
- [ ] Task 1: [Title] (Complexity: N, Tests: N)
- [ ] Task 2: [Title] (depends on Task 1)

## Phase 2: Core Features
- [ ] Task 3: [Title] (depends on Tasks 1-2)

## Phase 3: Integration
- [ ] Task N: [Title] (final integration)

## Validation Checklist
- [ ] All tests passing
- [ ] Documentation complete
- [ ] Performance acceptable
- [ ] Security verified
```

**Deliverable Checkpoint**:
- [ ] plan.md comprehensive
- [ ] todo.md actionable
- [ ] Prompts extractable
- [ ] Dependencies clear
- [ ] Ready for execution

## Quality Validation

### Planning Quality Metrics
Evaluate the plan against:
1. **Completeness**: All requirements addressed?
2. **Testability**: Every feature has clear tests?
3. **Incrementality**: Smooth progression?
4. **Independence**: Tasks can be done in parallel where possible?
5. **Clarity**: Prompts are unambiguous?

### Success Criteria
The plan is complete when:
- Every requirement maps to tasks
- Every task has a TDD prompt
- Dependencies form a valid DAG
- No implementation gaps exist
- Testing strategy is comprehensive

## Effort Estimation Framework

### Complexity Scoring (1-5)
1. **Trivial**: Configuration or simple logic
2. **Simple**: Straightforward implementation
3. **Moderate**: Multiple components involved
4. **Complex**: Architectural decisions required
5. **Very Complex**: Research and experimentation needed

### Test Coverage Units (TCU)
Count distinct behaviors:
- Each assertion = 1 TCU
- Each edge case = 1 TCU
- Each error path = 1 TCU
- Integration test = 2-3 TCU

### AI Interaction Rounds
Estimate iterations:
- Simple task: 1-2 rounds
- Moderate task: 3-4 rounds
- Complex task: 5+ rounds

## Anti-Patterns to Avoid

**Planning Mistakes**:
- Tasks too large (>5 complexity)
- Missing test specifications
- Unclear dependencies
- Vague acceptance criteria
- No integration instructions

**TDD Violations**:
- Writing code before tests
- Skipping test failure verification
- Not refactoring after green
- Incomplete test coverage
- Testing implementation not behavior

Begin with Phase 1: Specification Deep Dive using the investigator sub-agent.