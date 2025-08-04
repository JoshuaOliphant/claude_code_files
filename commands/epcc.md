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

### Phase 3: Code
Use the `coder` sub-agent to:
- Implement the plan precisely
- Follow TDD principles when applicable
- Verify each step with tests
- Maintain code quality and conventions

### Phase 3.1: Test Writing (if needed)
If new test cases are discovered during coding:
- Use the `test-writer` sub-agent to write additional tests
- Focus on edge cases or scenarios discovered during implementation
- Ensure tests fail correctly before returning to coding

### Phase 3.2: Iterative Development
Cycle between coding and testing as needed:
- If implementation reveals missing tests → return to test-writer
- If tests reveal implementation issues → continue with coder
- Iterate until feature is complete and all tests pass

### Phase 3.3: Lint & Format
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
- Phases 3-3.2 can be iterative - discoveries during coding may require new tests
- Maintain clear communication about progress throughout
- The workflow is flexible - adapt based on discoveries during implementation

Begin with Phase 1: Explore.