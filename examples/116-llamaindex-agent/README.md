---
teaching_ready: true
---
# 116-llamaindex-agent

## Prerequisites
**Keys:** `OPENAI_API_KEY` in `.env`
**Deps:** `pip install llama-index llama-index-llms-openai`
**Colab:** see workbook

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/116-llamaindex-agent/llamaindex_agent_workbook.ipynb)

```bash
python examples/116-llamaindex-agent/main.py
```

LlamaIndex's ReActAgent wraps tool-use and the ReAct reasoning loop behind a single
`agent.chat()` call. This example indexes 3 document domains (science, history, technology),
exposes each as a `QueryEngineTool`, then runs multi-hop questions that require routing
across tools — demonstrating what LlamaIndex hides vs. what LangGraph makes explicit.

---

### Architecture

```
ReActAgent
  |
  +-- science_tool   (VectorStoreIndex over 3 science docs)
  +-- history_tool   (VectorStoreIndex over 3 history docs)
  +-- technology_tool (VectorStoreIndex over 3 tech docs)

agent.chat(question)
  -> ReAct loop: Thought -> Action -> Observation -> ...
  -> Final answer synthesized from tool outputs
```
