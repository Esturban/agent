# 75-fastapi-sse-streaming

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Deps:** `pip install fastapi uvicorn`

```bash
python examples/75-fastapi-sse-streaming/main.py
```

FastAPI server that wraps a single-node LangGraph agent and streams token-by-token output to HTTP clients via Server-Sent Events using `graph.astream_events()` piped through a `StreamingResponse`.

---

### Graph

```
answer (async LLM call with streaming=True)
  ↓
END
```
