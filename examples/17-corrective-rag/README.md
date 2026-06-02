# 17-corrective-rag

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none — knowledge base is hardcoded inline
**Colab:** ✅ fully self-contained; notebook installs its own dependencies

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/17-corrective-rag/corrective_rag_workbook.ipynb)

```bash
python examples/17-corrective-rag/main.py
```

Implements **Corrective RAG (CRAG)** in LangGraph (Yan et al., 2024). After retrieval, an LLM grader scores each document for relevance. If any document scores "no", the pipeline rewrites the query and falls back to DuckDuckGo web search before generating. Covers five LangGraph nodes: `retrieve → grade_documents → [transform_query → web_search_node →] generate`.

---

### Graph

```
START
  │
retrieve          ← Chroma vectorstore, top-3 docs
  │
grade_documents   ← LLM scores each doc "yes"/"no"
  │
  ├─ all relevant ──────────────────────┐
  │                                     │
  └─ any irrelevant → transform_query   │
                          │             │
                    web_search_node     │
                          │             │
                        generate ←──────┘
                          │
                         END
```
