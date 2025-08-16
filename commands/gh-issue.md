---
description: Analyze and resolve a GitHub issue with comprehensive fix and testing
argument-hint: <issue number or URL>
---

# GitHub Issue Resolution Workflow

Think systematically about the issue and implement a complete solution for: $ARGUMENTS

## Issue Analysis Phase

Before making any changes, I will:
1. **Fetch Issue Details**: Use `gh issue view` to understand the full context
2. **Analyze Requirements**: Identify what needs to be fixed and why
3. **Assess Impact**: Determine affected components and potential side effects
4. **Plan Approach**: Design the solution strategy before coding

## Resolution Process

### Step 1: Issue Investigation
```bash
gh issue view $ARGUMENTS  # Get full issue details
```
- Read issue description thoroughly
- Review comments and discussions
- Note acceptance criteria if provided
- Identify related issues or PRs

### Step 2: Codebase Analysis
Search for relevant code:
- Use Grep to find related functions/classes
- Use Glob to locate affected files
- Read existing implementation
- Understand current behavior vs expected

### Step 3: Solution Implementation
Implement the fix systematically:
- Make targeted changes to resolve the issue
- Follow existing code patterns and style
- Add necessary error handling
- Update related documentation

### Step 4: Testing & Verification
Ensure the fix is robust:
- Write tests that reproduce the original issue
- Verify tests fail without the fix
- Confirm tests pass with the fix
- Run existing test suite for regressions
- Test edge cases and error conditions

### Step 5: Code Quality
Maintain high standards:
- Run linting (`npm run lint`, `ruff`, etc.)
- Execute type checking if applicable
- Ensure code follows project conventions
- Review changes for clarity and maintainability

### Step 6: Commit & Document
Create clear history:
- Stage relevant files only
- Write descriptive commit message:
  ```
  fix: [brief description of fix]
  
  - [What was broken]
  - [How it was fixed]
  - [Any side effects or considerations]
  
  Fixes #[issue number]
  ```

### Step 7: Pull Request Creation
Submit for review:
```bash
gh pr create --title "Fix: [issue title]" --body "..."
```

PR body should include:
- Link to issue being fixed
- Summary of changes made
- Testing performed
- Screenshots if UI changes
- Breaking changes if any

## Validation Checklist

Before submitting:
- [ ] Issue requirements fully addressed
- [ ] Tests written and passing
- [ ] No regression in existing tests
- [ ] Code follows project standards
- [ ] Documentation updated if needed
- [ ] Commit message references issue
- [ ] PR description is comprehensive

## Success Criteria

The issue is resolved when:
- Original problem no longer occurs
- Solution handles edge cases
- Tests prevent regression
- Code review feedback addressed
- PR merged to main branch

Begin with Step 1: Issue Investigation using GitHub CLI.