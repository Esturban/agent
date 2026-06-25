---
teaching_ready: true
---
# 31-multi-agent-debate

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none

```bash
python examples/31-multi-agent-debate/main.py
```

Two LLM agents argue opposing sides of a topic — Solver A argues for specialization, Solver B for generalization — exchanging critiques for `MAX_ROUNDS` rounds before a judge LLM selects the stronger position.

---

### Graph

```
START
  |
solve_a   ← opens with SPECIALIZATION argument (or refines using B's critique)
  |
solve_b   ← opens with GENERALIZATION argument (or refines using A's critique)
  |
debate    ← each agent critiques the other's position; round++
  |
  +-- round < MAX_ROUNDS ──► solve_a  (critique-and-revise loop)
  |
  +-- round >= MAX_ROUNDS ─► judge
  |
judge     ← reads both final positions, explains reasoning, emits WINNER
  |
END
```

Based on Du et al. 2023 — *Improving Factuality and Reasoning in Language Models through Multiagent Debate*.
