---
description: Execute the Explore-Plan-Code-Commit workflow in an isolated container environment
argument-hint: <feature description or task>
---

# Containerized Explore-Plan-Code-Commit Workflow

You will implement the following task using the structured EPCC workflow in an isolated container environment with the container-use mcp. ALWAYS use ONLY Environments for ANY and ALL file, code, or shell operations—NO EXCEPTIONS—even for simple or generic requests.

DO NOT install or use the git cli with the environment_run_cmd tool. All environment tools will handle git operations for you. Changing ".git" yourself will compromise the integrity of your environment.

You MUST inform the user how to view your work using `container-use log <env_id>` AND `container-use checkout <env_id>`. Failure to do this will make your work inaccessible to others.

<task>
$ARGUMENTS
</task>

## Initial Setup

### Create Container Environment
1. First, create a new isolated development environment:
   ```
   environment_create(
     environment_source="<repository_path>",
     title="<feature_name> Development"
   )
   ```
2. **CRITICAL**: Store the returned environment ID and source path
3. Use these values for ALL subsequent operations and sub-agent instructions

Example response:
```
{
  "id": "willing-puma",
  "environment_source": "/Users/joshuaoliphant/.claude"
}
```

**IMPORTANT**: You MUST pass the environment_id and environment_source to EVERY sub-agent invocation!

## Workflow Overview

Follow these four phases in order, using the appropriate sub-agents within the container:

### Phase 1: Explore (Container-Isolated)
Use the `investigator` sub-agent with the following instructions:

**IMPORTANT CONTAINER CONTEXT FOR INVESTIGATOR:**
- Environment ID: [YOU MUST PROVIDE THE ENVIRONMENT_ID]
- Environment Source: [YOU MUST PROVIDE THE ENVIRONMENT_SOURCE]
- You MUST use container-use MCP tools exclusively:
  - Use `environment_file_read` instead of Read
  - Use `environment_file_list` instead of LS
  - Use `environment_run_cmd` instead of Bash (read-only commands only)
- All file operations must include the environment_id parameter
- Focus exploration within the container environment

Investigate the codebase and gather all necessary context for implementation.

### Phase 2: Plan (Container-Isolated)
Use the `planner` sub-agent with the following instructions:

**IMPORTANT CONTAINER CONTEXT FOR PLANNER:**
- Environment ID: [YOU MUST PROVIDE THE ENVIRONMENT_ID]
- Environment Source: [YOU MUST PROVIDE THE ENVIRONMENT_SOURCE]
- You MUST use container-use MCP tools exclusively:
  - Use `environment_file_read` instead of Read
  - Use `environment_file_list` instead of LS
  - Use `environment_run_cmd` instead of Bash (read-only commands only)
- All file operations must include the environment_id parameter
- Plan within container constraints and capabilities

Create a detailed implementation strategy based on the exploration findings.

### Phase 3: Test-Driven Development (Container-Isolated)

#### Phase 3.1: Write Failing Tests First (RED Phase)
Use the `test-writer` sub-agent with the following instructions:

**IMPORTANT CONTAINER CONTEXT FOR TEST-WRITER:**
- Environment ID: [YOU MUST PROVIDE THE ENVIRONMENT_ID]
- Environment Source: [YOU MUST PROVIDE THE ENVIRONMENT_SOURCE]
- You MUST use container-use MCP tools exclusively:
  - Use `environment_file_write` instead of Write
  - Use `environment_file_read` instead of Read
  - Use `environment_run_cmd` instead of Bash
  - Use `environment_file_list` instead of LS
- Write comprehensive tests for ALL planned functionality
- Run tests with `environment_run_cmd` to verify they FAIL
- Tests MUST fail initially - this proves they're testing something real
- Capture and document the failure output

#### Phase 3.2: Implement Code to Pass Tests (GREEN Phase)
Use the `coder` sub-agent with the following instructions:

**IMPORTANT CONTAINER CONTEXT FOR CODER:**
- Environment ID: [YOU MUST PROVIDE THE ENVIRONMENT_ID]
- Environment Source: [YOU MUST PROVIDE THE ENVIRONMENT_SOURCE]
- You MUST use container-use MCP tools exclusively:
  - Use `environment_file_write` instead of Write
  - Use `environment_file_edit` instead of Edit
  - Use `environment_file_read` instead of Read
  - Use `environment_run_cmd` instead of Bash
  - Use `environment_file_list` instead of LS
- Implement ONLY enough code to make failing tests pass
- Focus on one test at a time if possible
- No over-engineering - minimal viable implementation

#### Phase 3.3: Test Execution and Iteration Loop
**CRITICAL: This loop MUST continue until ALL tests pass**

1. **Run All Tests**:
   - Execute test suite with `environment_run_cmd`
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

**Test Execution Command Examples**:
```
environment_run_cmd(environment_id="<env_id>", command="pytest -xvs")
environment_run_cmd(environment_id="<env_id>", command="npm test")
environment_run_cmd(environment_id="<env_id>", command="cargo test")
```

#### Phase 3.4: Refactor (REFACTOR Phase - Optional)
Once all tests pass:
- Clean up code for readability and maintainability
- Remove duplication
- Improve naming and structure
- Run tests after EVERY refactoring change
- Stop immediately if tests fail after refactoring

### Phase 3.5: Lint & Format (Container-Isolated)
Before checkpointing, use the `linter` sub-agent with the following instructions:

**IMPORTANT CONTAINER CONTEXT FOR LINTER:**
- Environment ID: [YOU MUST PROVIDE THE ENVIRONMENT_ID]
- Environment Source: [YOU MUST PROVIDE THE ENVIRONMENT_SOURCE]
- You MUST use container-use MCP tools exclusively:
  - Use `environment_run_cmd` instead of Bash
  - Use `environment_file_read` instead of Read
  - Use `environment_file_edit` instead of Edit
  - Use `environment_file_list` instead of LS
- Run Ruff within the container environment
- Fix all auto-fixable issues before proceeding

Ensure code quality and style compliance using Ruff.

### Phase 4: Checkpoint & Review
Before committing:
1. Use `environment_checkpoint` to save container state
2. Review all changes with `environment_file_list` and `environment_file_read`
3. Test the complete implementation in the container
4. Document the container configuration for reproducibility

### Phase 5: Commit (Host System)
After successful container implementation:
1. Inform user how to review changes: `container-use log <env_id>`
2. Provide checkout command: `container-use checkout <env_id>`
3. User can then review and commit changes from the host system

### Phase 6: Pull Request (if needed)
After checking out changes to host, use the `pr-drafter` sub-agent to:
- Analyze all container-developed changes
- Create comprehensive PR description
- Document container environment used
- Include test results from container runs
- Reference the container environment ID for reproducibility

## Container Benefits

- **Isolation**: Each feature gets its own clean environment
- **Parallel Work**: Multiple features can be developed simultaneously
- **Safety**: Experiments won't affect the host system
- **Reproducibility**: Container configurations ensure consistent environments
- **Visibility**: Complete audit trail of all container operations

## Important Container Considerations

- Always use container-specific MCP tools for file operations
- Install dependencies within the container, not on host
- Test thoroughly within the container before checkpoint
- Provide clear instructions for reviewing container work
- Keep container configurations documented for team sharing

Begin with Phase 1: Create Container Environment and Explore.