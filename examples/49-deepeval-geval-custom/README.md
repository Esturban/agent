---
teaching_ready: true
---
# 49-deepeval-geval-custom

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none

```bash
pip install deepeval
python examples/49-deepeval-geval-custom/main.py
```

G-Eval and custom metrics in DeepEval: define any evaluation criterion in natural language with `GEval(name, criteria, evaluation_steps)`, plus deterministic `BaseMetric` subclassing for exact-match and JSON schema checks.

---

### Graph

```
START
  |
generate   ← ChatOpenAI answers input query
  |
END        (GEval + BaseMetric run on the output)
```

### Two metric types

| Type | Class | When to use |
|------|-------|-------------|
| LLM-as-judge | `GEval(criteria, evaluation_steps)` | Subjective: tone, format, style, correctness |
| Deterministic | `BaseMetric` subclass | Objective: exact match, schema, length |

### G-Eval paper (Liu et al. 2023)

Chain-of-thought scoring: the judge LLM first generates reasoning steps, then assigns a score. Correlates 0.87 with human judgment vs 0.43 for ROUGE-L.
