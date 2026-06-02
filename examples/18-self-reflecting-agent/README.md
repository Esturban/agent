# 18-self-reflecting-agent

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none — all questions are hardcoded inline
**Colab:** ✅ fully self-contained; the notebook installs its own dependencies on Colab

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/18-self-reflecting-agent/reflexion_workbook.ipynb)

```bash
python examples/18-self-reflecting-agent/main.py
```

Implements the **Reflexion** self-improvement loop (Shinn et al., 2023) in LangGraph. The agent generates an initial answer, uses `with_structured_output` to critique it and score confidence (`low` / `medium` / `high`), then revises in a loop until confident or until `MAX_ITERATIONS` (default: 3) is reached.

No retrieval, no external tools — pure generate → critique → revise loop over a LangGraph `StateGraph`.

---

### Graph

```
START
  |
generate       <- draft (first pass) or revise (subsequent passes)
  |
critique       <- LLM scores answer confidence + identifies gaps
  |
  +- high confidence ───────────────────► END
  |
  +- max iterations reached ────────────► END
  |
  +- low / medium ──────────────────────► generate  (loop)
```
