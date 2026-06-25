---
teaching_ready: true
---
# 25-adaptive-rag

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none

```bash
python examples/25-adaptive-rag/main.py
```

Route each query to the cheapest strategy that correctly answers it: direct LLM, private vectorstore, or live web search.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/25-adaptive-rag/adaptive_rag_workbook.ipynb)

---

### Graph

```
START
  ↓
classify (LLM routes query)
  ↓
  ├─ "simple"      ──► direct_answer      ──► END
  ├─ "vectorstore" ──► vectorstore_answer ──► END
  └─ "web"         ──► web_answer         ──► END
```
