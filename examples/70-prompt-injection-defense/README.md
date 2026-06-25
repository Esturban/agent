---
teaching_ready: true
---
# 70-prompt-injection-defense

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none -- 10-doc corpus with 3 planted injections is inline in src/tools.py
**Colab:** not applicable -- requires local execution

```bash
python examples/70-prompt-injection-defense/main.py
```

Prompt Injection Defense: demonstrates indirect prompt injection (attackers plant override instructions inside retrieved documents) and a defended RAG pipeline. Each retrieved chunk is classified by `InjectionRisk` before being passed to the LLM — high-risk chunks are stripped entirely.

---

### Graph

```
START
  |
retrieve         <- similarity_search(question, k=6) from Chroma
  |
classify_chunks  <- InjectionRisk classifier for each chunk (high/low)
  |
filter_chunks    <- discard high-risk chunks
  |
generate         <- ChatOpenAI answers from safe context only
  |
END
```
