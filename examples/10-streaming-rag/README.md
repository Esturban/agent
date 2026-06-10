# 10-streaming-rag

RAG pipeline with `.stream(stream_mode="updates")` — prints each node's output to the terminal as it runs, so you can see `retrieve → fallback → generate` in real time. ChromaDB in-memory with hardcoded documents; DuckDuckGo fires as a fallback when local retrieval is sparse.

**Keys:** `OPENAI_API_KEY`
**Colab:** ✅ fully self-contained

```bash
python examples/10-streaming-rag/main.py
```
