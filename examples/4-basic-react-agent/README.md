---
teaching_ready: true
---
# 4-basic-react-agent

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** `data/product/Laptop pricing.csv`, `data/product/Laptop product descriptions.pdf`

```bash
python examples/4-basic-react-agent/main.py
```

ReAct agent with two tools: semantic search over a CSV pricing table and PDF retrieval from a product spec document. Maintains full conversation history across turns with `MemorySaver`.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/4-basic-react-agent/basic_react_agent_workbook.ipynb)

---

### Graph

```
START
  ↓
agent   ← ReAct loop: reason → call tool → observe
  ↓
  ├─ tool: csv_search   ← semantic search over pricing CSV
  ├─ tool: pdf_search   ← retrieval from product spec PDF
  ↓
END
```