# 91 · Analogical Reasoning

Asks the LLM to recall 3 analogous solved problems before tackling the target problem — no human-curated few-shot examples needed. Self-generated exemplars prime the right reasoning schema. Two-node graph: `generate_analogies → solve`. Reference: Webb et al. 2023 (nature.com/articles/s41562-023-01659-w).

```bash
cd examples/91-analogical-reasoning
python main.py
```

Requires: `OPENAI_API_KEY` in `.env`.
