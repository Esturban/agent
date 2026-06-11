# 29-llm-judge-harness

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/29-llm-judge-harness/llm_judge_workbook.ipynb)

LLM-as-judge evaluation harness: run a RAG pipeline on a test set and score each answer on **Relevance**, **Faithfulness**, and **Completeness** using a structured rubric enforced with `with_structured_output`. No labelled data required — ideal for teams without ground-truth datasets. Extends 16-rag-eval-notebook with a custom judge approach beyond RAGAS.

**Keys:** `OPENAI_API_KEY`

```bash
jupyter notebook examples/29-llm-judge-harness/llm_judge_workbook.ipynb
```
