# 46-tree-of-thoughts

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/46-tree-of-thoughts/tree_of_thoughts_workbook.ipynb)

Implements Tree of Thoughts (ToT) with LangGraph's Send API: fan out N=3 independent thought branches in parallel, score each with a judge LLM (0-10), select the best, and synthesize the final answer. Demonstrates the Send API pattern for branch exploration + `Annotated[list, operator.add]` reducer accumulation.

**Keys:** `OPENAI_API_KEY`

```bash
python examples/46-tree-of-thoughts/main.py
```

---

### Graph

```
START
  │
  ├─ Send → score_branch (branch 0)  ─┐
  ├─ Send → score_branch (branch 1)  ─┤→ select_best → synthesize → END
  └─ Send → score_branch (branch 2)  ─┘
```

### Key Concepts

| Concept | Description |
|---------|-------------|
| `Send("node", state)` | Fan-out: spawn N independent node invocations |
| `Annotated[list[dict], operator.add]` | Reducer: accumulate branch results |
| `set_conditional_entry_point` | Entry point that returns `list[Send]` |
| Judge LLM (low temp) | Consistent 0-10 scoring separate from generator |
| `select_best` | Pure Python max() — no LLM needed |
