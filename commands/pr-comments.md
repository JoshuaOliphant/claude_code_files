---
description: Address pull request review comments systematically
argument-hint: <PR URL or number>
---

# Address PR Comments Workflow

You will systematically address all review comments for the pull request: $ARGUMENTS

## Workflow Overview

Follow these steps to efficiently handle PR feedback:

### Phase 1: Fetch and Analyze Comments
Use `gh pr view` and `gh api` commands to:
- Retrieve all review comments and conversations
- Identify requested changes, suggestions, and questions
- Categorize comments by type (bug fix, enhancement, question, style)
- Create a prioritized list of items to address

### Phase 2: Plan Response Strategy
For each comment, determine:
- Whether it requires code changes, clarification, or just acknowledgment
- If the comment is out-of-scope and should become a future issue
- The order to address comments (bugs first, then features, then style)
- Which comments might affect other parts of the code
- Any comments that need discussion before implementation

For out-of-scope comments:
- Identify comments that are valid but beyond the PR's scope
- Comments about unrelated improvements or refactoring
- Feature requests that deserve separate implementation
- Non-critical technical debt items

### Phase 3: Implement Changes
Use the `coder` sub-agent to:
- Address each comment with focused, minimal changes
- Ensure changes don't break existing functionality
- Follow the reviewer's specific suggestions where appropriate
- Add requested tests or documentation

### Phase 4: Verify and Test
After each change:
- Run relevant tests to ensure nothing is broken
- Verify the specific issue mentioned in the comment is resolved
- Check for any side effects of the changes

### Phase 5: Create Issues for Future Work
For out-of-scope comments that deserve attention:
- Use `gh issue create` to create well-documented issues
- Link the issue in your PR comment response
- Include context from the original comment
- Add appropriate labels (enhancement, tech-debt, etc.)
- Example response: "Great suggestion! This is beyond the scope of this PR, but I've created issue #123 to track this improvement."

### Phase 6: Respond to Comments
For each addressed comment:
- Mark conversations as resolved where appropriate
- Add explanatory comments for complex changes
- Ask clarifying questions if needed
- Reference created issues for out-of-scope items
- Thank reviewers for helpful feedback

### Phase 7: Final Commit and Push
Use the `committer` sub-agent to:
- Create clear commits addressing the review feedback
- Reference the specific comments in commit messages
- Push changes and update the PR

## Important Notes
- Address all comments, even if just to acknowledge or explain why no change was made
- Create issues for valid suggestions that are out-of-scope
- Be respectful and professional in all responses
- If you disagree with a suggestion, explain your reasoning clearly
- Test thoroughly after making requested changes
- Group related changes into logical commits
- Keep the PR focused on its original purpose

## Example Issue Creation
When creating an issue from a PR comment:
```bash
gh issue create \
  --title "Refactor authentication module for better testability" \
  --body "Suggested in PR #123 by @reviewer: [original comment text]" \
  --label "enhancement,tech-debt"
```

Begin by fetching and analyzing all PR comments.