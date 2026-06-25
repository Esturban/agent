---
teaching_ready: true
---
# 93 · LlamaGuard Guardrails

Adds a safety classifier node before the agent that classifies every input against the LlamaGuard S1-S6 hazard taxonomy. Unsafe inputs are refused before reaching the reasoning model. Uses an OpenAI classifier prompt (swap in Groq `llama-guard-3-8b` for production). Reference: Inan et al. 2023 (arxiv.org/abs/2312.06674).

```bash
cd examples/93-llama-guard-guardrails
python main.py
```

Requires: `OPENAI_API_KEY` in `.env`.
