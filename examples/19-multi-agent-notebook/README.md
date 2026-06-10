# Multi-Agent Patterns with LangGraph

Supervisor/worker architecture: a central supervisor LLM routes tasks to specialist workers (researcher + writer), coordinating via shared `add_messages` state until the task is complete.

**Open in Colab:** `examples/19-multi-agent-notebook/multi_agent_workbook.ipynb`

**Run locally:** `jupyter notebook examples/19-multi-agent-notebook/multi_agent_workbook.ipynb`

**Covers:** supervisor/worker routing, `add_messages` reducer, `create_react_agent` workers, `add_conditional_edges`, streaming multi-agent execution
