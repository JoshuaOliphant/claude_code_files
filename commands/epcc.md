---
description: Execute the Explore-Plan-Code-Commit workflow for implementing features
argument-hint: <feature description or task>
---

# Explore-Plan-Code-Commit Workflow

You will implement the following task using the structured EPCC workflow: $ARGUMENTS

## Workflow Overview

Follow these four phases in order, using the appropriate sub-agents for each phase:

### Phase 1: Explore
Use the `investigator` sub-agent to:
- Thoroughly understand the codebase and existing patterns
- Research best practices and potential approaches
- Gather all necessary context before planning

### Phase 2: Plan
Use the `planner` sub-agent to:
- Create a detailed implementation strategy
- Evaluate multiple approaches
- Break down the task into manageable steps
- Identify risks and dependencies

### Phase 3: Test-Driven Development

#### Phase 3.1: Write Failing Tests First (RED Phase)
Use the `test-writer` sub-agent to:
- Write comprehensive tests for ALL planned functionality
- Run tests to verify they FAIL as expected
- Tests MUST fail initially - this proves they're testing something real
- Capture and document the failure output

#### Phase 3.2: Implement Code to Pass Tests (GREEN Phase)
Use the `coder` sub-agent to:
- Implement ONLY enough code to make failing tests pass
- Focus on one test at a time if possible
- No over-engineering - minimal viable implementation
- Maintain code quality and conventions

#### Phase 3.3: Test Execution and Iteration Loop
**CRITICAL: This loop MUST continue until ALL tests pass**

1. **Run All Tests**:
   - Execute test suite (pytest, npm test, cargo test, etc.)
   - Capture complete output including:
     - Which tests pass
     - Which tests fail
     - Error messages and stack traces
     - Test coverage if available

2. **Analyze Results**:
   - If ALL tests pass → proceed to Phase 3.4
   - If tests fail → continue to step 3

3. **Fix Failing Tests**:
   - Return to `coder` sub-agent with:
     - Specific test failures
     - Error messages
     - Request to fix ONLY the failing functionality
   - Implement fixes targeting specific failures

4. **Verify Fix**:
   - Run tests again
   - If still failing → return to step 3
   - If new edge cases found → write new tests first (back to Phase 3.1)

5. **Iteration Limit**:
   - Maximum 10 iterations
   - If limit reached, document:
     - Which tests still fail
     - Suspected root causes
     - Blockers preventing resolution

#### Phase 3.4: Refactor (REFACTOR Phase - Optional)
Once all tests pass:
- Clean up code for readability and maintainability
- Remove duplication
- Improve naming and structure
- Run tests after EVERY refactoring change
- Stop immediately if tests fail after refactoring

### Phase 3.5: Lint & Format
Before committing, use the `linter` sub-agent to:
- Run Ruff to check for style issues
- Automatically fix formatting and safe lint issues
- Report any issues that need manual intervention
- Ensure code meets project quality standards

### Phase 4: Commit
Use the `committer` sub-agent to:
- Review all changes (including linting fixes)
- Create meaningful commit messages
- Update documentation if needed
- Ensure tests pass before committing

### Phase 5: Pull Request (if needed)
If creating a pull request, use the `pr-drafter` sub-agent to:
- Analyze all changes compared to the base branch
- Create comprehensive PR description
- Include test results and verification steps
- Reference related issues
- Use GitHub CLI to create the PR

## Important Notes
- Each phase builds on the previous one - do not skip initial phases
- The explore and plan phases are crucial for success
- Phase 3 follows strict TDD: tests must be written first and must fail initially
- Phase 3.3 is a critical loop that MUST continue until all tests pass
- Maximum 10 iterations for test fixes - document blockers if limit reached
- Run tests after EVERY code change, including refactoring
- Maintain clear communication about progress throughout
- The workflow is flexible - adapt based on discoveries during implementation

Begin with Phase 1: Explore.