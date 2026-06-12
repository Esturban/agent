# 64-pydantic-ai

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none
**Colab:** not applicable -- requires local execution

```bash
pip install pydantic-ai
python examples/64-pydantic-ai/main.py
```

Pydantic AI: builds a typed research agent using `pydantic_ai.Agent` with `result_type=ResearchResult` — the LLM is forced to return a validated Pydantic model (summary, key_facts, confidence) without any manual `with_structured_output` wiring. Contrast to 13-structured-output (LangChain approach) — Pydantic AI eliminates the boilerplate.

---

### Pattern (no LangGraph)

```
pydantic_ai.Agent("openai:gpt-5-nano", result_type=ResearchResult)
  |
agent.run_sync(query)  -> result.data is a validated ResearchResult instance
  |
print summary, key_facts, confidence
```
