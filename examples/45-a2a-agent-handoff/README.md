---
teaching_ready: true
---
# 45-a2a-agent-handoff

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none

```bash
python examples/45-a2a-agent-handoff/main.py
```

Demonstrates Agent-to-Agent (A2A) handoff with a structured Pydantic schema. Planner Agent creates an `AgentTask`, passes it to Executor Agent, then synthesizes the final result — agents communicate via typed contracts, not raw strings.

---

### Graph

```
START → planner (A: creates AgentTask) → executor (B: runs task) → synthesizer (A: final answer) → END
```

### A2A Handoff Contract

```python
class AgentTask(BaseModel):
    task_id: str        # unique slug
    task_type: str      # research | analysis | synthesis
    instruction: str    # clear directive for executor
    context: str        # background to help executor
    expected_output: str # what executor should return
```

### Why typed handoffs?

| Approach | Coupling | Debuggability | Schema enforcement |
|----------|----------|---------------|--------------------|
| Raw string | Loose, fragile | Hard | None |
| Dict | Medium | OK | None |
| **Pydantic model** | **Explicit contract** | **Serializable** | **Validated** |
