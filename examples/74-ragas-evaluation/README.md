---
teaching_ready: true
---
# 74-ragas-evaluation

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Deps:** `pip install ragas datasets`

```bash
python examples/74-ragas-evaluation/main.py
```

Runs RAGAS `evaluate()` on a 5-row QA dataset, scoring a minimal ChromaDB RAG pipeline on `faithfulness` and `answer_relevancy`, and prints per-question scores with mean totals.

---

### Graph

```
build_rag_chain (ChromaDB + OpenAI retriever)
  ↓
run_evaluation (RAGAS faithfulness + answer_relevancy)
  ↓
END (prints score table)
```
