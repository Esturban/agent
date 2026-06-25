---
teaching_ready: true
---
# 56-contextual-compression

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none -- 10-doc corpus is inline in src/tools.py
**Colab:** not applicable -- requires local Chroma

```bash
python examples/56-contextual-compression/main.py
```

Contextual compression: retrieve top-8 chunks with vector similarity, then use LLMChainFilter to ask the LLM "does this passage answer the query?" for each chunk, keeping only those that do. Reduces the context window sent to the generator, lowering hallucination risk and token cost.

---

### Graph

```
START
  |
retrieve   <- base_retriever top-k=8 from Chroma
  |
compress   <- LLMChainFilter via ContextualCompressionRetriever
  |
generate   <- ChatOpenAI with only the relevant compressed passages
  |
END
```
