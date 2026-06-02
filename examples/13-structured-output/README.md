# 13-structured-output

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none
**Colab:** ✅ fully self-contained; uses DuckDuckGo (no API key required)

Search the web for any subject and extract a validated Pydantic profile using `with_structured_output()`.
Demonstrates the search-then-extract two-node pattern: raw retrieval separated from structured generation.

```bash
python main.py "Anthropic"
python main.py "Geoffrey Hinton"
```
