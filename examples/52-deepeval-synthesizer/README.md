# 52-deepeval-synthesizer

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/52-deepeval-synthesizer/synthesizer_workbook.ipynb)

DeepEval Synthesizer: auto-generate golden test datasets from documents using SIMPLE, REASONING, MULTI_HOP, and COMPARATIVE evolution strategies. Run `evaluate()`, save the dataset, re-run after changing the pipeline, and compare score deltas to detect regressions.

**Keys:** `OPENAI_API_KEY`

```bash
pip install deepeval
python examples/52-deepeval-synthesizer/main.py
```

---

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
