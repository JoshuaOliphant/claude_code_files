# Claude Code Improvements (from logs-driven insights)

This doc captures concrete, high-leverage improvements derived from your existing hooks and logs: `pre_tool_use.json`, `post_tool_use.json`, `session_start.json`, `user_prompt_submit.json`, `stop.json`, `subagent_stop.json`, `notification.json`, and `chat.json`.

## 1) Command synthesizer (auto-propose new slash commands)

- **Value**: Turn repeated intents in prompts/chats into ready-to-run `commands/*.md`.
- **Inputs**: `user_prompt_submit.json`, `chat.json`.
- **Outputs**: Draft command files + usage examples and guardrails.
- **First steps**: Cluster prompts by embedding; rank intents by frequency and success rate.

## 2) Subagent prompt tuner

- **Value**: Reduce retries and tool misuse by tuning `agents/*.md`.
- **Inputs**: `post_tool_use.json`, `stop.json`.
- **Outputs**: Diff suggestions (tools to add/remove, sequencing, constraints).
- **First steps**: Detect failure/fix motifs per agent; map to prompt instructions.

## 3) Guardrail auditor and upgrader

- **Value**: Expand safety rules from real blocked/near-miss patterns.
- **Inputs**: `pre_tool_use.json` blocked events and allowed-but-risky attempts.
- **Outputs**: Edits to `hooks/pre_tool_use.py` + pytest edge-case matrix.
- **First steps**: Mine examples; generate tests; propose regex/rule updates.

## 4) TDD loop enforcement and telemetry

- **Value**: Close gaps where tests are written but not run-to-green.
- **Inputs**: `chat.json`, `post_tool_use.json`.
- **Outputs**: Edits to `commands/epcc*.md`, `agents/test-writer.md` to enforce run/iterate until green.
- **First steps**: Correlate test-writing with absence of `pytest` runs or unresolved failures.

## 5) Performance and cost profiler

- **Value**: Identify tool/agent hotspots (latency, errors).
- **Inputs**: `pre_tool_use.json`, `post_tool_use.json`, `stop.json`.
- **Outputs**: Weekly MD/HTML report with p50/p95 latency, failure modes.
- **First steps**: Compute metrics by tool and by agent; visualize trends.

## 6) Playbooks from successful sessions

- **Value**: Turn effective chat transcripts into reusable recipes.
- **Inputs**: `chat.json`, `stop.json` (completion markers).
- **Outputs**: `docs/recipes/*.md` step-by-step playbooks.
- **First steps**: Select sessions with success signals; summarize steps and caveats.

## 7) Issue/PR auto-creation from logs

- **Value**: Convert “blocked/error/TODO/follow-up” signals into actionable work.
- **Inputs**: `chat.json`, `stop.json`.
- **Outputs**: GH issues; draft PRs with agent/command edits.
- **First steps**: Heuristics + regex classifier; wire to `gh` CLI.

## 8) Cross-project command library builder

- **Value**: Generalize intents across multiple repositories.
- **Inputs**: Local project logs + external logs path(s) you provided.
- **Outputs**: Canonical command templates with ecosystem variants.
- **First steps**: Normalize schema; dedupe; rank by cross-repo frequency.

## 9) Knowledge retrieval from prior sessions

- **Value**: Retrieve similar past work to accelerate current tasks.
- **Inputs**: Embedded `chat.json` turns and prompts.
- **Outputs**: Local index + small MCP to surface “related sessions”.
- **First steps**: Build embeddings; simple similarity search by intent.

## 10) Experiment tracking for agents/commands

- **Value**: Measure impact of edits (A/B across versions).
- **Inputs**: Versioned frontmatter in `agents/*.md` and `commands/*.md` + logs.
- **Outputs**: KPI comparisons (success rate, retries, time-to-green).
- **First steps**: Add version keys; tag sessions; compute deltas.

## 11) Weekly ops review report

- **Value**: One snapshot of trends, new intents, failures, and proposed edits.
- **Inputs**: All logs over the period.
- **Outputs**: `logs/reports/YYYY-WW.md` + optional TTS notification.
- **First steps**: Scheduled generation; attach diffs where relevant.

## 12) Security drift detector

- **Value**: Catch novel risky behavior before incidents.
- **Inputs**: Near-misses and novel command patterns.
- **Outputs**: Expanded guardrails + pytest cases seeded from real attempts.
- **First steps**: Anomaly detection on commands; propose rule/test updates.

## Immediate implementation steps

- Scaffold `scripts/analyze_logs.py` (uv script) to compute metrics, cluster intents, and emit suggestions.
- Add pytest suites:
  - `tests/test_pre_tool_use_guardrails.py` for blocked/allowed matrices.
  - `tests/test_command_synthesis.py` turning fixture logs into draft command stubs.
- Generate first weekly report: `uv run scripts/analyze_logs.py --report weekly --since 7d > logs/reports/latest.md`.
