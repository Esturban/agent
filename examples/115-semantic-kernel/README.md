---
teaching_ready: true
---
# 115-semantic-kernel

## Prerequisites
**Keys:** `OPENAI_API_KEY` in `.env`
**Deps:** `pip install semantic-kernel`
**Colab:** see workbook

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/115-semantic-kernel/semantic_kernel_workbook.ipynb)

```bash
python examples/115-semantic-kernel/main.py
```

Microsoft Semantic Kernel (SK) is the AI orchestration SDK powering Microsoft 365 Copilot.
This example registers Python functions as SK plugins using `@kernel_function`, then invokes
the Kernel with `FunctionChoiceBehavior.Auto` so the LLM decides which plugins to call
and in what sequence — the plugin/function-calling model vs. LangGraph's explicit graph.

---

### Architecture

```
Kernel
  |
  +-- OpenAIChatCompletion (gpt-4o-mini)
  |
  +-- WebSearchPlugin
  |     search(query) -> str
  |
  +-- SummarizerPlugin
        summarize(text, sentences) -> str
        extract_key_points(text) -> str

FunctionChoiceBehavior.Auto -> LLM decides call order
```
