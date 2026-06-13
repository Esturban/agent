# 73-langsmith-tracing

Decorates LangGraph nodes with `@traceable` and enables LangSmith tracing via env vars so every agent run is visible in the LangSmith UI with inputs, outputs, latency, and token counts.

## How to run

```bash
export LANGCHAIN_API_KEY=<your-key>
export LANGCHAIN_TRACING_V2=true
python main.py
```
