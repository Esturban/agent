---
teaching_ready: true
---
# 29-llm-judge-harness

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Colab:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/29-llm-judge-harness/llm_judge_workbook.ipynb)

Open `llm_judge_workbook.ipynb` in Colab or Jupyter. LLM-as-judge evaluation harness that scores RAG answers on Relevance, Faithfulness, and Completeness using a structured rubric — no labelled data required.

---

### Pattern (notebook)

```
build RAG pipeline → run test set → LLM judge scores each answer → aggregate metrics → exercises
```
