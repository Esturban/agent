---
teaching_ready: true
---
# 113 — DPO: Direct Preference Optimization

Trains a tiny model (SmolLM2-135M) to prefer safe refusals over harmful responses using Direct Preference Optimization — no separate reward model needed. Uses a {prompt, chosen, rejected} dataset where chosen=safe refusal and rejected=unsafe compliant answer. Shows before/after comparison.

## Run
```bash
pip install trl peft transformers datasets torch
python main.py
```
