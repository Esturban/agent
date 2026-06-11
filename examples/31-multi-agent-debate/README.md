# 31-multi-agent-debate

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/31-multi-agent-debate/multi_agent_debate_workbook.ipynb)

Two LLM agents argue opposing sides of a topic — Solver A argues for specialization, Solver B for generalization — exchanging critiques for `MAX_ROUNDS` rounds before a judge LLM selects the stronger position.

**Keys:** `OPENAI_API_KEY`

```bash
python examples/31-multi-agent-debate/main.py
```

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
