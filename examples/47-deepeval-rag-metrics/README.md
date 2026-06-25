---
teaching_ready: true
---
# 47-deepeval-rag-metrics

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none

```bash
pip install deepeval
python examples/47-deepeval-rag-metrics/main.py
```

DeepEval RAG metrics deep-dive: Faithfulness, AnswerRelevancy, ContextualPrecision, ContextualRecall, and ContextualRelevancy. Build a ChromaDB RAG pipeline, run `deepeval.evaluate()` on a golden dataset, inject deliberate failures, and watch scores respond.

---

### Graph

```
START
  |
retrieve   ← Chroma similarity_search, k=3
  |
generate   ← ChatOpenAI with retrieved context
  |
END        (deepeval.evaluate() runs on the output)
```

### The 5 RAG Metrics

| Metric | Formula | What it catches |
|--------|---------|-----------------|
| Faithfulness | supported_claims / total_claims | Hallucinations not in context |
| AnswerRelevancy | relevant_sentences / total_sentences | Off-topic or padded answers |
| ContextualPrecision | weighted_precision@k | Irrelevant chunks ranked high |
| ContextualRecall | context_covered / expected_output | Missing evidence in retrieval |
| ContextualRelevancy | relevant_chunks / total_chunks | Noisy retrieval |
