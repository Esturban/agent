---
teaching_ready: true
---
# 67-mem0-memory

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none -- sample sessions are inline in main.py
**Deps:** `mem0ai`

```bash
python examples/67-mem0-memory/main.py
```

Mem0 (MemoryAI): automatically extracts semantic facts from conversation messages using an LLM, stores them in an in-memory Qdrant vector store, and retrieves them by semantic search. Three-node LangGraph: `recall_memories` (Mem0 search) → `respond` (LLM with recalled context) → `store_memories` (Mem0 add). Session 1 stores facts; Session 2 recalls them without re-reading the original messages. Includes a raw memory dump so you can see exactly what Mem0 extracted.

> **Cloud mode:** use `MemoryClient(api_key="m0-...")` from mem0ai cloud for true cross-process persistence. Local mode (`Memory()`) resets when the process exits.

---

### Graph

```
SESSION_1_MESSAGES (4 msgs) → store_memories: Mem0 auto-extracts facts
  ↓
memory dump: show raw Mem0 objects + scores

SESSION_2_QUERIES (3 questions) → recall → respond (no messages needed)
  ↓
compare vs 36-long-term-memory: Mem0 auto-extracts vs InMemoryStore explicit writes
```
