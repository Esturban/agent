# 40-agent-observability

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/40-agent-observability/observability_workbook.ipynb)

Instrument a LangGraph agent with a custom `BaseCallbackHandler` to track per-call latency, token counts, and errors — no LangSmith account required. The callback plugs into any `invoke()` call via LangChain's `callbacks=` parameter.

**Keys:** `OPENAI_API_KEY`

```bash
python examples/40-agent-observability/main.py
```

---

### Key Concepts

| Concept | Description |
|---------|-------------|
| `BaseCallbackHandler` | Hook into LLM lifecycle: `on_llm_start`, `on_llm_end`, `on_llm_error` |
| `run_id` | Unique ID per LLM call — correlates start/end events |
| `callbacks=[cb]` | Pass to `invoke()` config to activate tracing |
| `response.llm_output["token_usage"]` | Token counts from OpenAI response metadata |
