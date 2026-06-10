# 26-rag-fusion

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/26-rag-fusion/rag_fusion_workbook.ipynb)

Generate N query paraphrases in parallel using the LangGraph Send API, retrieve independently for each, then merge results with Reciprocal Rank Fusion for higher recall than any single-query RAG.

## What makes it interesting

A single query is a point of failure — if your phrasing doesn't match the embedding space, you miss relevant docs entirely. RAG Fusion (Lawrence 2024) fixes this at the retrieval level: generate paraphrases, retrieve in parallel, merge with RRF. The key primitive is the **LangGraph Send API**, which dispatches the same node concurrently with different inputs and collects results back into shared state via `Annotated[list, add]`. RRF scoring (`1 / (k + rank)`) rewards documents that appear highly ranked across multiple query variants over documents that appear at rank 1 in only one.

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
generate_variants (LLM generates N paraphrases)
  |
  +--Send--> retrieve_variant (parallel, one per variant)
  +--Send--> retrieve_variant
  +--Send--> retrieve_variant
  +--Send--> retrieve_variant
       |
      fuse (RRF merge all ranked lists)
       |
    generate (LLM answers from fused context)
       |
      END
```

## RRF formula

```
score(doc) = sum( 1 / (RRF_K + rank_i) )  for each ranked list i
```

Documents appearing in the top positions across multiple lists win. `RRF_K=60` is the standard constant from the original paper.

## Related

- 22-hybrid-search-rag — ensemble BM25 + vector retrieval (single query, two retrievers)
- 25-adaptive-rag — route queries to the right retrieval strategy before retrieving
- 17-corrective-rag — grade documents after retrieval and fall back to web search
