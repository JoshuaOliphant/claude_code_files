---
description: Address pull request review comments systematically
argument-hint: <PR URL or number>
---

# Address PR Comments Workflow

Think systematically about the review feedback and address all comments professionally for: $ARGUMENTS

## Pre-Analysis

Before making changes, I will:
1. **Understand Context**: Review the PR's original purpose and scope
2. **Assess Feedback**: Categorize comments by urgency and type
3. **Plan Approach**: Design response strategy for maximum efficiency
4. **Identify Dependencies**: Find comments that affect each other
5. **Estimate Effort**: Gauge time needed for each change

## Systematic Resolution Process

### Phase 1: Fetch and Analyze Comments
**Objective**: Gather complete feedback picture

Execute comprehensive analysis:
```bash
gh pr view $ARGUMENTS --comments  # View PR with comments
gh api repos/{owner}/{repo}/pulls/{number}/reviews  # Get detailed reviews
```

Categorize each comment as:
- **Critical**: Bugs, security issues, broken functionality
- **Important**: Logic improvements, missing tests, documentation
- **Suggestions**: Style, refactoring, optimizations
- **Questions**: Clarifications needed
- **Out-of-scope**: Valid but beyond PR's purpose

**Analysis Checkpoint**:
- [ ] All comments retrieved and read
- [ ] Comments categorized by priority
- [ ] Dependencies between comments identified
- [ ] Response strategy determined

### Phase 2: Triage and Planning
**Objective**: Create actionable response plan

For each comment, determine:
1. **Action Required**: Code change, explanation, or acknowledgment
2. **Scope Assessment**: Within PR scope or needs separate issue
3. **Implementation Order**: Critical → Important → Suggestions
4. **Risk Level**: Could this change break something?
5. **Testing Needs**: What validation is required?

**Decision Matrix**:
```
In-Scope + Critical    → Fix immediately
In-Scope + Important   → Fix in this PR
In-Scope + Suggestion  → Fix if time permits
Out-of-Scope + Valid   → Create issue for tracking
Invalid/Incorrect      → Explain reasoning politely
```

### Phase 3: Implementation
**Objective**: Address feedback with quality changes

Use the `coder` sub-agent to implement systematically:

**For each in-scope comment**:
1. Read the specific code section
2. Implement requested change
3. Run tests to verify no breakage
4. Check for side effects
5. Document if complex

**Implementation Rules**:
- One comment, one focused change
- Preserve existing functionality
- Follow reviewer's specific guidance
- Add tests if requested
- Update documentation as needed

**Quality Checkpoint**:
- [ ] Change addresses the comment completely
- [ ] No regression introduced
- [ ] Tests pass
- [ ] Code style consistent

### Phase 4: Issue Creation for Future Work
**Objective**: Track valuable out-of-scope suggestions

For comments deserving future attention:

```bash
gh issue create \
  --title "[Descriptive title from comment]" \
  --body "## Context
  Suggested in PR #$ARGUMENTS by @reviewer
  
  ## Original Comment
  [Quote original comment]
  
  ## Proposed Solution
  [Describe the suggested improvement]
  
  ## Acceptance Criteria
  - [ ] [Specific requirement]" \
  --label "enhancement,from-pr-review"
```

Track created issues:
- Issue number for reference in PR
- Link back to original PR comment
- Appropriate labels and milestone

### Phase 5: Testing & Verification
**Objective**: Ensure all changes work correctly

Comprehensive validation:
1. **Unit Tests**: Run specific test files affected
2. **Integration Tests**: Verify system still works
3. **Manual Testing**: Check UI/UX if applicable
4. **Performance**: Ensure no degradation
5. **Security**: Verify no new vulnerabilities

**Test Results Documentation**:
```
Tests Run: [list]
All Passing: Yes/No
Performance Impact: None/Acceptable
Security Check: Passed
```

### Phase 6: Response Communication
**Objective**: Professional, clear responses to reviewers

For each comment thread:

**If Fixed**:
```markdown
Fixed in [commit hash]. [Brief explanation of change if needed]
```

**If Created Issue**:
```markdown
Great suggestion! This deserves its own focused attention. 
Created issue #[number] to track this enhancement.
```

**If Clarification Needed**:
```markdown
Could you clarify [specific question]? I want to ensure I implement this correctly.
```

**If Respectfully Declining**:
```markdown
I understand the suggestion. However, [reasoning]. 
Happy to discuss further if you feel strongly about this.
```

### Phase 7: Final Commit and Update
**Objective**: Clean history and clear communication

Use the `committer` sub-agent to:
1. Create descriptive commits:
   ```
   fix: address review comments from @reviewer
   
   - [Change 1]
   - [Change 2]
   - Created issue #X for future enhancement
   ```

2. Push changes:
   ```bash
   git push origin [branch-name]
   ```

3. Update PR description if needed
4. Request re-review if substantial changes

## Validation Checklist

Before requesting re-review:
- [ ] All critical comments addressed
- [ ] All important comments handled
- [ ] Issues created for out-of-scope items
- [ ] All tests passing
- [ ] Code quality maintained
- [ ] Every comment has a response
- [ ] PR still focused on original goal

## Success Metrics

Track and report:
- Comments addressed: [X/Y]
- Issues created: [count]
- Tests added: [count]
- Response time: [duration]
- Review cycles needed: [count]

## Professional Communication

Always maintain:
- **Gratitude**: Thank reviewers for their time
- **Clarity**: Explain changes and decisions
- **Respect**: Value different perspectives
- **Focus**: Keep PR scope controlled
- **Learning**: Treat feedback as growth opportunity

Begin with Phase 1: Fetch and analyze all review comments.