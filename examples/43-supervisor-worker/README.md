# 43-supervisor-worker

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none

```bash
python examples/43-supervisor-worker/main.py
```

A supervisor LLM uses `with_structured_output(WorkerRoute)` to classify each task and route it to the best specialist worker — researcher, summarizer, or analyst — each with a tailored system prompt.

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
