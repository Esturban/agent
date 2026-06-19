# 107 - NeMo Guardrails

Wires NVIDIA NeMo Guardrails to an OpenAI LLM using the Colang DSL. Demonstrates three rail types: input rails that block jailbreak attempts and off-topic requests before the LLM sees them, and output rails that intercept toxic responses before delivery.

Requires `nemoguardrails` (`pip install nemoguardrails`).

## Run

```bash
cp .env.example .env  # add OPENAI_API_KEY
pip install nemoguardrails
python main.py
```
