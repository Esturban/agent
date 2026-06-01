# 15-crewai-research-crew

A two-agent CrewAI crew: a **Researcher** searches the web and gathers key facts, a **Writer** turns those facts into a structured report. Shows the `Crew`, `Agent`, and `Task` primitives as a direct contrast to LangGraph's `StateGraph` approach — same goal, different framework.

## Run as a script

```bash
python examples/15-crewai-research-crew/main.py
python examples/15-crewai-research-crew/main.py "quantum computing breakthroughs 2025"
```

## Run as a workbook

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/15-crewai-research-crew/crewai_workbook.ipynb)

```bash
jupyter notebook examples/15-crewai-research-crew/crewai_workbook.ipynb
```

The notebook is fully self-contained — no `src/` imports, Colab-compatible, includes exercises.
