---
teaching_ready: true
---
# 65-litellm-multi-provider

## Prerequisites
**Keys:** `OPENAI_API_KEY` (required); `ANTHROPIC_API_KEY`, `MISTRAL_API_KEY` optional  
**Colab:** [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/esturban/agent/blob/main/examples/65-litellm-multi-provider/litellm_workbook.ipynb)

Open `litellm_workbook.ipynb` in Colab or Jupyter. Shows how `litellm.completion()` calls OpenAI, Anthropic, and Mistral with the same API — only the model string changes. Includes fallback chains via `Router`, per-call cost tracking with `completion_cost()`, and `ChatLiteLLM` for LangChain drop-in compatibility.

---

### Pattern (notebook)

```
litellm.completion("openai/gpt-4o-mini", ...)
  → same call, "anthropic/claude-haiku-4-5" / "mistral/mistral-small"
    → Router fallback chain: primary → fallback-1 on error
      → completion_cost() per call: cost comparison table
        → ChatLiteLLM: drop-in LangChain BaseChatModel
          → exercises: add provider, cost-threshold fallback
            → answer key
```
