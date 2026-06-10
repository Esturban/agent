# 19-multi-agent-notebook

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/19-multi-agent-notebook/multi_agent_workbook.ipynb)

Supervisor/Worker multi-agent pattern in LangGraph. A supervisor LLM uses `with_structured_output` to route tasks to specialist workers (researcher + writer), coordinating via shared `add_messages` state until the task is complete. Covers `add_messages` reducer, `create_react_agent` workers, `add_conditional_edges`, and streaming multi-agent execution.

**Keys:** `OPENAI_API_KEY`

```bash
# local notebook (recommended)
jupyter notebook examples/19-multi-agent-notebook/multi_agent_workbook.ipynb
```

---

### Graph

```
START
  |
supervisor  <-----------+
  |                     |
  +-- next=researcher --+--> researcher_agent --> supervisor
  |                     |
  +-- next=writer    ---+--> writer_agent    --> supervisor
  |
  +-- next=FINISH --------> END
```
