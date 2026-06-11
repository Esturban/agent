# 43-supervisor-worker

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/43-supervisor-worker/supervisor_worker_workbook.ipynb)

A supervisor LLM uses `with_structured_output(WorkerRoute)` to classify each task and route it to the best specialist worker — researcher, summarizer, or analyst — each with a tailored system prompt.

**Keys:** `OPENAI_API_KEY`

```bash
python examples/43-supervisor-worker/main.py
```

---

### Graph

```
START → supervisor (structured routing) → researcher ─┐
                                         summarizer ──┼→ END
                                         analyst   ───┘
```

### Supervisor vs Command pattern

| Feature | This example (structured output) | 38-langgraph-command-pattern |
|---------|----------------------------------|------------------------------|
| Routing | `with_structured_output(WorkerRoute)` | `Command(goto=route)` |
| Rationale | Explicit `rationale` field | Implicit in routing logic |
| Schema validation | Pydantic enforces valid worker name | No schema, string match |
