# 23-crewai-notebook

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none — all tasks and knowledge base are hardcoded inline
**Colab:** fully self-contained; notebook installs its own dependencies

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/23-crewai-notebook/crewai_workbook.ipynb)

```bash
jupyter notebook examples/23-crewai-notebook/crewai_workbook.ipynb
```

A deep-dive workbook into **CrewAI's role-based multi-agent model**. While LangGraph asks you to wire an explicit state machine, CrewAI asks you to describe a team: agents have roles and backstories, tasks have expected outputs and context dependencies, and a `Crew` orchestrates everything. Covers `Agent`, `Task`, `Crew`, `Process.sequential`, `Process.hierarchical`, and custom `@tool` definitions — with explicit comparisons to the LangGraph supervisor pattern from example 19.

**Companion to** [15-crewai-research-crew](../15-crewai-research-crew/) which shows a complete production pipeline.

---

### Framework contrast

```
LangGraph (example 19)           CrewAI (this example)
────────────────────             ─────────────────────
StateGraph + nodes/edges         Crew + agents/tasks
You define the routing           Manager LLM routes (hierarchical)
Explicit control flow            Declarative team structure
```
