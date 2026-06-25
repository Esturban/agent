---
teaching_ready: true
---
# 120 — Long-Context Agent

Compare full-document reasoning vs. chunked RAG on a 3,000-word synthetic report across 5 multi-hop questions.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/120-long-context-agent/long_context_agent_workbook.ipynb)

## What it does

- Loads a 3,000-word synthetic AI systems report
- Answers 5 multi-hop questions using: (1) full document in context, (2) keyword-overlap chunked RAG
- Scores both approaches and compares faithfulness and latency

## How to run

```bash
python examples/120-long-context-agent/main.py
```

## Key insight

Full-context: higher faithfulness (especially for multi-hop), higher latency and cost.
Chunked RAG: faster and cheaper, but 20-25% accuracy gap on multi-hop questions.
