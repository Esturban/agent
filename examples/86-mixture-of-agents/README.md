---
teaching_ready: true
---
# 86-mixture-of-agents

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Deps:** none (pure LangGraph)

```bash
python examples/86-mixture-of-agents/main.py
```

Mixture of Agents (Wang et al. 2024) — fan out a question to 3 parallel proposers via `Send()`, each answering from a different persona. An aggregator LLM synthesises all proposals into one final answer. `Annotated[list[str], operator.add]` lets parallel branches merge results without overwriting.

---

### Flow

```
START → dispatch() → Send("proposer", {persona=pragmatist})
                   → Send("proposer", {persona=theorist})
                   → Send("proposer", {persona=educator})
  All proposers run in parallel
  ↓ aggregate() → final_answer → END
```

### Key concepts
- `Send("node", state)` — fan-out: spawn parallel copies of a node
- `Annotated[list[str], operator.add]` — reducer that appends instead of overwrites
- `add_conditional_edges(START, dispatch, ["proposer"])` — dynamic routing from START
- Temperature 0.7 on proposers, 0 on aggregator — diversity then determinism
