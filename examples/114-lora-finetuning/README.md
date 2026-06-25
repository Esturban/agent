---
teaching_ready: true
---
# 114 — LoRA Fine-Tuning

Attaches LoRA adapters (r=8, lora_alpha=16) to SmolLM2-135M, trains on a Python Q&A dataset for 1 epoch, then merges and unloads the adapters. Demonstrates that LoRA trains only ~0.1% of parameters while producing domain-specific behavior. Includes before/after inference comparison.

## Run
```bash
pip install peft transformers datasets torch accelerate
python main.py
```
