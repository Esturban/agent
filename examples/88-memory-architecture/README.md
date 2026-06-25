---
teaching_ready: true
---
# 88-memory-architecture

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Deps:** none (pure LangGraph)

```bash
python examples/88-memory-architecture/main.py
```

Three-tier agent memory (Tulving 1972 + MemGPT): episodic (ordered event log), semantic (user facts dict), procedural (always-on behaviour rules). An LLM classifier routes each input to the correct tier. Respond node builds a system prompt from all three tiers on every turn.

---

### Flow

```
START → classify_and_store (LLM routes to episodic/semantic/procedural tier)
      → respond (system prompt = all three tiers, last-5 episodic)
      → END
```

### Key concepts
- Episodic: append-only list, retrieved by recency (last N)
- Semantic: key-value dict, retrieved by key lookup
- Procedural: rule list, ALWAYS prepended to every system prompt
- LLM classifier: one-word output (episodic/semantic/procedural)
- MemoryStore TypedDict in LangGraph state — no external DB needed for the pattern
