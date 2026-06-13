# 5-react-agent-lg

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** `data/product/EcoSprint_Specification_Document.pdf`

```bash
python examples/5-react-agent-lg/main.py
```

LangGraph ReAct agent with a two-node critique loop: a **Summarizer** drafts a PDF summary, a **Reviewer** grades it and suggests improvements, and the loop continues until approved.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/5-react-agent-lg/react_agent_lg_workbook.ipynb)

---

### Graph

```
START
  ↓
generate_summary   ← Summarizer drafts a PDF summary
  ↓
review_summary     ← Reviewer grades and suggests improvements
  ↓
  ├─ approved ──────────────────────► END
  └─ needs revision ────────────────► generate_summary  (loop)
```
