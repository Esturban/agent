# 41-pdf-extraction-agent

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/41-pdf-extraction-agent/pdf_extraction_workbook.ipynb)

Downloads an arXiv PDF, extracts text with `pdfplumber`, then uses `with_structured_output(PaperSchema)` to extract typed fields — with automatic retry on validation failure.

**Keys:** `OPENAI_API_KEY`

```bash
pip install pdfplumber requests
python examples/41-pdf-extraction-agent/main.py
```

---

### Graph

```
START → download → extract ◄──┐
                    |          │ (retry if failed, up to 3x)
                 success? ─────┘
                    |
                   END
```

### Key Concepts

| Concept | Description |
|---------|-------------|
| `pdfplumber` | Extract raw text from PDF bytes |
| `with_structured_output(PaperSchema)` | Force LLM to return validated Pydantic model |
| Retry loop | `add_conditional_edges` routes back on failure |
| `retries` counter | State field prevents infinite retry loop |
