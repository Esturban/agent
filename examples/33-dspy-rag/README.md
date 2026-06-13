# 33-dspy-rag

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none

```bash
python examples/33-dspy-rag/main.py
```

Builds a RAG pipeline using DSPy Signatures instead of hand-crafted prompts. Compiles the module with BootstrapFewShot to auto-discover few-shot examples, then compares base vs compiled answers side-by-side.

---

### Graph

```
SAMPLE_QUESTIONS
     |
  question
     |
  keyword_retrieve   ← TF-IDF-style scorer over inline DOCS
     |
  context
     |
  ChainOfThought(GenerateAnswer)   ← reasoning + answer
     |
  answer
```

### DSPy vs LangChain LCEL

| Concern | DSPy | LangChain LCEL |
|---------|------|----------------|
| Prompt authoring | Signature fields + docstring (auto-tuned) | Hand-written PromptTemplate |
| Optimization | BootstrapFewShot / MIPROv2 compiler | Manual iteration |
| Module composition | `dspy.Module.forward()` | `prompt | model | parser` |
| Few-shot examples | Auto-bootstrapped from trainset | Manually added to template |
