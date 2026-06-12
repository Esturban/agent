# 59-semantic-router

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none -- route descriptors are inline in src/tools.py
**Colab:** not applicable -- requires local execution

```bash
python examples/59-semantic-router/main.py
```

Semantic Router: route incoming queries to specialist handlers (code, billing, general) using cosine similarity over pre-embedded route descriptors — no LLM call needed for routing. The embeddings are built once at startup; each query is embedded and matched against the nearest route centroid. Queries scoring below 0.6 fall through to the general handler.

---

### Graph

```
START
  |
route_query   <- embed query, cosine_similarity vs all route descriptors, pick best match
  |
handle        <- specialist handler (code / billing / general) answers with ChatOpenAI
  |
END
```
