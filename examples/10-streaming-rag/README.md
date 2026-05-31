# 10-streaming-rag

RAG pipeline using `.stream(stream_mode="updates")` to surface each node's output as it runs.
ChromaDB ingests a small hardcoded document set; DuckDuckGo fires as a web fallback if local retrieval is sparse.

Run: `python examples/10-streaming-rag/main.py`
