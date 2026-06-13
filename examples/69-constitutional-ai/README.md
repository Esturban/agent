# 69-constitutional-ai

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none -- prompts and constitution inline in src/tools.py
**Colab:** not applicable -- requires local execution

```bash
python examples/69-constitutional-ai/main.py
```

Constitutional AI (Bai et al. 2022): uses a written constitution (5 principles) to self-improve outputs instead of human feedback. Generates a response, critiques it against each principle individually, revises to fix violations, and loops until all principles pass or MAX_REVISIONS is hit.

---

### Graph

```
START
  |
generate  <- LLM produces initial response
  |
critique  <- check each principle independently (Critique structured output)
  |
  +-- no violations or max revisions --> END
  |
  +-- violations found --> revise -> critique  (loop)
```
