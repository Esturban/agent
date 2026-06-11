# 48-deepeval-hallucination-bias

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/48-deepeval-hallucination-bias/hallucination_bias_workbook.ipynb)

DeepEval safety metrics: HallucinationMetric, BiasMetric, ToxicityMetric. Deliberately injects failing outputs to show scores respond correctly. Explains the Faithfulness vs Hallucination distinction and includes math definitions.

**Keys:** `OPENAI_API_KEY`

```bash
pip install deepeval
python examples/48-deepeval-hallucination-bias/main.py
```

---

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
