# 34-openai-agents-sdk

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/34-openai-agents-sdk/openai_agents_workbook.ipynb)

Builds a triage agent that routes questions to specialist agents using OpenAI Agents SDK handoffs. A Researcher agent answers factual questions using a `@tool` function; a Writer agent rewrites findings into polished prose. Demonstrates SDK-native tracing and the handoff primitive as an alternative to LangGraph edges.

**Keys:** `OPENAI_API_KEY`

```bash
python examples/34-openai-agents-sdk/main.py
```

---

### Agent graph

```
user question
     |
  Triage agent        ← decides routing, no direct answer
     |
     +── factual question ──► Researcher  ← keyword_search(@tool) → answer
     |
     +── explain/write ─────► Writer      ← rewrite into paragraph
```

### Agents SDK vs LangGraph

| Concern | OpenAI Agents SDK | LangGraph |
|---------|-------------------|-----------|
| Routing | `handoff(agent)` on the source agent | `add_conditional_edges` on StateGraph |
| Tool definition | `@tool` decorator on any function | `@tool` (LangChain) or node function |
| State | Conversation history (implicit) | Typed `TypedDict` state (explicit) |
| Tracing | Built-in, zero config | Requires LangSmith or custom |
| Execution | `Runner.run_sync()` | `graph.compile().invoke()` |
