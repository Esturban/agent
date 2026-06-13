# 75-fastapi-sse-streaming

FastAPI server that wraps a LangGraph agent and streams token-by-token output to any HTTP client via Server-Sent Events. Uses `graph.astream_events()` piped through a `StreamingResponse` generator.

## How to run

```bash
python main.py
# or
uvicorn main:app --reload

# Test with curl:
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is retrieval-augmented generation?"}' \
  --no-buffer
```
