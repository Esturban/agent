# 62-async-langgraph

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Colab:** [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/esturban/agent/blob/main/examples/62-async-langgraph/async_langgraph_workbook.ipynb)

Open `async_langgraph_workbook.ipynb` in Colab or Jupyter. Demonstrates async LangGraph nodes, `ainvoke()`, `asyncio.gather()` for concurrent tool calls (3× speedup over sequential), and `astream_events()` for token streaming.

---

### Pattern (notebook)

```
sync baseline (time it)
  → async node + ainvoke()
    → asyncio.gather() inside node: 3 tools × 1s → ~1s total
      → astream_events(): token-level streaming
        → exercises: convert sync graph, add 4th tool
          → answer key
```
