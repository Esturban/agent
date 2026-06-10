# 13-structured-output

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/13-structured-output/structured_output_workbook.ipynb)

Search the web for any subject and extract a validated Pydantic profile using `with_structured_output()`. Demonstrates the search-then-extract two-node pattern: raw web retrieval separated from structured generation.

**Keys:** `OPENAI_API_KEY` · DuckDuckGo (no extra key required)

```bash
python examples/13-structured-output/main.py "Anthropic"
python examples/13-structured-output/main.py "Geoffrey Hinton"
```
