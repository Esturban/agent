---
teaching_ready: true
---
# 89 · Self-Consistency

Samples `N` independent chain-of-thought reasoning paths for the same question using `temperature=0.7`, then takes a majority vote over the extracted final answers. Demonstrates the `Send()` fan-out pattern with an `operator.add` reducer. Reference: Wang et al. 2022 (arxiv.org/abs/2203.11171).

```bash
cd examples/89-self-consistency
python main.py
```

Requires: `OPENAI_API_KEY` in `.env`.
