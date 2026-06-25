---
teaching_ready: true
---
# 136 — DeerFlow Sandboxed SWE Agent

Upload a tiny Python package with a failing test into a DeerFlow thread and let the sandboxed SWE agent fix it.

## How to run

```bash
# 1. Start DeerFlow with sandbox enabled — see runtime/README.md (copy config.aio.yaml to conf/config.yaml)
# 2. Set OPENAI_API_KEY in your .env
DEERFLOW_BASE_URL=http://localhost:8000 python main.py
```

## What it demonstrates

- Two sandbox modes: `LocalSandboxProvider` (file tools, no shell) vs `AioSandboxProvider` (bash in container) — see `runtime/`
- `SWEAgent`: uploads `fixtures/buggy_repo/` files, streams a fix task, verifies the patch contains `return a + b`
- Security boundary: DeerFlow's thread-local workspace isolates file state per request; never expose the endpoint on an untrusted network
- Contrast with 134/135: 134 = generic chat client; 135 = custom research skill; 136 = coding task in an isolated sandbox workspace
