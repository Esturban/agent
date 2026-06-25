---
teaching_ready: true
---
# 1-basic-local-rag

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none — documents are fetched from the web at runtime

```bash
python examples/1-basic-local-rag/main.py
```

Minimal RAG: fetch web documents at runtime, split and embed into a local ChromaDB, answer questions via a single-node LangGraph.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/1-basic-local-rag/basic_local_rag_workbook.ipynb)

---

### Graph

```
START
  ↓
retrieve   ← fetch web docs, split, embed into ChromaDB, top-k lookup
  ↓
generate   ← LLM answers from retrieved context
  ↓
END
```
