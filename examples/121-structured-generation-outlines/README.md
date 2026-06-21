# 121 — Structured Generation with Outlines

Guarantee JSON and regex-constrained output from any open model using the `outlines` library, and compare to the `instructor` retry approach.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/121-structured-generation-outlines/structured_generation_outlines_workbook.ipynb)

## What it does

- Defines Pydantic models: `ExtractedPerson`, `ParsedDate`
- Demos 3 constraint types: JSON schema, regex pattern, choice list
- Compares outlines (CFG sampling, 1 pass) vs instructor (retry loops, N API calls)

## How to run

```bash
# Demo mode (uses OpenAI fallback if outlines/transformers not installed)
python examples/121-structured-generation-outlines/main.py

# Full outlines mode (requires GPU + ~2GB download)
pip install outlines transformers torch
python examples/121-structured-generation-outlines/main.py
```

## Key insight

outlines modifies the token sampling process itself — invalid tokens get zero probability.
This guarantees valid output in one pass. instructor retries until the schema is satisfied.
Use outlines for local models; use instructor for hosted OpenAI/Anthropic APIs.
