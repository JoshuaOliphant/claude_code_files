---
description: Execute the Explore-Plan-Code-Commit workflow for implementing features
argument-hint: <feature description or task>
---

# Explore-Plan-Code-Commit Workflow

Think systematically about this implementation task and execute the structured EPCC workflow to deliver: $ARGUMENTS

## Pre-Workflow Analysis

Before beginning the EPCC phases, I will analyze:
1. **Task Scope**: What exactly needs to be built and why
2. **Complexity Assessment**: Is this simple, medium, or complex?
3. **Risk Identification**: What could go wrong or block progress?
4. **Success Criteria**: How will we know when we're done?
5. **Agent Allocation**: Which sub-agents are best suited for each phase?

## Workflow Execution Phases

### Phase 1: EXPLORE - Deep Investigation
**Objective**: Gather complete context and understanding

Use the `investigator` sub-agent to:
- Thoroughly understand the existing codebase architecture
- Research best practices and industry patterns
- Identify integration points and dependencies
- Document assumptions and constraints
- Find similar implementations for reference

**Exploration Checkpoint**:
- [ ] Codebase structure understood
- [ ] Existing patterns identified
- [ ] Dependencies mapped
- [ ] Best practices researched
- [ ] Constraints documented

### Phase 2: PLAN - Strategic Design
**Objective**: Create detailed implementation blueprint

Use the `planner` sub-agent to:
- Design comprehensive implementation strategy
- Evaluate multiple architectural approaches
- Decompose into testable, atomic steps
- Identify risks and mitigation strategies
- Create dependency graph between tasks

**Planning Checkpoint**:
- [ ] Multiple approaches evaluated
- [ ] Optimal approach selected
- [ ] Tasks broken down appropriately
- [ ] Dependencies clearly mapped
- [ ] Risks identified with mitigations

### Phase 3: CODE - Test-Driven Implementation
**Objective**: Build feature with quality and confidence

#### Phase 3.1: Write Tests First (RED)
Use the `test-writer` sub-agent to:
- Design comprehensive test suite architecture
- Write failing tests for ALL requirements
- Include edge cases and error conditions
- Verify tests fail for the right reasons
- Document what each test validates

**Test Creation Checkpoint**:
- [ ] All behaviors have tests
- [ ] Tests are failing as expected
- [ ] Edge cases covered
- [ ] Error conditions tested
- [ ] Test documentation complete

#### Phase 3.2: Minimal Implementation (GREEN)
Use the `coder` sub-agent to:
- Implement ONLY code needed to pass tests
- Focus on one failing test at a time
- Avoid premature optimization
- Follow existing code patterns
- Maintain consistent style

**Implementation Rules**:
- No code without failing test
- Simplest solution that works
- One logical change at a time
- Preserve existing functionality

#### Phase 3.3: Test-Fix Iteration Loop
**CRITICAL**: Continue until ALL tests pass

**Iteration Process** (max 10 rounds):
1. **Execute Tests**:
   ```bash
   # Run appropriate test command
   pytest / npm test / cargo test / go test
   ```

2. **Analyze Results**:
   - Record passing tests count
   - Document failing tests
   - Capture error messages
   - Note test coverage

3. **Decision Point**:
   - All tests pass → Proceed to 3.4
   - Tests failing → Fix specific failures
   - New edge cases → Write new tests first
   - Iteration limit → Document blockers

4. **Fix Implementation**:
   - Target specific test failures
   - Make minimal changes
   - Verify fix doesn't break other tests
   - Run full suite after each fix

**Iteration Checkpoint**:
- [ ] Test results captured
- [ ] Failures analyzed
- [ ] Fixes implemented
- [ ] Progress documented
- [ ] Iteration count tracked

#### Phase 3.4: Refactor (REFACTOR)
Once all tests pass:
- Eliminate code duplication
- Improve naming and clarity
- Simplify complex logic
- Extract reusable components
- Run tests after EVERY change

**Refactoring Checkpoint**:
- [ ] Code is DRY
- [ ] Names are descriptive
- [ ] Logic is simplified
- [ ] Tests still passing
- [ ] Performance acceptable

### Phase 3.5: Quality Assurance
**Objective**: Ensure code meets standards

Use the `linter` sub-agent to:
- Run automated formatting (Ruff/ESLint/etc.)
- Fix style violations automatically
- Report issues needing manual fix
- Verify type checking passes
- Ensure documentation updated

**Quality Checkpoint**:
- [ ] Linting passes
- [ ] Formatting correct
- [ ] Types validated
- [ ] Documentation current
- [ ] Standards met

### Phase 4: COMMIT - Version Control
**Objective**: Create clean git history

Use the `committer` sub-agent to:
- Review all changes comprehensively
- Stage appropriate files
- Create atomic, meaningful commits
- Write descriptive commit messages
- Update relevant documentation

**Commit Checkpoint**:
- [ ] Changes reviewed
- [ ] Files staged correctly
- [ ] Commit message clear
- [ ] Tests passing
- [ ] Documentation updated

### Phase 5: Pull Request (if applicable)
**Objective**: Prepare for code review

Use the `pr-drafter` sub-agent to:
- Analyze changes vs base branch
- Create comprehensive PR description
- Include test results and coverage
- Reference related issues
- Add review checklist

**PR Checkpoint**:
- [ ] All changes included
- [ ] Description comprehensive
- [ ] Tests documented
- [ ] Issues linked
- [ ] Ready for review

## Validation & Completion

### Final Verification Checklist
- [ ] Original requirements fully met
- [ ] All tests passing
- [ ] Code quality standards met
- [ ] Documentation complete
- [ ] No regression introduced
- [ ] Performance acceptable
- [ ] Security considerations addressed

### Success Metrics
Track and report:
- Tests written: [count]
- Test coverage: [percentage]
- Iterations needed: [count]
- Refactoring rounds: [count]
- Total execution time: [duration]

## Workflow Rules

**NEVER violate these principles**:
1. No skipping exploration phase
2. Plan before coding
3. Tests before implementation
4. Fix all failing tests
5. Quality before speed

## Adaptive Execution

If blockers encountered:
1. **Document the blocker clearly**
2. **Attempt alternative approach**
3. **Escalate if truly blocked**
4. **Create issues for follow-up**
5. **Deliver partial if valuable**

Begin with Phase 1: EXPLORE using the investigator sub-agent.