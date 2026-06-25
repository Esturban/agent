---
teaching_ready: true
---
# 127 — Spotlighting: Indirect Prompt Injection Defense

Three data-isolation techniques that reduce indirect injection ASR from ~80% to near-zero — plus the adaptive attack that breaks encoding. Microsoft Research 2024 (arxiv:2403.14720).

## Run

```bash
python main.py          # 5 injections, 3 variants (none/delimiting/encoding)
python main.py --all    # 10 injections
```

## Key files

| File | Purpose |
|------|---------|
| `prompts/injections.py` | 10 payloads across 4 attack families + benign document |
| `prompts/system_prompts.py` | 4 system prompt variants with spotlighting instructions |
| `src/variants.py` | delimit() / datamark() / encode() transformation functions |
| `src/agent.py` | Document summarization agent |
| `src/injector.py` | Inserts payload into benign document |
| `src/adaptive_attack.py` | Pre-encoded bypass attack against encoding spotlighting |
| `src/benchmark.py` | Runs all variant × injection combinations, checks compliance |
