# 80-multi-agent-supervisor

## Prerequisites
**Keys:** `OPENAI_API_KEY`

```bash
python examples/80-multi-agent-supervisor/main.py
```

A supervisor node classifies each question into math, history, or science and routes it to the matching specialist agent, demonstrating conditional routing in a multi-agent LangGraph.

---

### Graph

```
supervisor (classifies question → math | history | science)
  ↓
math_agent | history_agent | science_agent (specialist answer)
  ↓
END
```
