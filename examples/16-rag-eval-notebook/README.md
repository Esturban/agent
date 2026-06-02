# 16-rag-eval-notebook

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none — knowledge base is hardcoded inline
**Extra dep:** `ragas>=0.1.0` (already in `requirements.txt`)
**Colab:** ✅ fully self-contained; the notebook installs its own dependencies on Colab

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/16-rag-eval-notebook/rag_eval_workbook.ipynb)

```bash
jupyter notebook examples/16-rag-eval-notebook/rag_eval_workbook.ipynb
```

A hands-on evaluation workbook using **RAGAS** to score a RAG pipeline across three metrics: **Faithfulness**, **Answer Relevance**, and **Context Recall**. Includes exercises that deliberately degrade the pipeline so you can see exactly how each metric reacts and what to fix.
