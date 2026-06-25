---
teaching_ready: true
---
# 17-corrective-rag

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/17-corrective-rag/corrective_rag_workbook.ipynb)

Corrective RAG (CRAG, Yan et al. 2024): after retrieval, an LLM grader scores each document for relevance. If any score "no", the query is rewritten and the pipeline falls back to DuckDuckGo web search before generating. Five LangGraph nodes: `retrieve → grade_documents → [transform_query → web_search →] generate`.

**Keys:** `OPENAI_API_KEY`

```bash
# local notebook (recommended)
jupyter notebook examples/17-corrective-rag/corrective_rag_workbook.ipynb

# or run the script
python examples/17-corrective-rag/main.py
```

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
