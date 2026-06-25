---
teaching_ready: true
---
# 13-structured-output

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none

```bash
python examples/13-structured-output/main.py "Anthropic"
```

Search the web for any subject and extract a validated Pydantic profile using `with_structured_output()`. Demonstrates the search-then-extract two-node pattern.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/13-structured-output/structured_output_workbook.ipynb)

---

### Graph

```
START
  ↓
search    ← DuckDuckGo web search for the subject
  ↓
extract   ← LLM extracts EntityProfile via with_structured_output()
  ↓
END
```
