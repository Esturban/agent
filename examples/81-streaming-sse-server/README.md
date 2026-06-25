---
teaching_ready: true
---
# 81-streaming-sse-server

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Deps:** `pip install fastapi uvicorn`

```bash
python examples/81-streaming-sse-server/main.py
```

FastAPI endpoint that streams a 2-node LangGraph's token-by-token output as Server-Sent Events, demonstrating think-then-answer reasoning delivered over SSE.

---

### Graph

```
think_node (brief reasoning pass)
  ↓
answer_node (final concise answer)
  ↓
END
```
