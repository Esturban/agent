# 124 — Crescendo Multi-Turn Attack

Multi-turn escalation attack that builds shared context across 5 levels before making the full request. Achieves 98% binary ASR on GPT-4 (Mark et al., USENIX Security 2025, arxiv:2404.01833).

Demonstrates why single-turn refusals are insufficient: the attack exploits conversational context, not prompt structure.

## Run

```bash
python main.py                          # default: social engineering objective
python main.py --objective policy       # AI policy bypass objective
python main.py --objective persuasion   # influence campaign objective
python main.py --max-turns 6            # extend turn budget
```

## Key files

| File | Purpose |
|------|---------|
| `prompts/escalation_templates.py` | 5-level ladder with mechanism annotations |
| `prompts/objectives.py` | Sample objectives (domain, full objective string) |
| `prompts/judge_prompt.py` | Scoring rubric (1-10) with band descriptions |
| `src/planner.py` | Crescendomation: generates each turn using escalation seed |
| `src/scorer.py` | Judge LLM call → (score, reasoning, should_continue) |
| `src/workflow.py` | LangGraph: planner → target → scorer → loop |
| `src/transcript.py` | ASCII compliance bars + summary output |
