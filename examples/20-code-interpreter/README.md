---
teaching_ready: true
---
# 20-code-interpreter

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none — tasks are hardcoded inline
**Colab:** not applicable — requires subprocess execution unavailable in Colab sandbox

```bash
python examples/20-code-interpreter/main.py
```

Implements a **code interpreter agent** in LangGraph. The agent receives a natural language coding task, writes Python code via an LLM, executes it in a `subprocess` sandbox with a 10-second timeout, and loops back to fix errors until the code runs successfully or `MAX_ITERATIONS` (default: 3) is reached.

---

### Graph

```
START
  |
write_code     <- LLM writes Python for the task (or fixes previous error)
  |
run_code       <- subprocess.run with 10s timeout, captures stdout/stderr
  |
  +-- success or max iterations ────► END
  |
  +-- error, iterations < MAX ──────► write_code  (fix loop)
```
