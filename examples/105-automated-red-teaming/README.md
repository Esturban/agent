---
teaching_ready: true
---
# 105 · Automated Red-Teaming

LLMs as adversaries: an attacker LLM generates N adversarial prompts in parallel, a target LLM responds, and a judge scores each exchange. Computes the attack success rate (ASR) — based on Perez et al. 2022 (DeepMind).

## Run

```bash
cp .env.example .env   # add OPENAI_API_KEY
python examples/105-automated-red-teaming/main.py
```

## Key concepts

- **Three-role pipeline**: attacker (temp=0.9 for diversity) → target → judge
- **`Send()` fan-out**: N attack chains run concurrently; `operator.add` reducer collects results — same pattern as examples 89, 97, 98
- **Attack Success Rate (ASR)**: `successful_attacks / N` — the primary red-team metric
- Use this to test safety improvements: lower ASR after adding guardrails = measurable progress
