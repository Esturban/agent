---
teaching_ready: true
---
# 28-parallel-subgraph

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/28-parallel-subgraph/parallel_subgraph_workbook.ipynb)

LangGraph Send API map-reduce pattern: a `distribute` node fans out one `Send` per document, spawning N parallel `summarize` workers. Each worker writes its result into an `Annotated[list, operator.add]` field which LangGraph merges automatically. After all workers complete, a single `aggregate` node synthesizes the results.

**Keys:** `OPENAI_API_KEY`

```bash
python examples/28-parallel-subgraph/main.py
```

---

### Graph

```
START
  │
distribute        ← returns [Send("summarize", {doc: d}) for d in documents]
  │
  ├─ summarize(doc=documents[0])  ─┐
  ├─ summarize(doc=documents[1])  ─┤  (run in parallel)
  ├─ summarize(doc=documents[2])  ─┤
  └─ summarize(doc=documents[3])  ─┘
                                   │  Annotated[list, operator.add] merges all
                                aggregate
                                   │
                                  END
```
