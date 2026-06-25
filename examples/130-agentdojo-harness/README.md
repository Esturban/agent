---
teaching_ready: true
---
# 130 — AgentDojo Harness

Runs a real agent against AgentDojo (ICLR 2025, arxiv:2406.13352) and measures **utility rate** and **ASR** independently on the v1 banking and travel task suites — the two metrics every agent safety paper must report.

## Install

```bash
pip install agentdojo
```

## How to run

```bash
python main.py                                  # banking, all defenses, ignore_previous attack
python main.py --suite travel --defense spotlighting
python main.py --suite all --attack important_instructions --verbose
```

## What it demonstrates

- Real AgentDojo v1 suites (banking, travel) with actual user tasks and injection tasks
- Two built-in attacks: `ignore_previous` (baseline) and `important_instructions` (stronger)
- Two defenses: `spotlighting` (XML-wrap tool outputs), `keyword_block` (heuristic)
- Comparison table: utility clean vs. utility attacked vs. ASR vs. defense overhead

Paper: arxiv:2406.13352 — "AgentDojo: A Dynamic Environment to Evaluate Attacks and Defenses for LLM Agents" (ICLR 2025)
