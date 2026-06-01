# Agentic AI Examples — LangGraph & LangChain

A progressive workbook covering core agentic AI patterns using LangGraph and LangChain:

- **RAG** — local and cloud vector stores, streaming, grading, and corrective loops
- **ReAct agents** — tool use, conversation memory, PDF retrieval
- **Multi-agent graphs** — supervisor routing, specialist agents, shared state
- **Human-in-the-loop** — interrupt and resume with checkpointing
- **Structured output** — search → validated Pydantic extraction
- **SQL agents** — natural language to SQL with a local SQLite database

Each example is self-contained — clone, install, and run.

---

## Examples

| # | Folder | What it demonstrates |
|---|--------|----------------------|
| 1 | [1-basic-local-rag](./examples/1-basic-local-rag/README.md) | Minimal RAG with local ChromaDB — documents loaded from the web, split, embedded, and queried in a single-node graph |
| 2 | [2-multi-tool-rag](./examples/2-multi-tool-rag/README.md) | RAG with a cloud-hosted Qdrant vector DB and a web-search fallback tool |
| 3 | [3-prospect-agent](./examples/3-prospect-agent/README.md) | Prospect research agent — DuckDuckGo search → personalized outreach draft + confidence score |
| 4 | [4-basic-react-agent](./examples/4-basic-react-agent/README.md) | ReAct agent with conversation memory and PDF retrieval |
| 5 | [5-react-agent-lg](./examples/5-react-agent-lg/README.md) | LangGraph ReAct agent: PDF summarizer + critique loop between two specialist nodes |
| 6 | [6-multi-agent-graph](./examples/6-multi-agent-graph/README.md) | Two-agent graph: `ProductQnA` and `OrdersAgent` routed by a supervisor node |
| 7 | [7-redis-rag](./examples/7-redis-rag/README.md) | RAG backed by Redis vector store; grader node decides whether to answer or rewrite the query |
| 8 | [8-new-idea-gen](./examples/8-new-idea-gen/README.md) | Two-stage pipeline: parse the free-for-dev list → generate structured, scored ideas |
| 9 | [9-prospect-searx](./examples/9-prospect-searx/README.md) | Prospect agent upgraded to SearXNG (self-hosted, privacy-focused, multi-engine) |
| 10 | [10-streaming-rag](./examples/10-streaming-rag/README.md) | Same RAG pipeline with `.stream(stream_mode="updates")` — live node-by-node output |
| 11 | [11-hitl-approval](./examples/11-hitl-approval/README.md) | Human-in-the-loop: `interrupt()` pauses the graph mid-run for yes/no approval, `Command(resume=…)` continues from checkpoint |
| 12 | [12-basic-rag-notebook](./examples/12-basic-rag-notebook/README.md) | Jupyter/Colab teaching workbook — chunk, embed, store, retrieve, generate end-to-end |
| 13 | [13-structured-output](./examples/13-structured-output/README.md) | Search → extract a validated Pydantic model with `with_structured_output()` |
| 14 | [14-sql-agent](./examples/14-sql-agent/README.md) | ReAct agent over a local SQLite DB using `create_react_agent`; seeds sample data on first run |
| 15 | [15-crewai-research-crew](./examples/15-crewai-research-crew/README.md) | CrewAI researcher + writer crew — contrasts `Crew`/`Agent`/`Task` primitives against LangGraph's `StateGraph` |

---

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then fill in your keys
```

Most examples need only `OPENAI_API_KEY`. Exceptions:
- `2-multi-tool-rag` — `QDRANT_URL`, `QDRANT_KEY`, `BRAVE_API_KEY`
- `3-prospect-agent` — optional `BRAVE_API_KEY`, optional `OPENROUTER_API_KEY`
- `8-new-idea-gen` — `BRAVE_API_KEY`, optional `OPENROUTER_API_KEY`
- `9-prospect-searx` — SearXNG running in Docker (see that folder's README)
- `7-redis-rag` — Redis (`docker run -p 6379:6379 -d redis`)

The root `.env.example` covers both the script examples and the notebook/workbook flows.

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
