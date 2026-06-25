---
teaching_ready: true
---
# 15-crewai-research-crew

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none

```bash
python examples/15-crewai-research-crew/main.py
```

A two-agent CrewAI crew: a **Researcher** gathers web facts, a **Writer** turns them into a structured report. Direct contrast to LangGraph's `StateGraph` approach.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/15-crewai-research-crew/crewai_workbook.ipynb)

---

### Graph

```
START
  ↓
researcher  ← Agent: web search, extracts 5-7 key facts with source notes
  ↓
writer      ← Agent: writes a 200-word structured report
  ↓
END
```
