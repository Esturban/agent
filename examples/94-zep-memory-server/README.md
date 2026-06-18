# 94 · Zep Memory Server

Integrates Zep Cloud for production agent memory. Seeds a past conversation, then runs follow-up queries — Zep auto-summarizes history and injects a compressed `context` string into the system prompt. Contrasts with DIY Redis (example 82): same three-node graph structure, managed compaction instead of manual. Requires: `pip install zep-cloud`.

```bash
pip install zep-cloud
cd examples/94-zep-memory-server
python main.py
```

Requires: `OPENAI_API_KEY` and `ZEP_API_KEY` in `.env` (free tier at getzep.com).
