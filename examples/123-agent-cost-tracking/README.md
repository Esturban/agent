# 123 — Agent Cost Tracking

Per-node token cost accounting, budget enforcement, and cost reporting in a 3-node LangGraph agent using tiktoken.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/123-agent-cost-tracking/agent_cost_tracking_workbook.ipynb)

## What it does

- `count_tokens()` via tiktoken — exact token counts before/after each LLM call
- `CostTracker` class accumulates per-node usage across the graph
- 3-node LangGraph: planner → executor → summarizer
- Routes to `budget_exceeded` node if cumulative cost > max_budget_usd
- Emits cost report: total, per-node breakdown, most expensive node

## How to run

```bash
python examples/123-agent-cost-tracking/main.py
```

## Key insight

tiktoken counts tokens BEFORE the API call — you can enforce budget limits proactively.
CostTracker gives you per-node cost attribution for production cost governance.
