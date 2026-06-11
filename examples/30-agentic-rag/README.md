# 30-agentic-rag

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/30-agentic-rag/agentic_rag_workbook.ipynb)

Retrieval as one tool in a full ReAct loop. Unlike fixed-pipeline RAG where retrieval always runs first, the agent decides per-turn which tool to call: `vectorstore_search` (internal Chroma KB), `web_search` (DuckDuckGo), or `calculator` (Python eval). Can skip retrieval entirely for math, chain multiple tool calls for complex questions.

**Keys:** `OPENAI_API_KEY`

```bash
python examples/30-agentic-rag/main.py
```
