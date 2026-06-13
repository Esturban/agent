# 39-checkpoint-resume

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none

```bash
python examples/39-checkpoint-resume/main.py
```

Demonstrates LangGraph's `SqliteSaver` checkpointer: persist full graph state to SQLite mid-run, resume from any `thread_id`, and inspect historical states. Shows how thread-based isolation lets multiple tasks run independently with full state recovery.

---

### Graph

```
START
  |
step  ◄──┐  ← executes STEP_PROMPTS[state.step], appends to outputs
  |      │
done? ───┘  (loop until step >= len(STEP_PROMPTS))
  |
END
```

### Key Concepts

| Concept | Description |
|---------|-------------|
| `SqliteSaver.from_conn_string(path)` | Creates checkpointer backed by SQLite file |
| `graph.compile(checkpointer=saver)` | Attaches saver; every node completion = checkpoint |
| `config = {"configurable": {"thread_id": "..."}}` | Scopes state to a named thread |
| `app.invoke(..., config=config)` | Run or resume a specific thread |
| `app.get_state(config)` | Read persisted state without re-running |
| `app.get_state_history(config)` | List all checkpoints for a thread |

### Checkpoint flow

```
invoke(state, config={thread_id: "t1"})
  step 1 → checkpoint written to SQLite
  step 2 → checkpoint written
  step 3 → checkpoint written (done=True)

invoke(state={}, config={thread_id: "t1"})  # resume
  → picks up from last checkpoint, no re-execution of done steps
```
