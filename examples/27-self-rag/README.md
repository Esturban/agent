# 27-self-rag

Self-RAG (Asai et al. 2023): before retrieving, an LLM classifier decides *if* retrieval is even needed. If yes, each retrieved document is graded for relevance (Gate 2) and the final answer is checked for groundedness (Gate 3). Three conditional gates implemented as LangGraph nodes: `classify → retrieve → grade_docs → generate → check_support`.

**Keys:** `OPENAI_API_KEY`

```bash
python examples/27-self-rag/main.py
```

---

### Graph

```
START
  │
classify          ← should_retrieve? (Gate 1)
  │
  ├─ True  → retrieve → grade_docs → generate → check_support → END
  │                      (Gate 2: filter irrelevant docs)         (Gate 3: isSupported?)
  │
  └─ False → generate → check_support → END
```
