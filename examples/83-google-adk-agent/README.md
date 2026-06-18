# 83-google-adk-agent

## Prerequisites
**Keys:** `GOOGLE_API_KEY` (get one at aistudio.google.com)
**Deps:** `google-adk`, `google-genai`

```bash
python examples/83-google-adk-agent/main.py
```

Google ADK — declare an `LlmAgent` with plain-function tools; ADK manages the Gemini tool-call loop via an async `Runner`. Contrast: LangGraph requires an explicit `StateGraph`; ADK handles the graph internally. Tool schemas are auto-generated from Python docstrings.

---

### Flow

```
create_agent(LlmAgent)
  ↓
Runner.run_async() — ADK manages tool-call loop:
  LlmAgent → [tool calls if needed] → final response
  ↓
is_final_response() event → extract text
```

### Key concepts
- `LlmAgent(name, model, instruction, tools)` — declarative agent definition
- `Runner(agent, app_name, session_service)` — executes the agent loop
- `InMemorySessionService` — per-session conversation state
- `genai_types.Content` — message format for the Gemini API
