# 77-langfuse-observability

## Prerequisites
**Keys:** `OPENAI_API_KEY`

```bash
python examples/77-langfuse-observability/main.py
```

Demonstrates callback-based observability by attaching a `SimpleTraceHandler` (mirroring the Langfuse callback interface) to a 2-node LangGraph, capturing LLM start/end events with trace IDs for each run.

---

### Graph

```
ask_question (LLM call with trace handler)
  ↓
format_answer (prepends trace ID to response)
  ↓
END
```
