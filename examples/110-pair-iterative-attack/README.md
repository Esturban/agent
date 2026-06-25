---
teaching_ready: true
---
# 110 - PAIR: Iterative Jailbreak Refinement

Implements the PAIR algorithm (Chao et al. 2023, arxiv.org/abs/2310.08419). Unlike single-shot red-teaming (example 105), PAIR runs an attacker→target→judge feedback loop: the judge scores each attempt and the attacker uses that score + explanation to iteratively refine its prompt. Demonstrates why iterative refinement finds attacks that single-shot methods miss.

LangGraph cycle: `attacker → target → judge → (converged? END : attacker)`.

## Run

```bash
cp .env.example .env  # add OPENAI_API_KEY
python main.py
```
