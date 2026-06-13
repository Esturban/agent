# 74-ragas-evaluation

Runs RAGAS `evaluate()` programmatically on a 5-row QA dataset, scoring a minimal ChromaDB RAG pipeline on `faithfulness` and `answer_relevancy`. Outputs a per-question score table and mean scores.

## How to run

```bash
pip install ragas datasets
python main.py
```
