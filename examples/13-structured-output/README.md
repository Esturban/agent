# 13-structured-output

Search the web for any subject and extract a validated Pydantic profile using `with_structured_output()`. Demonstrates the search-then-extract two-node pattern: raw web retrieval separated from structured generation.

**Keys:** `OPENAI_API_KEY`
**Colab:** ✅ fully self-contained; uses DuckDuckGo (no API key required)

```bash
python examples/13-structured-output/main.py "Anthropic"
python examples/13-structured-output/main.py "Geoffrey Hinton"
```
