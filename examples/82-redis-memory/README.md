# 82-redis-memory

LangGraph with Redis for cross-session persistent memory. Each session loads prior conversation turns from Redis, answers with full context, then appends the new exchange back to Redis.

Requires Redis running locally: `docker run -p 6379:6379 redis:alpine`

```bash
python main.py
```
