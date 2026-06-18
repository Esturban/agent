# 85-agno-agent

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Deps:** `agno`

```bash
python examples/85-agno-agent/main.py
```

Agno (formerly Phidata) — minimal agent framework: `Agent(model, tools, instructions)`. Tool schemas are inferred from Python type hints and docstrings. `agent.run(task)` handles the tool-call loop. Contrast with LangGraph: ~5 lines vs ~30 lines for the same tool-using agent. Trade-off: less explicit control, faster to write.

---

### Flow

```
Agent(OpenAIChat("gpt-4o-mini"), tools=[search_knowledge, add_knowledge, list_topics])
  ↓ agent.run(task) — internal tool-call loop
  ↓ response.content → text answer
```

### Key concepts
- `Agent(model, tools, instructions)` — single-call agent definition
- Tool schemas auto-generated from function signatures + docstrings
- `response.content` — final text output
- `show_tool_calls=True` — prints tool invocations for teaching visibility
