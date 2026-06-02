## 11 — Human-in-the-Loop Approval with interrupt()

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none
**Colab:** ⚠️ the script uses an interactive CLI prompt; run locally or adapt the approval step for a notebook cell

```bash
python examples/11-hitl-approval/main.py
```

Drafts a destructive action, pauses mid-graph via `interrupt()` for human yes/no approval, then resumes with `Command(resume=...)`. Demonstrates the key contrast with all prior examples: the first `.stream()` stops at an `__interrupt__` event rather than running to END, and a second `.stream()` continues from the saved checkpoint.

```bash
python main.py
```
