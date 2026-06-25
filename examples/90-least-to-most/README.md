---
teaching_ready: true
---
# 90 · Least-to-Most Prompting

Decomposes a problem into ordered sub-questions (easiest → hardest), then solves each sequentially — passing all prior solutions as context to each next solve call. Uses a conditional loop in LangGraph (`solve_next → check_done → solve_next`). Reference: Zhou et al. 2022 (arxiv.org/abs/2205.10625).

```bash
cd examples/90-least-to-most
python main.py
```

Requires: `OPENAI_API_KEY` in `.env`.
