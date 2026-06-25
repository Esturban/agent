# 143 — Context Compression

Scores each sentence in a document against the user query, keeps only the top 40%, and sends the compressed context to the LLM. Demonstrates relevance-based context reduction to cut token costs without sacrificing answer quality.

**Run:** `python main.py` — requires `OPENAI_API_KEY` in `.env`
