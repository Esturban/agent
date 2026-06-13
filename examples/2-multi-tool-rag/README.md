# 2-multi-tool-rag

## Prerequisites
**Keys:** `OPENAI_API_KEY`, `QDRANT_URL`, `QDRANT_KEY`, `BRAVE_API_KEY`
**Files:** none

```bash
python examples/2-multi-tool-rag/main.py
```

RAG backed by a cloud-hosted Qdrant vector store with a Brave web-search fallback. Demonstrates using a persistent, cloud-hosted vector DB instead of an in-memory one, and wiring multiple tools into a single ReAct agent.

---

### Graph

```
START
  ↓
agent   ← ReAct loop: reason → call tool → observe
  ↓
  ├─ tool: vector_search  ← Qdrant cloud retrieval
  ├─ tool: web_search     ← Brave API fallback
  ↓
END
```