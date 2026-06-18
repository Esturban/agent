# 104 · Prompt Injection Defense

Demonstrates indirect prompt injection (Greshake et al. 2023) and two defenses side-by-side: an undefended browsing agent gets hijacked by malicious page content; a defended agent resists via instruction hierarchy + spotlighting.

## Run

```bash
cp .env.example .env   # add OPENAI_API_KEY
python examples/104-prompt-injection-defense/main.py
```

## What you'll see

Both agents browse the same 5 pages (2 safe, 3 with embedded attacks). The undefended agent may follow injected instructions; the defended agent summarises content only and ignores directives in page text.

## Key concepts

- **Indirect injection**: malicious instructions hidden in external content (web pages, documents, tool results) — not directly from the user
- **Instruction hierarchy**: system prompt > user task > tool results; model is told to ignore directives from lower tiers
- **Spotlighting**: wrapping external content in `<<<EXTERNAL_CONTENT>>>` markers signals to the model that this is data, not instructions
- Three attack patterns: role override, hidden directive, data exfiltration request
