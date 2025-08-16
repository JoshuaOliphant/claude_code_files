---
description: Execute Test-Driven Development workflow - write tests first, then implement code to make them pass
argument-hint: <feature description>
---

# Test-Driven Development Workflow

Think deeply about the feature requirements and execute a disciplined TDD workflow to implement: $ARGUMENTS

## Pre-Implementation Analysis

Before writing any code, I will:
1. **Understand Requirements**: Analyze what the feature must do and why
2. **Identify Behaviors**: List all behaviors that need testing
3. **Design Test Strategy**: Plan comprehensive test coverage
4. **Consider Edge Cases**: Think through failure modes and boundaries
5. **Verify Approach**: Ensure TDD is the right methodology for this task

## TDD Execution Phases

### Phase 1: Test Planning & Writing (RED)
**Objective**: Define behavior through failing tests

Use the `test-writer` sub-agent to:
- Design test architecture and organization
- Write comprehensive test cases covering:
  - Happy path scenarios
  - Edge cases and boundaries
  - Error conditions and exceptions
  - Integration points
- Verify tests fail for the right reasons
- Document what each test validates

**Validation Checkpoint**:
- [ ] All requirements have corresponding tests
- [ ] Tests are atomic and focused
- [ ] Test names clearly describe behavior
- [ ] Tests fail with meaningful error messages

### Phase 2: Initial Test Commit
**Objective**: Lock in behavioral specification

Use the `committer` sub-agent to:
- Review test completeness and quality
- Run tests to confirm they fail correctly
- Commit with message: "test: add failing tests for [feature]"
- Document expected vs actual behavior

**Validation Checkpoint**:
- [ ] Tests committed in failing state
- [ ] Failure messages are informative
- [ ] No syntax errors in tests
- [ ] Test structure follows project conventions

### Phase 3: Minimal Implementation (GREEN)
**Objective**: Make tests pass with simplest code possible

Use the `coder` sub-agent to implement incrementally:

**Iteration Loop** (repeat for each test):
1. Pick one failing test
2. Write minimal code to make it pass
3. Run test suite to verify:
   - Target test now passes
   - No existing tests broken
4. Continue to next failing test

**Implementation Rules**:
- Write ONLY code required to pass current test
- No premature optimization
- No untested functionality
- Follow existing patterns

**Validation Checkpoint**:
- [ ] Each test passes individually
- [ ] All tests pass together
- [ ] No test is skipped or disabled
- [ ] Implementation is minimal but complete

### Phase 4: Refactoring (REFACTOR)
**Objective**: Improve code quality while maintaining green tests

Use the `coder` sub-agent to:
- Identify code smells and duplication
- Refactor for clarity and maintainability
- Extract methods/functions where appropriate
- Improve naming and structure
- Run tests after EVERY change

**Refactoring Checklist**:
- [ ] Remove duplication (DRY principle)
- [ ] Improve readability
- [ ] Simplify complex logic
- [ ] Ensure consistent style
- [ ] All tests remain green

### Phase 5: Quality Verification
**Objective**: Ensure implementation meets standards

Perform comprehensive validation:
1. Run entire test suite
2. Check code coverage metrics
3. Review for missing test cases
4. Verify performance characteristics
5. Ensure documentation is updated

**Quality Metrics**:
- Test Coverage: [target percentage]
- All Tests Passing: Yes/No
- Performance: Meets requirements
- Code Quality: Follows standards

### Phase 6: Final Commit
**Objective**: Deliver complete, tested feature

Use the `committer` sub-agent to:
- Review complete implementation
- Verify all quality checks pass
- Create commit: "feat: implement [feature] with full test coverage"
- Update relevant documentation

**Final Checklist**:
- [ ] All tests pass
- [ ] Code is clean and documented
- [ ] Feature works as specified
- [ ] Changes are atomic and focused

## TDD Principles Enforcement

**Core Rules** (NEVER violate):
1. No production code without failing test
2. Write minimal code to pass tests
3. Refactor only with green tests
4. One logical change at a time
5. Tests are the specification

## Iteration Strategy

If tests reveal gaps or issues:
1. **Stop implementation immediately**
2. **Write additional failing tests**
3. **Restart implementation cycle**
4. **Document learning for future**

## Success Metrics

Track and report:
- Number of tests written: [count]
- Test execution time: [seconds]
- Code coverage achieved: [percentage]
- Refactoring iterations: [count]
- Total implementation time: [duration]

## Common Pitfalls to Avoid

- Writing tests after code (not TDD)
- Writing too much code at once
- Skipping refactoring phase
- Not running tests frequently
- Testing implementation instead of behavior
- Coupling tests to implementation details

Begin with Phase 1: Test Planning & Writing. Think carefully about what behaviors need testing.