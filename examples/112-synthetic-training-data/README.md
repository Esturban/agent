---
teaching_ready: true
---
# 112 - Synthetic Training Data Generation

Use GPT-4o to generate diverse labeled training examples for a classification task, deduplicate with embedding cosine similarity, validate with a second LLM judge, and export clean JSONL ready for fine-tuning (example 111). Implements the Stanford Alpaca / WizardLM data flywheel pattern.

## Run

```bash
cp .env.example .env  # add OPENAI_API_KEY
python main.py
```

## Workbook

Open `synthetic_training_data_workbook.ipynb` for a step-by-step walkthrough with exercises and answer key.
