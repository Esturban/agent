---
teaching_ready: true
---
# 118-mirascope-typed-llm

## Prerequisites
**Keys:** `OPENAI_API_KEY` and `ANTHROPIC_API_KEY` in `.env`
**Deps:** `pip install "mirascope[openai,anthropic]"`
**Colab:** see workbook

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/118-mirascope-typed-llm/mirascope_typed_llm_workbook.ipynb)

```bash
python examples/118-mirascope-typed-llm/main.py
```

Mirascope is a Pydantic-first LLM toolkit where `@openai.call(response_model=...)` turns
a decorated function into a typed LLM call — prompt formatting, API invocation, and Pydantic
parsing in a single decorator. Swapping `@openai.call` for `@anthropic.call` switches the
provider with no other code changes. This example extracts a `MeetingSummary` from the same
transcript using both providers and compares results side-by-side.

---

### Provider-switch pattern

```python
# OpenAI
@openai.call(model="gpt-4o-mini", response_model=MeetingSummary)
@prompt_template("Summarize: {transcript}")
def summarize(transcript: str): ...

# Anthropic — only the decorator changes
@anthropic.call(model="claude-haiku-4-5", response_model=MeetingSummary)
@prompt_template("Summarize: {transcript}")
def summarize(transcript: str): ...
```
