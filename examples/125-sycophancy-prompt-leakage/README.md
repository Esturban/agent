# 125 — Sycophancy-Based Prompt Leakage

Flattery raises system prompt extraction ASR from 17.7% to 86.2%. Salesforce, EMNLP 2024 (arxiv:2404.16251).

Runs a 4-attack × 3-defense matrix and shows which combinations leak the embedded canary token.

## Run

```bash
python main.py
```

## Key files

| File | Purpose |
|------|---------|
| `prompts/attack_variants.py` | 4 attacks: baseline, flattery, reiteration, combined (Salesforce) |
| `prompts/system_prompt.py` | 3 system prompt variants (strict/moderate/loose) with canary tokens |
| `prompts/defenses.py` | 3 defenses: none, instruction guard, canary injection |
| `src/rag_agent.py` | Minimal RAG agent with synthetic Acme Corp knowledge base |
| `src/attacker.py` | 2-turn attack (benign opener → sycophancy payload) |
| `src/monitor.py` | Canary string search + LLM-based sycophancy pattern classifier |
| `src/comparison.py` | Builds the 4×3 results matrix |
