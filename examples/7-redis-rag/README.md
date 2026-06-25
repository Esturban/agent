---
teaching_ready: true
---
# 7-redis-rag

RAG backed by Redis vector store. A grader node scores each retrieved document for relevance — if any are irrelevant, the query is rewritten and retrieval runs again until the answer is satisfactory.

**Keys:** `OPENAI_API_KEY`
**Services:** Redis — `docker run -p 6379:6379 -d redis` or a free [Redis Cloud](https://redis.io/try-free/) instance
**Colab:** ❌ requires a running Redis server

```bash
python examples/7-redis-rag/main.py
```

---

### Graph

```
START
  |
retrieve      <- Redis vector store, top-k docs
  |
grade         <- LLM scores each doc "relevant" / "irrelevant"
  |
  +-- relevant ─────────────────────► generate → END
  |
  +-- irrelevant → rewrite_query → retrieve  (loop)
```