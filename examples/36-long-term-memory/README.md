# 36-long-term-memory

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/36-long-term-memory/long_term_memory_workbook.ipynb)

Persists facts about a user across conversation threads using LangGraph's `InMemoryStore`. Each run retrieves relevant memories via semantic search, responds with that context, then extracts and stores new facts — enabling personalized behavior that improves across sessions.

**Keys:** `OPENAI_API_KEY`

```bash
python examples/36-long-term-memory/main.py
```

---

### Graph

```
START
  |
retrieve    ← store.search(namespace, query, limit=5)
  |
respond     ← SystemMessage with retrieved memories injected
  |
store       ← extract facts → store.put(namespace, key, {"fact": ...})
  |
END
```

### Key Concepts

| Concept | Description |
|---------|-------------|
| `InMemoryStore` | Cross-thread key-value store; survives thread boundaries |
| `store.put(namespace, key, value)` | Write: `(("memories", user_id), "key", {"fact": "..."})` |
| `store.search(namespace, query)` | Semantic search over stored values |
| Namespace | `("memories", user_id)` — isolates memories per user |
| Cross-thread | Thread-1 stores facts; Thread-2 retrieves them automatically |
