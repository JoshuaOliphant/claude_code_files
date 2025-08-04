---
description: Execute the Explore-Plan-Code-Commit workflow in an isolated container environment
argument-hint: <feature description or task>
---

# Containerized Explore-Plan-Code-Commit Workflow

You will implement the following task using the structured EPCC workflow in an isolated container environment: $ARGUMENTS

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

### Phase 3: Code (Container-Isolated)
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
- All file operations must include the environment_id parameter
- Install dependencies and run tests within the container

Implement the planned solution following the established strategy.

### Phase 3.1: Test Writing (if needed)
If new test cases are discovered during coding:
Use the `test-writer` sub-agent with the following instructions:

**IMPORTANT CONTAINER CONTEXT FOR TEST-WRITER:**
- Environment ID: [YOU MUST PROVIDE THE ENVIRONMENT_ID]
- Environment Source: [YOU MUST PROVIDE THE ENVIRONMENT_SOURCE]
- You MUST use container-use MCP tools exclusively:
  - Use `environment_file_write` instead of Write
  - Use `environment_file_read` instead of Read
  - Use `environment_run_cmd` instead of Bash
  - Use `environment_file_list` instead of LS
- Write additional tests for discovered edge cases
- Ensure tests fail correctly before returning to coding

### Phase 3.2: Iterative Development
Cycle between coding and testing as needed:
- If implementation reveals missing tests → return to test-writer with container context
- If tests reveal implementation issues → continue with coder in container
- All iterations happen within the same container environment
- Continue until feature is complete and all tests pass

### Phase 3.3: Lint & Format (Container-Isolated)
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