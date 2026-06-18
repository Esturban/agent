# 103 · Tool Synthesis (LATM)

LLMs as Tool Makers (Cai et al. 2023): a dispatcher LLM picks an existing tool or requests synthesis; a tool-maker LLM generates Python code on demand; synthesized tools are cached and reused across subsequent calls.

## Run

```bash
cp .env.example .env   # add OPENAI_API_KEY
python examples/103-tool-synthesis-latm/main.py
```

## What you'll see

Tasks 1 and 3 trigger synthesis (new tools written and registered). Tasks 2 and 4 hit the same task type — the dispatcher reuses the cached tool with no code generation. Task 5 synthesizes a third tool. Registry grows from 0 → 1 → 2 → 3 tools across 5 tasks.

## Key concepts

- **Dispatcher LLM** selects from available tools or returns `synthesize`
- **Tool-maker LLM** generates Python code; `exec()` registers it in `_registry`
- **Caching amortizes cost** — synthesis happens once, reuse is free
- Uses zero-auth public APIs (`wttr.in`, `numbersapi.com`) as synthesis targets
- **Production note**: replace `exec()` with E2B sandboxing (example 92)
