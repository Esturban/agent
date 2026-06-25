---
teaching_ready: true
---
# 134 — DeerFlow Embedded Client

Drive a running DeerFlow service from plain Python: upload a file into a thread workspace, stream a plan-mode run watching SSE events live, then make a blocking chat call — all through a thin `DeerFlowClient` HTTP wrapper.

## How to run

```bash
# 1. Start DeerFlow (see runtime/README.md)
# 2. Set DEERFLOW_BASE_URL if not on localhost:8000
python main.py
```

## What it demonstrates

- `DeerFlowClient`: upload / stream / chat over DeerFlow's FastAPI HTTP API
- SSE event types: `message_chunk`, `tool_call`, `tool_result`, `end`
- `plan_mode=True` surfaces the planning step as distinct events
- Contrast table: LangGraph vs ADK vs Agno vs DeerFlow — what each runtime owns
