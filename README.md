# Agentic AI Examples — LangGraph & LangChain

A progressive workbook covering core agentic AI patterns using LangGraph and LangChain:

- **RAG** — local and cloud vector stores, streaming, Corrective RAG (CRAG) with document grading and query rewrite
- **ReAct agents** — tool use, conversation memory, PDF retrieval
- **Multi-agent graphs** — supervisor routing, specialist agents, shared state
- **Human-in-the-loop** — interrupt and resume with checkpointing
- **Structured output** — search → validated Pydantic extraction
- **SQL agents** — natural language to SQL with a local SQLite database
- **Evaluation** — RAGAS faithfulness/relevance/recall scoring and LLM-as-judge harnesses

Each example is self-contained — clone, install, and run.

---

## Examples

| # | Folder | What it demonstrates | Workbook |
|---|--------|----------------------|:-------:|
| 1 | [1-basic-local-rag](./examples/1-basic-local-rag/README.md) | Minimal RAG with local ChromaDB — documents loaded from the web, split, embedded, and queried in a single-node graph | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/1-basic-local-rag/basic_local_rag_workbook.ipynb) |
| 2 | [2-multi-tool-rag](./examples/2-multi-tool-rag/README.md) | RAG with a cloud-hosted Qdrant vector DB and a web-search fallback tool | — |
| 3 | [3-prospect-agent](./examples/3-prospect-agent/README.md) | Prospect research agent — DuckDuckGo search → personalized outreach draft + confidence score | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/3-prospect-agent/prospect_agent_workbook.ipynb) |
| 4 | [4-basic-react-agent](./examples/4-basic-react-agent/README.md) | ReAct agent with conversation memory and PDF retrieval | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/4-basic-react-agent/basic_react_agent_workbook.ipynb) |
| 5 | [5-react-agent-lg](./examples/5-react-agent-lg/README.md) | LangGraph ReAct agent: PDF summarizer + critique loop between two specialist nodes | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/5-react-agent-lg/react_agent_lg_workbook.ipynb) |
| 6 | [6-multi-agent-graph](./examples/6-multi-agent-graph/README.md) | Two-agent graph: `ProductQnA` and `OrdersAgent` routed by a supervisor node | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/6-multi-agent-graph/multi_agent_graph_workbook.ipynb) |
| 7 | [7-redis-rag](./examples/7-redis-rag/README.md) | RAG backed by Redis vector store; grader node decides whether to answer or rewrite the query | — |
| 8 | [8-new-idea-gen](./examples/8-new-idea-gen/README.md) | Two-stage pipeline: parse the free-for-dev list → generate structured, scored ideas | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/8-new-idea-gen/new_idea_gen_workbook.ipynb) |
| 9 | [9-prospect-searx](./examples/9-prospect-searx/README.md) | Prospect agent upgraded to SearXNG (self-hosted, privacy-focused, multi-engine) | — |
| 10 | [10-streaming-rag](./examples/10-streaming-rag/README.md) | Same RAG pipeline with `.stream(stream_mode="updates")` — live node-by-node output | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/10-streaming-rag/streaming_rag_workbook.ipynb) |
| 11 | [11-hitl-approval](./examples/11-hitl-approval/README.md) | Human-in-the-loop: `interrupt()` pauses the graph mid-run for yes/no approval, `Command(resume=…)` continues from checkpoint | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/11-hitl-approval/hitl_workbook.ipynb) |
| 12 | [12-basic-rag-notebook](./examples/12-basic-rag-notebook/README.md) | Jupyter/Colab teaching workbook — chunk, embed, store, retrieve, generate end-to-end | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/12-basic-rag-notebook/rag_workbook.ipynb) |
| 13 | [13-structured-output](./examples/13-structured-output/README.md) | Search → extract a validated Pydantic model with `with_structured_output()` | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/13-structured-output/structured_output_workbook.ipynb) |
| 14 | [14-sql-agent](./examples/14-sql-agent/README.md) | ReAct agent over a local SQLite DB using `create_react_agent`; seeds sample data on first run | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/14-sql-agent/sql_workbook.ipynb) |
| 15 | [15-crewai-research-crew](./examples/15-crewai-research-crew/README.md) | CrewAI researcher + writer crew — contrasts `Crew`/`Agent`/`Task` primitives against LangGraph's `StateGraph` | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/15-crewai-research-crew/crewai_workbook.ipynb) |
| 16 | [16-rag-eval-notebook](./examples/16-rag-eval-notebook/README.md) | RAGAS evaluation workbook — score a RAG pipeline on faithfulness, answer relevance, and context recall | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/16-rag-eval-notebook/rag_eval_workbook.ipynb) |
| 17 | [17-corrective-rag](./examples/17-corrective-rag/README.md) | Corrective RAG (CRAG) — LLM grades each retrieved doc, rewrites query if irrelevant, falls back to web search | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/17-corrective-rag/corrective_rag_workbook.ipynb) |
| 18 | [18-self-reflecting-agent](./examples/18-self-reflecting-agent/README.md) | Reflexion loop — generate answer, critique with structured confidence score, revise until confident or capped | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/18-self-reflecting-agent/reflexion_workbook.ipynb) |
| 19 | [19-multi-agent-notebook](./examples/19-multi-agent-notebook/README.md) | Supervisor/Worker multi-agent pattern — supervisor LLM routes tasks to researcher + writer workers via `add_messages` state | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/19-multi-agent-notebook/multi_agent_workbook.ipynb) |
| 20 | [20-code-interpreter](./examples/20-code-interpreter/README.md) | Code interpreter loop — write Python, run in subprocess sandbox, fix on error until max iterations | — |
| 21 | [21-autogen-debate](./examples/21-autogen-debate/README.md) | Two-agent AutoGen debate — Proponent vs Opponent argue back and forth for MAX_TURNS exchanges | — |
| 22 | [22-hybrid-search-rag](./examples/22-hybrid-search-rag/README.md) | Hybrid Search RAG — BM25 keyword + vector retrieval merged via Reciprocal Rank Fusion | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/22-hybrid-search-rag/hybrid_search_rag_workbook.ipynb) |
| 23 | [23-crewai-notebook](./examples/23-crewai-notebook/README.md) | CrewAI deep-dive workbook — `Agent`, `Task`, `Crew`, sequential and hierarchical processes | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/23-crewai-notebook/crewai_workbook.ipynb) |
| 24 | [24-graph-rag](./examples/24-graph-rag/README.md) | Graph RAG — extract `(subject, predicate, object)` triples into NetworkX, answer multi-hop questions via graph traversal | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/24-graph-rag/graph_rag_workbook.ipynb) |
| 25 | [25-adaptive-rag](./examples/25-adaptive-rag/README.md) | Adaptive RAG — classify each query and route to the cheapest correct strategy: direct LLM, vectorstore, or web search | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/25-adaptive-rag/adaptive_rag_workbook.ipynb) |
| 26 | [26-rag-fusion](./examples/26-rag-fusion/README.md) | RAG Fusion — generate N query paraphrases in parallel via Send API, retrieve each, merge with RRF for higher recall | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/26-rag-fusion/rag_fusion_workbook.ipynb) |
| 27 | [27-self-rag](./examples/27-self-rag/README.md) | Self-RAG — three decision gates: classify if retrieval is needed, grade doc relevance, check answer groundedness | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/27-self-rag/self_rag_workbook.ipynb) |
| 28 | [28-parallel-subgraph](./examples/28-parallel-subgraph/README.md) | Parallel subgraphs — Send API map-reduce: fan out N workers via `Send`, merge with `Annotated[list, operator.add]` | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/28-parallel-subgraph/parallel_subgraph_workbook.ipynb) |
| 29 | [29-llm-judge-harness](./examples/29-llm-judge-harness/README.md) | LLM-as-judge eval harness — score RAG answers on Relevance, Faithfulness, Completeness with a structured rubric | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/29-llm-judge-harness/llm_judge_workbook.ipynb) |
| 30 | [30-agentic-rag](./examples/30-agentic-rag/README.md) | Agentic RAG — retrieval as one tool in a ReAct loop alongside web search and calculator; agent chooses per-turn | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/30-agentic-rag/agentic_rag_workbook.ipynb) |

> Links in the Workbook column open the .ipynb directly in Google Colab. — = requires local service or external credentials not available in Colab.

---

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then fill in your keys
```

## Prerequisites at a glance

| # | API keys | Local files | Services |
|---|----------|-------------|----------|
| 1 | `OPENAI_API_KEY` | — | — |
| 2 | `OPENAI_API_KEY` · `QDRANT_URL` · `QDRANT_KEY` · `BRAVE_API_KEY` | — | Qdrant Cloud |
| 3 | `OPENAI_API_KEY` · optional `BRAVE_API_KEY` · optional `OPENROUTER_API_KEY` | `data/Connections.csv` | — |
| 4 | `OPENAI_API_KEY` | `data/product/Laptop pricing.csv` · `data/product/Laptop product descriptions.pdf` | — |
| 5 | `OPENAI_API_KEY` | `data/product/EcoSprint_Specification_Document.pdf` | — |
| 6 | `OPENAI_API_KEY` | `data/product/Laptop pricing.csv` · `data/product/Laptop Orders.csv` · `data/product/Laptop product descriptions.pdf` | — |
| 7 | `OPENAI_API_KEY` | — | Redis (`docker run -p 6379:6379 -d redis`) |
| 8 | `OPENAI_API_KEY` · `BRAVE_API_KEY` | — | — |
| 9 | `OPENAI_API_KEY` or `OPENROUTER_API_KEY` | `data/Connections.csv` | SearXNG (Docker — see folder README) |
| 10 | `OPENAI_API_KEY` | — | — |
| 11 | `OPENAI_API_KEY` | — | — |
| 12 | `OPENAI_API_KEY` | — | — |
| 13 | `OPENAI_API_KEY` | — | — |
| 14 | `OPENAI_API_KEY` | — | — |
| 15 | `OPENAI_API_KEY` | — | — |
| 16 | `OPENAI_API_KEY` | — | — |
| 17 | `OPENAI_API_KEY` | — | — |
| 18 | `OPENAI_API_KEY` | — | — |
| 19 | `OPENAI_API_KEY` | — | — |
| 20 | `OPENAI_API_KEY` | — | — |
| 21 | `OPENAI_API_KEY` | — | — |
| 22 | `OPENAI_API_KEY` | — | — |
| 23 | `OPENAI_API_KEY` | — | — |
| 24 | `OPENAI_API_KEY` | — | — |
| 25 | `OPENAI_API_KEY` | — | — |
| 26 | `OPENAI_API_KEY` | — | — |
| 27 | `OPENAI_API_KEY` | — | — |
| 28 | `OPENAI_API_KEY` | — | — |
| 29 | `OPENAI_API_KEY` | — | — |
| 30 | `OPENAI_API_KEY` | — | — |

Each folder's README has the exact setup steps.

---

## Running an example

```bash
# scripts
python examples/14-sql-agent/main.py

# notebooks
jupyter notebook examples/12-basic-rag-notebook/rag_workbook.ipynb
```

---

## Repo layout

```
examples/
  {n}-{slug}/
    main.py          # entry point
    src/
      workflow.py    # create_workflow()
      tools.py       # tool definitions
    README.md
_queue/
  ideas.json         # planned examples (15+)
requirements.txt
```
