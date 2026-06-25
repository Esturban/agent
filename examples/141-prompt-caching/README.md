# 141 — Prompt Caching

Benchmarks Claude's prompt caching by sending the same large system prompt twice — once without cache, once with `cache_control` ephemeral blocks. Prints token savings and latency delta.

**Run:** `python main.py` — requires `ANTHROPIC_API_KEY` in `.env`
