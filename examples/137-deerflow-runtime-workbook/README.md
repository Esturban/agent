---
teaching_ready: true
---
# 137 — DeerFlow Runtime Workbook

Notebook-as-operator-console: connect to a running DeerFlow instance, upload a markdown corpus, stream an agent run with live event rendering, and inspect the output — all from Jupyter cells.

## How to run

```bash
# 1. Start DeerFlow: run `make dev` or `make docker-start` in the deer-flow repo
# 2. Set OPENAI_API_KEY in your .env
# 3. Open the notebook
jupyter notebook deerflow_runtime_workbook.ipynb
```

## What it demonstrates

- **Fail-fast setup**: cell 2 raises immediately if DeerFlow is not reachable — no silent failures
- **File upload**: uploads a 3-file markdown corpus to a DeerFlow thread via `/api/files/upload`
- **Live streaming**: iterates SSE events (`message_chunk`, `tool_call`, `end`) and prints chunks as they arrive
- **Gateway pattern**: no SDK dependency — just `httpx`; contrast with the embedded client (134) and custom skill (135)
- Swap `DEERFLOW_BASE_URL` to point at a remote server to use this as a production monitoring console
