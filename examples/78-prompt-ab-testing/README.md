# 78-prompt-ab-testing

## Prerequisites
**Keys:** `OPENAI_API_KEY`

```bash
python examples/78-prompt-ab-testing/main.py
```

A/B tests two prompt variants (concise vs. detailed) across 5 questions, scores each response by word count, and declares a winner with a comparison table.

---

### Graph

```
run_variant_a (concise prompt → LLM → score)
  ↓
run_variant_b (detailed prompt → LLM → score)
  ↓
END
```
