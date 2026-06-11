# 38-langgraph-command-pattern

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/38-langgraph-command-pattern/command_pattern_workbook.ipynb)

Demonstrates LangGraph's `Command` primitive for edgeless dynamic routing. A router node classifies the task and returns `Command(goto="code"|"explain"|"math"|"creative", update={...})` — no `add_conditional_edges` needed, routing is entirely in code.

**Keys:** `OPENAI_API_KEY`

```bash
python examples/38-langgraph-command-pattern/main.py
```

---

### Graph

```
START
  |
router      ← classifies task, returns Command(goto=route)
  |
  ├─ code ──────────────────────────────────────────┐
  ├─ explain ────────────────────────────────────────┤→ END
  ├─ math ───────────────────────────────────────────┤
  └─ creative ───────────────────────────────────────┘
```

### Command vs conditional_edges

| Feature | `Command(goto=...)` | `add_conditional_edges` |
|---------|---------------------|------------------------|
| Routing logic location | Inside node function | Separate routing function |
| State updates | Inline with routing | Separate update step |
| Dynamic destinations | Yes — any valid node | Requires mapping dict |
| Readability | Logic co-located | Logic separated |

```python
# Command: routing + update in one return
return Command(goto="code", update={"route": "code"})

# conditional_edges: routing function separate
def route(state) -> str:
    return state["route"]
graph.add_conditional_edges("router", route, {"code": "code", ...})
```
