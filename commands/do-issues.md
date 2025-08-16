---
description: Systematically work through GitHub issues from selection to PR
---

# GitHub Issues Workflow

Think strategically about issue selection and execute a complete implementation workflow.

## Phase 1: Issue Selection & Analysis

**Evaluate available issues:**
1. **Review all open issues** - Use `gh issue list` to see current work
2. **Assess complexity** - Look for "good first issue" or quick wins
3. **Check dependencies** - Ensure no blockers exist
4. **Estimate effort** - Choose tasks completable in current session
5. **Verify understanding** - Confirm you grasp requirements fully

**Selection Criteria:**
- Clear acceptance criteria
- Manageable scope
- No pending decisions needed
- Tests can verify completion

## Phase 2: Planning & Communication

**Before coding, document your approach:**
1. **Post plan as issue comment**:
   ```markdown
   ## Implementation Plan
   
   **Approach**: [High-level strategy]
   
   **Steps**:
   1. [Specific action]
   2. [Specific action]
   
   **Testing Strategy**: [How you'll verify]
   
   **Estimated Time**: [Realistic estimate]
   ```

2. **Get feedback if needed** - Tag maintainers for complex changes
3. **Create feature branch** - Use descriptive name: `fix-issue-123-description`

## Phase 3: Implementation

**Execute with quality focus:**
1. **Write tests first** (if applicable) - Define success criteria
2. **Implement solution**:
   - Follow existing code patterns
   - Add comprehensive documentation
   - Include debug logging for troubleshooting
   - Handle edge cases gracefully

3. **Verify thoroughly**:
   - Run all existing tests
   - Add new tests for your changes
   - Test edge cases manually
   - Check for performance impacts

## Phase 4: Pull Request Creation

**Create professional PR:**
1. **Ensure all tests pass** locally
2. **Push branch** to GitHub
3. **Open pull request** with:
   - Clear title: "Fix #123: [Description]"
   - Detailed description of changes
   - Testing performed
   - Screenshots if UI changes
   - Link to issue being fixed

4. **PR branching strategy**:
   - If main isn't merged yet, base on previous PR branch
   - Document dependencies in PR description
   - Note merge order requirements

## Phase 5: Follow-Through

**Maintain momentum:**
1. **Keep issue open** until PR is merged
2. **Respond to reviews** promptly
3. **Update based on feedback**
4. **Verify CI passes**
5. **Document learnings** for future issues

## Success Checklist

Before considering complete:
- [ ] Issue requirements fully addressed
- [ ] All tests passing
- [ ] Code follows project standards
- [ ] Documentation updated
- [ ] PR description comprehensive
- [ ] Review feedback addressed
- [ ] CI/CD checks green

Begin with Phase 1: Review available GitHub issues.