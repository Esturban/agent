---
teaching_ready: true
---
# 6-multi-agent-graph

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** `data/product/Laptop pricing.csv`, `data/product/Laptop Orders.csv`, `data/product/Laptop product descriptions.pdf`

```bash
python examples/6-multi-agent-graph/main.py
```

Two specialist agents in a single LangGraph: **ProductQnA** answers product questions, **OrdersAgent** handles order lookup and quantity updates. A supervisor node routes messages between them based on intent.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/6-multi-agent-graph/multi_agent_graph_workbook.ipynb)

---

### Graph

```
START
  ↓
supervisor   ← routes message by intent
  ↓
  ├─ product question ──► product_qna_agent  ─► supervisor
  └─ order request    ──► orders_agent       ─► supervisor
  ↓
  └─ FINISH ──────────────────────────────────► END
```
