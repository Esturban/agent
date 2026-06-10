# 25-adaptive-rag

Route each query to the cheapest strategy that correctly answers it: direct LLM, private vectorstore, or live web search.

## What makes it interesting

Most RAG pipelines apply one strategy uniformly — which means you pay embedding costs for trivial arithmetic questions and hallucinate on current-events queries. This example shows how a single LLM classifier (`with_structured_output`) can cheaply decide which path to take *before* any retrieval happens, routing at the graph edge level. It's a direct precursor to CRAG and Self-RAG: instead of correcting after bad retrieval, we skip retrieval entirely when it isn't needed.

## Prerequisites

| Requirement | Value |
|---|---|
| `OPENAI_API_KEY` | required |
| Extra files | none |
| Colab-ready | yes |

## Run

```bash
python main.py
```

## Graph

```
START
  |
classify (LLM routes query)
  |
  +-- "simple"      --> direct_answer --> END
  +-- "vectorstore" --> vectorstore_answer --> END
  +-- "web"         --> web_answer --> END
```

## Routing examples

| Question | Strategy |
|---|---|
| What is 7 × 8? | simple |
| What is your refund policy? | vectorstore |
| What is the current price of Bitcoin? | web |

## Related

- 17-corrective-rag — grades docs *after* retrieval and falls back to web if poor
- 22-hybrid-search-rag — fuses BM25 + vector retrieval before answering
- 26-rag-fusion — generates query variants in parallel via LangGraph Send API
