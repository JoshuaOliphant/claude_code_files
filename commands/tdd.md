---
description: Execute Test-Driven Development workflow - write tests first, then implement code to make them pass
argument-hint: <feature description>
---

# Test-Driven Development Workflow

You will implement the following feature using strict TDD principles: $ARGUMENTS

## Workflow Overview

Follow the TDD red-green-refactor cycle using structured phases with appropriate sub-agents:

### Phase 1: Test Planning & Writing
Use the `test-writer` sub-agent to:
- Understand the feature requirements thoroughly
- Design comprehensive test cases that define the expected behavior  
- Write failing tests that cover all aspects of the feature
- Ensure tests are well-structured and follow testing best practices
- Create tests for happy path, edge cases, and error conditions

### Phase 2: Initial Test Commit
Use the `committer` sub-agent to:
- Review the written tests for completeness and quality
- Commit failing tests with descriptive message like "Add failing tests for [feature]"
- Verify tests actually fail (RED phase of TDD)
- Document test expectations clearly

### Phase 3: Implementation Cycle
Use the `coder` sub-agent to:
- Write minimal code to make the first failing test pass
- Run tests frequently to verify progress
- Implement only what's needed to pass current tests
- Avoid over-engineering or implementing untested features
- Follow existing code patterns and conventions

### Phase 4: Test Validation Loop
Iterate between running tests and coding until:
- All tests pass consistently (GREEN phase of TDD)
- No tests are skipped or ignored
- Code coverage meets requirements
- Implementation is clean and maintainable

### Phase 5: Refactor & Polish
Use the `coder` sub-agent to:
- Refactor code while keeping tests green
- Improve code structure and readability
- Remove duplication and improve design
- Ensure all tests still pass after refactoring

### Phase 6: Final Commit
Use the `committer` sub-agent to:
- Review the complete implementation
- Verify all tests pass and code is clean
- Create meaningful commit message describing the implemented feature
- Ensure documentation is updated if needed

## TDD Principles to Follow

1. **RED**: Write a failing test first
2. **GREEN**: Write minimal code to make it pass  
3. **REFACTOR**: Improve code while keeping tests green
4. **Never write production code without a failing test**
5. **Tests define the API and behavior**
6. **Keep tests simple, focused, and readable**

## Success Criteria

- All tests pass consistently
- Code is well-tested with good coverage
- Implementation follows existing patterns
- Code is clean and maintainable
- Feature works as specified
- Two commits: one for tests, one for implementation

## Important Notes

- **NEVER skip the test-first phase** - this is fundamental to TDD
- Tests should fail initially - if they pass immediately, they're not testing new code
- Write the simplest code possible to make tests pass
- Refactor fearlessly - tests provide the safety net
- Each phase builds on the previous one - maintain discipline
- If implementation reveals test gaps, add more tests and restart the cycle

Begin with Phase 1: Test Planning & Writing.