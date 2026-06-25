---
teaching_ready: true
---
# 122 — Eval CI Pipeline

Wire LLM evaluation metrics as pytest tests that automatically fail the CI build when answer quality regresses.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/122-eval-ci-pipeline/eval_ci_pipeline_workbook.ipynb)

## What it does

- Golden dataset: 10 Q&A pairs about Python/LLM topics
- Good pipeline: answers using provided context (passes eval)
- Degraded pipeline: ignores context, returns "I don't know" (fails eval)
- Shows how to wire DeepEval metrics as pytest for automated CI

## How to run

```bash
python examples/122-eval-ci-pipeline/main.py

# With DeepEval (requires DEEPEVAL_API_KEY)
pip install deepeval
pytest tests/test_pipeline_eval.py
```

## Key insight

When you commit a change that degrades answer quality, pytest fails automatically.
No human review needed — the golden dataset catches regressions before they ship.
