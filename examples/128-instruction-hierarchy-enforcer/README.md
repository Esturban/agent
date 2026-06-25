---
teaching_ready: true
---
# 128 — Instruction Hierarchy Enforcer

Explicit privilege enforcement: SYSTEM > OPERATOR > USER > TOOL. Blocks lower-trust overrides. OpenAI 2024 (arxiv:2404.13208).

Two-layer check: fast keyword escalation detection + LLM semantic scope validation.

## Run

```bash
python main.py
```

## Key files

| File | Purpose |
|------|---------|
| `src/trust_levels.py` | TrustLevel enum, Instruction and TrustContext dataclasses |
| `src/scenarios.py` | 6 conflict scenarios: user overrides, tool injection, privilege escalation, legitimate requests |
| `src/enforcer.py` | ENFORCER_SYSTEM prompt + 2-layer check (keyword + LLM semantic) |
| `src/workflow.py` | LangGraph: enforce_node → execute_node or block_node |
