# 73-langsmith-tracing

## Prerequisites
**Keys:** `OPENAI_API_KEY`, `LANGCHAIN_API_KEY`, `LANGCHAIN_TRACING_V2=true`

```bash
python examples/73-langsmith-tracing/main.py
```

Decorates a LangGraph node with `@traceable` and enables LangSmith tracing so every agent run is visible in the LangSmith UI with inputs, outputs, latency, and token counts.

---

### Graph

```
answer (traceable LLM call)
  ↓
END
```
