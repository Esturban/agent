---
teaching_ready: true
---
# 97 · Best-of-N Sampling

Samples `N=4` independent chain-of-thought solutions at `temperature=0.8` using the `Send()` fan-out pattern, then scores each chain with an LLM-as-judge acting as a process reward model (PRM) — judging step clarity, logical rigor, and correctness rather than just the final answer. The highest-scoring chain wins. Demonstrates inference-time scaling: more compute at generation → better answer quality with no fine-tuning. Reference: Cobbe et al. 2021 (arxiv.org/abs/2110.14168).

```bash
cd examples/97-best-of-n-sampling
python main.py
```

Requires: `OPENAI_API_KEY` in `.env`.
