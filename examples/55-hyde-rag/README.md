# 55-hyde-rag

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none -- 10-doc corpus is inline in src/tools.py
**Colab:** not applicable -- requires local Chroma

```bash
python examples/55-hyde-rag/main.py
```

Hypothetical Document Embeddings (Gao et al. 2022): instead of embedding the raw query, ask the LLM to write a plausible answer first (even if hallucinated), then embed that answer and use it as the retrieval vector. The hypothesis lives in the same embedding space as real answer documents, producing better nearest-neighbor matches for question-style queries.

---

### Graph

```
START
  |
hypothesize   <- LLM writes a plausible answer to the query
  |
retrieve      <- embed hypothesis vector, similarity_search_by_vector k=3
  |
generate      <- ChatOpenAI with retrieved context + original query
  |
END
```
