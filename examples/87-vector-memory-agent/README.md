# 87-vector-memory-agent

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Deps:** `chromadb` (included in requirements.txt)

```bash
python examples/87-vector-memory-agent/main.py
```

Vector memory — embed conversation turns into ChromaDB; at query time, retrieve only the k most semantically relevant turns instead of all history. Contrast with example 82 (Redis list = full history, O(N)); Chroma = relevant history, O(k). Per-user isolation via metadata `where={"user_id": ...}`.

---

### Flow

```
Seed turns → store_turn() → ChromaDB embeddings
  ↓
START → retrieve (top-3 semantic) → respond (conditioned on memories) → save turn → END
```

### Key concepts
- `text-embedding-3-small` for turn embeddings
- `collection.query(query_embeddings, n_results, where)` — semantic top-k with filter
- `collection.add(ids, embeddings, documents, metadatas)` — store with user_id tag
- Why vector > full history: context cost stays constant as memory grows
