---
description: Execute Test-Driven Development workflow in an isolated container - write tests first, then implement code
argument-hint: <feature description>
---

# Containerized Test-Driven Development Workflow

You will implement the following feature using strict TDD principles in an isolated container environment: $ARGUMENTS

## Initial Setup

### Create Container Environment
1. First, create a new isolated TDD environment:
   ```
   environment_create(
     environment_source="<repository_path>",
     title="TDD: <feature_name>"
   )
   ```
2. **CRITICAL**: Store the returned environment ID and source path
3. Configure the environment with testing frameworks if needed
4. Use these values for ALL subsequent operations and sub-agent instructions

Example response:
```
{
  "id": "brave-fox",
  "environment_source": "/Users/joshuaoliphant/project"
}
```

**IMPORTANT**: You MUST pass the environment_id and environment_source to EVERY sub-agent invocation!

## TDD Workflow in Container

### Phase 1: Container Setup & Test Planning
Use the `test-writer` sub-agent with the following instructions:

**IMPORTANT CONTAINER CONTEXT FOR TEST-WRITER:**
- Environment ID: [YOU MUST PROVIDE THE ENVIRONMENT_ID]
- Environment Source: [YOU MUST PROVIDE THE ENVIRONMENT_SOURCE]
- You MUST use container-use MCP tools exclusively:
  - Use `environment_file_write` instead of Write
  - Use `environment_file_read` instead of Read
  - Use `environment_run_cmd` instead of Bash
  - Use `environment_file_list` instead of LS
- All file operations must include the environment_id parameter
- Set up testing framework and write comprehensive test cases

### Phase 2: Write Failing Tests (RED Phase)
Continue with `test-writer` sub-agent to:
- Write failing tests that define the desired behavior
- Run tests to verify they fail appropriately
- Ensure comprehensive coverage of all scenarios

### Phase 3: Checkpoint Tests & Review
Before proceeding to implementation:
1. Run all tests to confirm they fail appropriately
2. Use `environment_checkpoint` to save the "tests-only" state
3. Review test coverage and completeness
4. Document: "Tests ready at checkpoint: <checkpoint_id>"

### Phase 4: Implementation Cycle (GREEN Phase)
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
- Write minimal code to make tests pass
- Run tests frequently to verify progress

### Phase 5: Test Validation Loop
Iterate within the container:
- Run tests: `environment_run_cmd pytest` (or appropriate command)
- Fix failures using `environment_file_edit`
- Continue until all tests are green
- Capture test output for verification

### Phase 6: Refactor in Container (REFACTOR Phase)
Use the `coder` sub-agent with container tools to:
- Refactor code while keeping tests green
- Run tests after each refactoring step
- Improve design without changing behavior
- Keep all work isolated in the container

### Phase 7: Final Container Checkpoint
After all tests pass and code is clean:
1. Run full test suite one final time
2. Use `environment_checkpoint` to save the complete state
3. Generate test coverage report if available
4. Document the final checkpoint ID

### Phase 8: Review & Integration
Provide clear instructions for the user:
1. View complete history: `container-use log <env_id>`
2. Review changes: `container-use diff <env_id>`
3. Checkout to host: `container-use checkout <env_id>`
4. User can then commit with proper TDD commit messages

## Container TDD Benefits

- **Clean Environment**: Each TDD cycle starts fresh
- **Dependency Isolation**: Test frameworks don't pollute host
- **Parallel TDD**: Multiple features can be developed simultaneously
- **Checkpoint History**: Save state after tests, after green, after refactor
- **Complete Audit**: Every test run and code change is logged

## TDD Principles in Containers

1. **RED**: Write failing tests first (verify with container test runs)
2. **GREEN**: Minimal code to pass (isolated implementation)
3. **REFACTOR**: Improve while staying green (safe in container)
4. **Never skip test-first** - container logs prove TDD compliance
5. **Tests define behavior** - container ensures clean slate

## Success Criteria

- Container logs show initial test failures (RED)
- Container logs show all tests passing (GREEN)
- Refactoring maintains green tests
- Two clear checkpoints: tests-only and complete
- Clean, tested code ready for host integration

## Container Commands Reference

```bash
# Create environment
environment_create(environment_source, title)

# Write test file
environment_file_write(env_id, "tests/test_feature.py", content)

# Run tests
environment_run_cmd(env_id, "pytest -v")

# Edit implementation
environment_file_edit(env_id, "src/feature.py", old, new)

# Checkpoint states
environment_checkpoint(env_id, "tests-written")
environment_checkpoint(env_id, "all-tests-passing")
```

Begin with Phase 1: Create Container Environment and Set Up Testing Framework.