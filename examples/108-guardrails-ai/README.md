# 108 - Guardrails AI

Wraps a raw OpenAI call with a `Guard` that enforces a Pydantic output schema: max-200-char summary, exactly 3 bullet points, no URLs. When the LLM violates any validator, the Guard automatically reasks with a correction instruction — no LangChain or LangGraph required.

Requires `pip install guardrails-ai`.

## Run

```bash
cp .env.example .env  # add OPENAI_API_KEY
pip install guardrails-ai
python main.py
```
