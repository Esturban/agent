# 84-haystack-pipeline

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Deps:** `haystack-ai`

```bash
python examples/84-haystack-pipeline/main.py
```

Haystack 2.x — stateless DAG pipeline: `InMemoryBM25Retriever → PromptBuilder → OpenAIGenerator`. Components connect via named ports with `pipeline.connect("source.output", "target.input")`. Contrast with LangGraph's shared mutable state: Haystack passes data explicitly between ports; no global state dict.

---

### Flow

```
InMemoryDocumentStore (8 docs)
  ↓ BM25Retriever (top-k)
  ↓ PromptBuilder (Jinja2 template)
  ↓ OpenAIGenerator → replies[0]
```

### Key concepts
- `Pipeline.add_component()` — register a component instance under a name
- `Pipeline.connect("a.output", "b.input")` — wire named ports
- `pipeline.run({"retriever": {"query": q}, ...})` — pass inputs per-component
- `InMemoryBM25Retriever` — keyword retrieval, no embeddings needed
