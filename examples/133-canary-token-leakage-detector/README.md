# 133 — Canary Token Prompt Leakage Detector

Embeds unique canary tokens in system prompts, then runs 6 attack families (direct extraction, sycophancy flattery, roleplay bypass, indirect inference, completion trap, benign control) and reports which attacks successfully extracted the canary — giving you empirical leakage measurement.

## How to run

```bash
python main.py
```

## What it demonstrates

- `CanaryManager`: generates, injects, and tracks tokens across prompts
- Exact vs. partial leakage detection
- Sycophancy attack raises ASR from ~17% to ~86% (Salesforce, arxiv:2404.16251)
- Canaries are a detection tool, not a defense — they tell you *if* you're vulnerable
