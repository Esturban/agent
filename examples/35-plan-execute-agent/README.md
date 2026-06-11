# 35-plan-execute-agent

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/35-plan-execute-agent/plan_execute_workbook.ipynb)

Separates planning from execution: a planner node emits a typed `Plan` (list of steps) via `with_structured_output`, an executor loops through each step passing prior results forward, and a synthesizer combines all outputs into a final answer. Teaches DAG-style task decomposition as an alternative to monolithic ReAct loops.

**Keys:** `OPENAI_API_KEY`

```bash
python examples/35-plan-execute-agent/main.py
```

---

### Graph

```
START
  |
planner          ← with_structured_output → Plan(steps=[...])
  |
executor  ◄──┐  ← runs steps[0], appends result, pops step
  |          │
  remaining? ┘  (loop until steps exhausted)
  |
synthesizer      ← combines all step results
  |
END
```

### Plan-Execute vs ReAct

| Concern | Plan-Execute | ReAct |
|---------|-------------|-------|
| Planning | Upfront, committed | Interleaved with execution |
| Adaptability | Low (plan is fixed) | High (replans on observation) |
| Token spend | Lower (no re-planning) | Higher (observe→think→act loop) |
| Best for | Structured, predictable tasks | Open-ended, exploratory tasks |
