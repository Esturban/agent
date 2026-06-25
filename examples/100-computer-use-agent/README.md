---
teaching_ready: true
---
# 100 · Computer Use Agent

Uses Anthropic's computer-use beta to run a headless bash + file-editor action loop. The model requests tool calls, the agent executes them locally, feeds results back, and loops until `end_turn`.

## Run

```bash
cp .env.example .env   # add ANTHROPIC_API_KEY
python examples/100-computer-use-agent/main.py
```

## What you'll see

The agent writes `/tmp/fib.py`, runs it with bash, and returns the first 10 Fibonacci numbers — all driven by the model's tool-use decisions with no human steering.

## Key concepts

- `betas=["computer-use-2024-10-22"]` unlocks `bash_20241022` and `text_editor_20241022`
- Action loop: model → tool calls → execute → feed results → repeat
- No GUI / display required for bash + editor tools; add `computer_20241022` + Xvfb for mouse/keyboard
