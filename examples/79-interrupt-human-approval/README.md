---
teaching_ready: true
---
# 79-interrupt-human-approval

## Prerequisites
**Keys:** `OPENAI_API_KEY`

```bash
python examples/79-interrupt-human-approval/main.py
```

Demonstrates LangGraph `interrupt()` by pausing a graph mid-execution at an approval gate; auto-simulates human decisions based on risk level (low auto-approves, high auto-rejects).

---

### Graph

```
propose_action (stage the action and risk level)
  ↓
await_approval (interrupt → human decision → approve or reject)
  ↓
END
```
