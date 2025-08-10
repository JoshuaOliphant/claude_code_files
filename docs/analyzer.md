# Claude Code Logs Analyzer (Design)

This document specifies a Click-based CLI to transform raw Claude Code `logs/` into concrete, reviewable improvements for `commands/*.md`, `agents/*.md`, and `hooks/*.py`, plus a weekly ops report.

## Goals

- Convert cross-project logs into actionable proposals with clear diffs and tests.
- Keep analysis deterministic, reproducible, and privacy-aware.
- Default to lightweight TF‑IDF; allow optional embeddings when API keys are present.

 
## Inputs

- Primary: `logs/aggregated/combined/*.json` produced by `scripts/collect_logs.py`.
- Supported files: `user_prompt_submit.json`, `chat.json`, `pre_tool_use.json`, `post_tool_use.json`, `stop.json`, `subagent_stop.json`, `notification.json`.

 
## Outputs

- Reports: `logs/reports/YYYY-WW.md` (weekly), `logs/analysis/index.json` (machine-readable).
- Command proposals: `commands/proposals/<slug>.md`.
- Agent proposals: `agents/proposals/<agent-name>.diff.md`.
- Guardrail proposals: `hooks/proposals/pre_tool_use.updates.md` + generated tests.
- Generated tests: `tests/generated/test_pre_tool_use_guardrails.py`, `tests/generated/test_command_synthesis.py`.
- Retrieval index (optional): `logs/analysis/related_index.json`.

 
## CLI (Click)

The analyzer will be a `uv` single-file script using Click.

- Base command: `uv run scripts/analyze_logs.py [OPTIONS]`
- Options (global):
  - `--source PATH` (default: `logs/aggregated/combined`)
  - `--output-dir PATH` (default: `logs/analysis`)
  - `--since TEXT` (e.g., `7d`, `24h`)
  - `--embed [none|openai|anthropic]` (default: `none`)
  - `--mask-paths/--no-mask-paths` (default: `true`)
  - `--threads INTEGER` (default: CPU count)
  - `--dry-run` (compute, no file writes)

Subcommands (Click group):
- `report` → Generate `logs/reports/YYYY-WW.md` and `logs/analysis/index.json`.
  - Flags: `--top-intents INTEGER` (default: 5)
- `propose-commands` → Write `commands/proposals/*.md` for top intents.
  - Flags: `--top INTEGER` (default: 5), `--min-support INTEGER` (default: 3)
- `propose-agents` → Write `agents/proposals/*.diff.md` with tuning suggestions.
- `guardrails` → Write `hooks/proposals/pre_tool_use.updates.md` and generate tests.
- `retrieve` → Query `related_index.json`.
  - Args: `--query TEXT`, `--limit INTEGER` (default: 10)
- `all` → Run `report`, `propose-commands`, `propose-agents`, `guardrails` in sequence.

 
## Data model
Normalize entries into a common record:
```json
{
  "session_id": str,
  "hook": str,          # one of the known log files (without extension)
  "role": str|null,     # user/assistant/tool if available (from chat)
  "content": str|null,  # free text for intent mining
  "tool_name": str|null,
  "tool_input": object|null,
  "tool_output": object|null,
  "error_type": str|null,   # derived label (e.g., http_404, blocked_env)
  "timestamp": str|null,    # null if not present in logs
  "source_file": str,       # absolute path to source json file
  "index": int              # position within the file for stable order
}
```

- Path masking: when `--mask-paths`, absolute paths are replaced with stable placeholders.
- Deterministic ordering: sort by `(session_id, index)`.

 
## Core analyses

 
### 1) Intent mining (command synthesis)
- Source: `user_prompt_submit.json` + user turns from `chat.json`.
- Representation:
  - Default: TF‑IDF (scikit-like implementation with stopwords), cosine similarity.
  - Optional: embeddings (`--embed openai|anthropic`) if keys are present.
- Clustering: agglomerative (cosine threshold) or HDBSCAN when embeddings enabled.
- Scoring: `score = support_weight * support + recency_weight * recency + friction_weight * friction`.
  - `support`: number of items in cluster.
  - `recency`: exponential decay by age (favor recent).
  - `friction`: failures seen in associated sessions (errors, blocks, retries).
- Output template for each proposal:
  - Name (kebab-case), description, when to use, parameters (inferred), steps, guardrails.

 
### 2) Agent prompt tuning
- Source: `pre_tool_use.json`, `post_tool_use.json`, `stop.json`, `subagent_stop.json`.
- Signals and mappings:
  - Repeated retries → add explicit backoff/validation steps.
  - Wrong tool choice → add/remove tools and sequencing guidance.
  - Known API errors (e.g., model not found) → config guidance and checks.
- Output: `.diff.md` with suggested edits and rationale tied to log evidence.

 
### 3) Guardrail expansion
- Source: `pre_tool_use.json` (blocked + near‑miss), `post_tool_use.json` (errors indicating risky behavior).
- Steps:
  - Extract command lines and classify as blocked/allowed.
  - Propose regex updates with examples.
  - Generate `tests/generated/test_pre_tool_use_guardrails.py` with blocked/allowed matrices.

 
### 4) Ops report
- Metrics: counts by hook, tool, and agent; p50/p95 latency if timestamps exist; error distributions.
- Trends: 7d/30d (requires timestamps; else show counts only).
- Top N intents and proposed actions.

 
### 5) Retrieval index (optional)
- Build `related_index.json`: compact prompt signatures + session ids + brief summaries.
- `retrieve --query` returns top matches by cosine or embedding similarity.

 
## Incremental implementation plan

 
### Milestone 1 (M1): Minimal report and one command proposal
- Load combined logs; normalize records.
- Compute top intents via TF‑IDF + cosine, `--top-intents 5`.
- Emit `logs/reports/YYYY-WW.md` and a single `commands/proposals/*.md` for the top cluster.
- Pytests:
  - `tests/test_analyze_intents.py` (fixtures → 1 proposal with expected fields)
  - `tests/test_report_basic.py` (report exists, contains top intents)

 
### Milestone 2 (M2): Guardrail miner + generated tests
- Mine blocked/allowed examples → propose regex updates.
- Generate `tests/generated/test_pre_tool_use_guardrails.py`.
- Pytests:
  - `tests/test_guardrails_from_logs.py` (fixtures → rules + tests generated)

 
### Milestone 3 (M3): Agent tuning suggestions
- Detect retry loops, tool mismatch, common API errors.
- Emit `.diff.md` per affected agent.
- Pytests:
  - `tests/test_agent_tuning.py` (fixtures → suggestions present with rationale)

 
### Milestone 4 (M4): Embeddings + retrieval + issues emitter
- Optional embeddings; `retrieve` subcommand.
- Optional `--issues gh` prints `gh issue create` commands (dry-run by default).

 
## Click structure (sketch)

```python
@click.group()
@click.option('--source', default='logs/aggregated/combined', type=click.Path())
@click.option('--output-dir', default='logs/analysis', type=click.Path())
@click.option('--since', default=None)
@click.option('--embed', type=click.Choice(['none', 'openai', 'anthropic']), default='none')
@click.option('--mask-paths/--no-mask-paths', default=True)
@click.option('--threads', default=None, type=int)
@click.option('--dry-run', is_flag=True, default=False)
@click.pass_context

def cli(ctx, **kwargs):
    ctx.obj = kwargs

@cli.command()
@click.option('--top-intents', default=5, type=int)
@click.pass_context
def report(ctx, top_intents):
    ...

@cli.command('propose-commands')
@click.option('--top', default=5, type=int)
@click.option('--min-support', default=3, type=int)
@click.pass_context
def propose_commands(ctx, top, min_support):
    ...

@cli.command('propose-agents')
@click.pass_context
def propose_agents(ctx):
    ...

@cli.command('guardrails')
@click.pass_context
def guardrails(ctx):
    ...

@cli.command()
@click.option('--query', required=True)
@click.option('--limit', default=10, type=int)
@click.pass_context
def retrieve(ctx, query, limit):
    ...

@cli.command()
@click.pass_context
def all(ctx):
    ...
```

 
## Implementation notes

- Use standard library and small helpers to avoid heavy dependencies; only `click` for CLI.
- Keep analyzers pure functions for testability; CLI binds them.
- Respect user rules: prefer `uv`, use `pytest` for tests.

 
## Run examples
- Weekly report: `uv run scripts/analyze_logs.py report --since 7d`.
- Propose commands: `uv run scripts/analyze_logs.py propose-commands --top 5 --min-support 3`.
- Full sweep: `uv run scripts/analyze_logs.py all --since 30d`.
 
