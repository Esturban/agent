---
teaching_ready: true
---
# 37-rewoo-agent

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none

```bash
python examples/37-rewoo-agent/main.py
```

ReWOO (Reasoning WithOut Observation) emits all tool calls upfront as a structured plan, executes them in bulk with variable substitution, then solves using accumulated evidence — eliminating the interleaved observe-think-act loop of ReAct.

---

### Graph

```
START
  |
planner     ← LLM emits [{tool, args, output_var}, ...] as JSON
  |
executor    ← runs ALL steps, resolves $E1/$E2 variable refs
  |
solver      ← synthesizes evidence into final answer
  |
END
```

### ReWOO vs ReAct

| Concern | ReWOO | ReAct |
|---------|-------|-------|
| Planning | Upfront (committed plan) | Interleaved (think→act→observe) |
| Tool calls | Batch — all at once | Sequential — one per loop iteration |
| Adaptability | Low (no mid-plan replanning) | High (observes after each action) |
| Token spend | Lower (no repeated reasoning) | Higher (observe loop overhead) |
| Best for | Well-defined tasks with predictable tools | Open-ended exploration |

### Variable substitution

The executor resolves `$E1`, `$E2`, etc. in later steps:
```
Step 1: search("LangGraph") → $E1 = "LangGraph is..."
Step 2: summarize("$E1")   → args becomes "LangGraph is..."
```
