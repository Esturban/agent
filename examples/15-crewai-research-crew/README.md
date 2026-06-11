# 15-crewai-research-crew

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/15-crewai-research-crew/crewai_workbook.ipynb)

A two-agent CrewAI crew: a **Researcher** gathers web facts, a **Writer** turns them into a structured report. Direct contrast to LangGraph's `StateGraph` approach — same goal, different primitives (`Crew`, `Agent`, `Task` vs nodes and edges).

**Keys:** `OPENAI_API_KEY`
**Extra dep:** `crewai>=0.76.0` (already in `requirements.txt`)

```bash
# local notebook (recommended)
jupyter notebook examples/15-crewai-research-crew/crewai_workbook.ipynb

# or run the script
python examples/15-crewai-research-crew/main.py
python examples/15-crewai-research-crew/main.py "quantum computing breakthroughs 2025"
```
