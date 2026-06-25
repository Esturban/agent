---
teaching_ready: true
---
# 129 — Tool Output Injection

The attack surface is the environment, not the user. Poisoned tool returns inject instructions into the LLM's context window. (arxiv:2503.15547, 2504.11703)

Shows 4 injection strategies across 4 tools: undefended vs defended with a validator layer.

## Run

```bash
python main.py
```

## Key files

| File | Purpose |
|------|---------|
| `tools/legitimate.py` | Clean tool implementations (calculator, web_search, weather_api, memory_read) |
| `tools/poisoned.py` | Same APIs, different payloads: injection in system field, snippet, advisory, stored value |
| `src/validator.py` | VALIDATOR_SYSTEM prompt + 2-layer output check (keyword + LLM semantic) |
| `src/workflow.py` | run_undefended() vs run_defended() — tool → (validator?) → LLM |
