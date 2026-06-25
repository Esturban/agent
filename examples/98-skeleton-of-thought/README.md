---
teaching_ready: true
---
# 98 · Skeleton-of-Thought

Implements the Skeleton-of-Thought (SoT) pattern for parallel long-form generation. One LLM call produces a numbered outline; each point is then expanded concurrently via `Send()` fan-out — wall-clock time equals the skeleton call plus one expand call, not N. An `idx` field tags each expansion so `concatenate` can sort them back into the correct order after parallel arrival. Three-node graph: `make_skeleton → expand (×N parallel) → concatenate`. Reference: Ning et al. 2023 (arxiv.org/abs/2307.15337).

```bash
cd examples/98-skeleton-of-thought
python main.py
```

Requires: `OPENAI_API_KEY` in `.env`.
