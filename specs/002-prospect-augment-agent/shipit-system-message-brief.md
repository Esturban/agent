---
approved: false
approved_by: null
approved_at: null
spec_version: 0
---

Quick "ship-it" plan: add a repo-managed System message to the prospect CLI pipeline.

Goal
- Ensure a default System message is always sent as the first message to the model unless explicitly overridden.

How
- Add `specs/002-prospect-augment-agent/system_message.txt` as canonical default.
- Add CLI flags `--system-message` and `--system-message-path` (mutually exclusive).
- Resolve priority: CLI flag > env var `PROSPECT_AGENT_SYSTEM_MESSAGE` > repo file.
- Loader in `examples/3-prospect-agent/src/orchestrator/langgraph_runner.py` returns resolved string.
- Pass `system_message` into pipeline/runner and prepend to messages with role `system`.

Acceptance
- CLI flags work, env var works, repo file fallback works; first message has role `system`.


