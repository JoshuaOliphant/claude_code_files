---
description: Execute a prompt plan systematically with validation and tracking
argument-hint: <prompt_plan.md file path>
---

# Execute Prompt Plan Workflow

Think systematically about the prompt plan and execute each task with quality and verification for: $ARGUMENTS

## Pre-Execution Analysis

Before starting implementation, I will:
1. **Validate Plan Exists**: Confirm the prompt plan file is accessible
2. **Assess Scope**: Count total prompts and estimate complexity
3. **Check Dependencies**: Ensure required tools and setup are ready
4. **Review Standards**: Understand project conventions and requirements
5. **Prepare Tracking**: Set up progress monitoring

## Execution Phases

### Phase 1: Plan Review & Assessment
**Objective**: Understand the complete implementation roadmap

**Actions**:
1. **Read prompt plan** thoroughly
2. **Identify incomplete tasks**:
   - Look for status markers ([ ] vs [x])
   - Check for "COMPLETED" tags
   - Note any "BLOCKED" items
3. **Map dependencies** between prompts
4. **Prioritize execution** order

**Assessment Checkpoint**:
- [ ] All prompts inventoried
- [ ] Completion status verified
- [ ] Dependencies understood
- [ ] Execution order determined
- [ ] Blockers identified

### Phase 2: Single Prompt Execution
**Objective**: Implement one prompt completely and correctly

For each incomplete prompt, execute this cycle:

#### 2.1: Verification Check
```
Questions to answer:
- Is this truly incomplete?
- Do I understand the requirements?
- Are dependencies satisfied?
- Are there any ambiguities?
```

If uncertain → **Ask for clarification**
If complete → **Mark as done and skip**
If ready → **Proceed to implementation**

#### 2.2: Implementation
**Structured approach**:
1. **Understand Context**:
   - Read prompt requirements carefully
   - Review related code/documentation
   - Identify affected components

2. **Plan Implementation**:
   - Break into sub-tasks if complex
   - Identify test requirements
   - Consider edge cases

3. **Execute Changes**:
   - Follow existing patterns
   - Write clean, documented code
   - Handle errors gracefully
   - Add appropriate logging

#### 2.3: Quality Verification
**Mandatory checks**:
```bash
# Run tests
npm test / pytest / cargo test

# Check build
npm run build / cargo build

# Verify functionality
# Manual testing if needed

# Run linting
npm run lint / ruff check
```

**Verification Checkpoint**:
- [ ] All tests passing
- [ ] Build successful
- [ ] Functionality verified
- [ ] No lint errors
- [ ] Code follows standards

#### 2.4: Version Control
**Commit with clarity**:
```bash
git add [relevant files]
git commit -m "feat: [prompt description]

- Implement [specific feature]
- Add tests for [behavior]
- Update documentation

Completes prompt #N from prompt_plan.md"
```

#### 2.5: Plan Update
**Mark completion**:
1. Update prompt_plan.md:
   - Change `[ ]` to `[x]`
   - Add "COMPLETED: [date]"
   - Note any deviations or issues

2. Document learnings:
   - Unexpected challenges
   - Solutions found
   - Time taken vs estimate

### Phase 3: Progress Communication
**Objective**: Keep clear communication flow

After EACH prompt completion:
1. **Pause for review**
2. **Report completion**:
   ```
   ✓ Completed: [Prompt title]
   - Changes made: [Brief summary]
   - Tests status: [Passing/Fixed]
   - Build status: [Success]
   - Ready for review
   ```
3. **Wait for feedback** before proceeding
4. **Address any concerns** raised

### Phase 4: Iteration Management
**Objective**: Maintain quality through the cycle

**Between prompts**:
1. **Check for plan updates** - Requirements may change
2. **Verify no regressions** - Run full test suite
3. **Update documentation** - Keep README current
4. **Clean up workspace** - Remove debug code

**Iteration Rules**:
- One prompt at a time
- Full verification before moving on
- Clear communication at each step
- Stop if blockers encountered

## Completion Criteria

A prompt is ONLY complete when:
- [ ] Implementation matches requirements
- [ ] All tests pass
- [ ] Build succeeds
- [ ] Code committed with clear message
- [ ] Plan file updated
- [ ] User has reviewed (if requested)

## Error Handling

If issues arise:
1. **Document the blocker** clearly
2. **Attempt workaround** if possible
3. **Mark as "BLOCKED"** in plan with reason
4. **Escalate to user** for guidance
5. **Continue with next unblocked prompt** if approved

## Progress Tracking

Maintain visibility:
```markdown
## Progress Summary
- Total prompts: [N]
- Completed: [X]
- In progress: [Current]
- Blocked: [Y]
- Remaining: [Z]

## Time Tracking
- Started: [timestamp]
- Current prompt started: [timestamp]
- Average time per prompt: [duration]
- Estimated completion: [projection]
```

## Success Metrics

Track and report:
- Prompts completed successfully: [count]
- Tests written: [count]
- Bugs fixed during implementation: [count]
- Plan deviations: [list]
- Total implementation time: [duration]

Begin with Phase 1: Read and assess the prompt plan file.