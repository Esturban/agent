---
teaching_ready: true
---
# 142 — Semantic Caching

Embeds each query, checks cosine similarity against cached responses, and returns a cached answer when similarity exceeds the threshold (default 0.92). Near-duplicate queries hit the cache without calling the LLM.

**Run:** `python main.py` — requires `OPENAI_API_KEY` in `.env`
