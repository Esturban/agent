# 2-multi-tool-rag

RAG backed by a cloud-hosted Qdrant vector store with a DuckDuckGo web-search fallback. Demonstrates using a persistent, cloud-hosted vector DB instead of an in-memory one, and wiring multiple tools into a single agent.

**Keys:** `OPENAI_API_KEY` · `QDRANT_URL` · `QDRANT_KEY` · `BRAVE_API_KEY`
**Files:** none

```bash
python examples/2-multi-tool-rag/main.py
```

---

### How it works

- `src/` — checksum and deduplication logic for safe upsert into Qdrant
- `main.py` — ReAct agent with two tools: vector retrieval and web search fallback