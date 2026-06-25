---
teaching_ready: true
---
# 96 · Extended Thinking

Calls `claude-3-7-sonnet-20250219` with `thinking={'type':'enabled','budget_tokens':8000}` to give the model a private chain-of-thought scratchpad. The response contains two `ContentBlock`s: a `ThinkingBlock` (private, never returned to users) and a `TextBlock` (the final answer). Runs three puzzles — modular math, a wordplay trap, and a Cognitive Reflection Test item — with and without thinking to show where the scratchpad changes the answer. Framework-agnostic: uses the `anthropic` SDK directly, not LangGraph.

```bash
pip install anthropic
cd examples/96-extended-thinking
python main.py
```

Requires: `ANTHROPIC_API_KEY` in `.env` (console.anthropic.com).
