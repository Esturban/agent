---
teaching_ready: true
---
# 106 - Jailbreak Detection

Classifies user inputs against 5 attack families (DAN, roleplay, encoding, many-shot, override) using an LLM-as-judge node that intercepts before the target model ever sees the prompt. Blocked inputs never reach the downstream LLM.

Based on the taxonomy from Wei et al. 2023 "Jailbroken: How Does LLM Safety Training Fail?" (arxiv.org/abs/2307.02483).

## Run

```bash
cp .env.example .env  # add OPENAI_API_KEY
python main.py
```
