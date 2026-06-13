# 76-agent-evaluation

## Prerequisites
**Keys:** `OPENAI_API_KEY`

```bash
python examples/76-agent-evaluation/main.py
```

Evaluates an agent against a golden QA dataset using exact-match and cosine-similarity scoring, printing a pass/fail result and score for each question.

---

### Graph

```
evaluate_one (run_agent + evaluate_answer)
  ↓
END
```
