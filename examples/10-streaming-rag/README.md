# 10-streaming-rag

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none — documents are hardcoded inline

```bash
python examples/10-streaming-rag/main.py
```

RAG pipeline with `.stream(stream_mode="updates")` — prints each node's output to the terminal as it runs, so you can see `retrieve → fallback → generate` in real time.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/10-streaming-rag/streaming_rag_workbook.ipynb)

---

### Graph

```
START
  ↓
retrieve      ← ChromaDB in-memory, top-k docs from hardcoded corpus
  ↓
  ├─ sufficient ──────────────────────► generate → END
  └─ sparse    ──────────────────────► web_fallback (DuckDuckGo)
                                           ↓
                                        generate → END
```
