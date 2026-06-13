# 30-agentic-rag

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none — knowledge base is hardcoded inline

```bash
python examples/30-agentic-rag/main.py
```

Retrieval as one tool in a full ReAct loop: the agent decides per-turn whether to call `vectorstore_search`, `web_search`, or `calculator`.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/30-agentic-rag/agentic_rag_workbook.ipynb)

---

### Graph

```
START
  ↓
agent   ← ReAct loop: reason → call tool → observe
  ↓
  ├─ tool: vectorstore_search  ← internal Chroma knowledge base
  ├─ tool: web_search          ← DuckDuckGo live search
  ├─ tool: calculator          ← Python eval for arithmetic
  ↓
END
```
