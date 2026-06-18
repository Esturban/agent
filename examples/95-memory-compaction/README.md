# 95 · Memory Compaction

Implements MemGPT-style 3-tier memory for agents that run thousands of turns without hitting context limits. Hot tier holds the last N verbatim turns; when it overflows, an LLM summarizes the lowest-importance turns into the warm tier; when warm overflows, oldest summary blocks archive to cold. Importance scoring uses recency decay + keyword boost so explicit user facts ("remember that…", "never…") stay verbatim longer. Four-node graph: `load_context → respond → save_turn → compact`. Reference: Packer et al. 2023 (arxiv.org/abs/2310.08560).

```bash
cd examples/95-memory-compaction
python main.py
```

Requires: `OPENAI_API_KEY` in `.env`.
