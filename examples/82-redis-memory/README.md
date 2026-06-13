# 82-redis-memory

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Deps:** Redis running locally — `docker run -p 6379:6379 redis:alpine`

```bash
python examples/82-redis-memory/main.py
```

LangGraph with Redis-backed persistent memory: each session loads prior conversation turns from a Redis list, answers with full context, then appends the new exchange — surviving process restarts.

---

### Graph

```
load_history (fetch prior turns from Redis list)
  ↓
respond (LLM call with full history as context)
  ↓
save_history (append user + assistant turn to Redis)
  ↓
END
```
