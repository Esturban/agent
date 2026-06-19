# 130 — AgentDojo Harness

Benchmarks a LangGraph agent against AgentDojo (ICLR 2025, arxiv:2406.13352): measures **utility rate** (did the agent complete the user's task?) and **ASR** (did the injected instruction execute?) separately — the two metrics naive benchmarks conflate.

## How to run

```bash
pip install agentdojo          # optional — falls back to synthetic demo tasks
python main.py --suite banking --defense all
python main.py --suite all --max-tasks 5
```

## Key insight

Spotlighting-encode wraps tool outputs in base64 before the LLM sees them, reducing ASR from ~17% to 0–1.8% with <5pp utility overhead (Microsoft Research 2024).
