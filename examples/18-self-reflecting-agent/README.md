# 18-self-reflecting-agent

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/18-self-reflecting-agent/reflexion_workbook.ipynb)

Reflexion loop (Shinn et al. 2023): generate an answer, critique it with a structured confidence score (`low` / `medium` / `high`), revise until confident or until `MAX_ITERATIONS` (default: 3) is reached. No retrieval or external tools — pure generate → critique → revise in LangGraph.

**Keys:** `OPENAI_API_KEY`

```bash
# local notebook (recommended)
jupyter notebook examples/18-self-reflecting-agent/reflexion_workbook.ipynb

# or run the script
python examples/18-self-reflecting-agent/main.py
```

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
