---
teaching_ready: true
---
# 132 — Indirect Injection Full Cycle

The richest attack/defense example: shows the complete lifecycle of an indirect prompt injection. The attacker poisons a web page and an email with hidden instructions. The undefended agent executes them. The defended pipeline applies spotlighting (XML delimiters), privilege separation (no exfiltration tools in the research context), and pre-model injection scanning.

## How to run

```bash
python main.py
```

## Attack vectors demonstrated

- HTML comment injection + CSS-invisible div in a web page
- Compliance-disguised instructions embedded in an email body

## Defense layers

1. **Spotlighting**: XML `<external_data>` delimiters + system prompt policy
2. **Privilege separation**: send_email / read_contacts not available in research context
3. **Output scan**: keyword detection before content reaches the model

Papers: arxiv:2503.15547, arxiv:2403.14720 (spotlighting), arxiv:2504.11703
