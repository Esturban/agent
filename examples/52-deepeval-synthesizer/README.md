---
teaching_ready: true
---
# 52-deepeval-synthesizer

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none

```bash
pip install deepeval
python examples/52-deepeval-synthesizer/main.py
```

DeepEval Synthesizer: auto-generate golden test datasets from documents using SIMPLE, REASONING, MULTI_HOP, and COMPARATIVE evolution strategies. Run `evaluate()`, save the dataset, re-run after changing the pipeline, and compare score deltas to detect regressions.

---

### Graph

```
START
  |
retrieve   ← Chroma similarity_search, k=3 (or k=1 for degraded run)
  |
generate   ← ChatOpenAI with retrieved context
  |
END        (Synthesizer generates goldens → evaluate() → compare delta)
```

### Evolution strategies

| Strategy | What it generates | Tests |
|----------|------------------|-------|
| SIMPLE | Direct factual questions | Basic recall |
| REASONING | Multi-step logical questions | Inference |
| MULTI_HOP | Questions spanning multiple docs | Cross-doc linking |
| COMPARATIVE | "Compare X and Y" questions | Synthesis |

### The regression eval loop

```
generate goldens → evaluate (k=3) → degrade pipeline (k=1) → re-evaluate → compare delta
```
