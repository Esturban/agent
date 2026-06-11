# 32-speculative-rag

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/32-speculative-rag/speculative_rag_workbook.ipynb)

Generates a draft answer first (without retrieval), extracts its factual claims, retrieves evidence per claim, and revises only the unsupported parts. Retrieval becomes a targeted fact-check layer rather than a mandatory first step.

**Keys:** `OPENAI_API_KEY`

```bash
python examples/32-speculative-rag/main.py
```

---

### Graph

```
START
  |
draft              ← LLM answers from training knowledge (no retrieval)
  |
extract_claims     ← parse draft into numbered checkable facts
  |
retrieve_and_grade ← retrieve top-k docs per claim, label SUPPORTED / CONTRADICTED / UNRELATED
  |
  +-- any unsupported ──► revise  ← rewrite only flagged claims using evidence
  |
  +-- all supported ────► END
```

### Why this is faster than standard RAG

Standard RAG always retrieves before answering — even for questions the model knows perfectly well. Speculative RAG retrieves only when the model's draft contains unsupported claims, saving retrieval latency for well-known facts.
