# 11-hitl-approval

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/11-hitl-approval/hitl_workbook.ipynb)

Human-in-the-loop approval using LangGraph's `interrupt()` primitive. The agent drafts a destructive action, pauses at an `__interrupt__` event, prompts the user for yes/no approval via CLI, then resumes from the saved checkpoint with `Command(resume=...)`.

**Keys:** `OPENAI_API_KEY`

```bash
python examples/11-hitl-approval/main.py
```

---

### How interrupt differs from all prior examples

Every earlier example runs `.stream()` all the way to `END`. Here:
1. First `.stream()` stops at `__interrupt__` — the graph is suspended mid-run
2. User approves or denies via CLI
3. Second `.stream(Command(resume=...))` resumes from the checkpoint
