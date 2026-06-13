# 40-agent-observability

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none

```bash
python examples/40-agent-observability/main.py
```

Instrument a LangGraph agent with a custom `BaseCallbackHandler` to track per-call latency, token counts, and errors — no LangSmith account required. The callback plugs into any `invoke()` call via LangChain's `callbacks=` parameter.

---

### Graph

```
START
  |
llm    ← invoke with callbacks=[ObservabilityCallback]
  |
END
```

### Key Concepts

| Concept | Description |
|---------|-------------|
| `BaseCallbackHandler` | Hook into LLM lifecycle: `on_llm_start`, `on_llm_end`, `on_llm_error` |
| `run_id` | Unique ID per LLM call — correlates start/end events |
| `callbacks=[cb]` | Pass to `invoke()` config to activate tracing |
| `response.llm_output["token_usage"]` | Token counts from OpenAI response metadata |
