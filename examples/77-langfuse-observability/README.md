# 77-langfuse-observability

Demonstrates callback-based observability: a SimpleTraceHandler (mirrors LangfuseCallbackHandler) captures LLM events across a 2-node LangGraph.

```
task --> ask_question --> format_answer --> [traced answer]
```

```bash
python examples/77-langfuse-observability/main.py
```
