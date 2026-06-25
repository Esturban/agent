---
teaching_ready: true
---
# 48-deepeval-hallucination-bias

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none

```bash
pip install deepeval
python examples/48-deepeval-hallucination-bias/main.py
```

DeepEval safety metrics: HallucinationMetric, BiasMetric, ToxicityMetric. Deliberately injects failing outputs to show scores respond correctly. Explains the Faithfulness vs Hallucination distinction and includes math definitions.

---

### Graph

```
grounded workflow:   START → respond (context-grounded) → END
freeform workflow:   START → respond (no context)        → END
```

### Safety Metrics

| Metric | Formula | What it detects |
|--------|---------|-----------------|
| Hallucination | contradicted_claims / total_claims | Statements that contradict the given context |
| Bias | biased_opinions / total_opinions | Gender, race, age, political stereotypes |
| Toxicity | toxic_segments / total_segments | Harmful, offensive, or aggressive language |

### Faithfulness vs Hallucination

| Metric | Input | What it measures |
|--------|-------|-----------------|
| Faithfulness | RAG answer + retrieval context | Grounded in *retrieved* docs |
| Hallucination | LLM output + source context | Contradicts *any* provided context |
