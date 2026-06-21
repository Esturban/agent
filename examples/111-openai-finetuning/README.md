# 111 - OpenAI Fine-Tuning API

Prepare a JSONL training dataset, upload to OpenAI, launch a fine-tuning job on `gpt-4o-mini`, poll until complete, then compare base vs. fine-tuned model accuracy on a held-out eval set. Task: customer service tone classification (formal / informal / urgent).

## Run

```bash
cp .env.example .env  # add OPENAI_API_KEY
python main.py                    # dry run — uploads data only, no training job
```

To launch an actual training job (costs ~$0.02–0.05):

```python
from src.workflow import create_workflow
create_workflow(dry_run=False)
```

## Workbook

Open `openai_finetuning_workbook.ipynb` for a step-by-step walkthrough of every stage with explanations, exercises, and an answer key.
