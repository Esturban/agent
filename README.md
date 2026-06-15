# Agentic AI Examples — LangGraph & LangChain

A progressive workbook covering core agentic AI patterns using LangGraph and LangChain:

- **RAG** — local/cloud vector stores, streaming, CRAG, HyDE, RAG Fusion, Self-RAG, Speculative RAG, hybrid search, reranking, contextual compression, step-back prompting, tabular RAG, parent document retriever
- **ReAct agents** — tool use, conversation memory, PDF retrieval, Plan-Execute, ReWOO, Tree of Thoughts, Chain-of-Verification, Constitutional AI
- **Multi-agent graphs** — supervisor routing, specialist agents, parallel subgraphs, supervisor-worker, multi-agent debate
- **Human-in-the-loop** — interrupt and resume with checkpointing, risk-based approval gates
- **Structured output** — search → validated Pydantic extraction, guardrails, prompt injection defense
- **Memory and state** — long-term cross-session memory, Redis memory, Mem0, checkpoint/resume
- **Evaluation** — RAGAS, DeepEval (RAG, safety, G-Eval, agentic, conversational, synthesizer), LLM-as-judge, agent golden dataset, prompt A/B testing
- **Observability** — LangSmith tracing, Langfuse, custom callback handler, token budget manager
- **Production** — FastAPI SSE streaming, async LangGraph, batch agent runner, semantic router
- **Framework landscape** — CrewAI, AutoGen, OpenAI Agents SDK, DSPy, Pydantic AI, LiteLLM, SmolAgents

Each example is self-contained — clone, install, and run.

> **Workbook column:** links open the `.ipynb` directly in Google Colab. `—` = requires a local service (Redis, SearXNG, FastAPI server) or external account not available in Colab.

---

## All Examples

<details>
<summary>Complete list — all 82 examples in order</summary>

| # | Folder | What it demonstrates | Keys | Workbook |
|---|--------|----------------------|:------:|:-------:|
| 1 | [1-basic-local-rag](./examples/1-basic-local-rag/README.md) | Minimal RAG with local ChromaDB — documents loaded from the web, split, embedded, and queried in a single-node graph | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/1-basic-local-rag/basic_local_rag_workbook.ipynb) |
| 2 | [2-multi-tool-rag](./examples/2-multi-tool-rag/README.md) | RAG with a cloud-hosted Qdrant vector DB and a web-search fallback tool | ✅ +Qdrant +Brave | — |
| 3 | [3-prospect-agent](./examples/3-prospect-agent/README.md) | Prospect research agent — DuckDuckGo search → personalized outreach draft + confidence score | ✅ opt.+Brave | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/3-prospect-agent/prospect_agent_workbook.ipynb) |
| 4 | [4-basic-react-agent](./examples/4-basic-react-agent/README.md) | ReAct agent with conversation memory and PDF retrieval | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/4-basic-react-agent/basic_react_agent_workbook.ipynb) |
| 5 | [5-react-agent-lg](./examples/5-react-agent-lg/README.md) | LangGraph ReAct agent: PDF summarizer + critique loop between two specialist nodes | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/5-react-agent-lg/react_agent_lg_workbook.ipynb) |
| 6 | [6-multi-agent-graph](./examples/6-multi-agent-graph/README.md) | Two-agent graph: `ProductQnA` and `OrdersAgent` routed by a supervisor node | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/6-multi-agent-graph/multi_agent_graph_workbook.ipynb) |
| 7 | [7-redis-rag](./examples/7-redis-rag/README.md) | RAG backed by Redis vector store; grader node decides whether to answer or rewrite the query | ✅ +Redis | — |
| 8 | [8-new-idea-gen](./examples/8-new-idea-gen/README.md) | Two-stage pipeline: parse the free-for-dev list → generate structured, scored ideas | ✅ +Brave | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/8-new-idea-gen/new_idea_gen_workbook.ipynb) |
| 9 | [9-prospect-searx](./examples/9-prospect-searx/README.md) | Prospect agent upgraded to SearXNG (self-hosted, privacy-focused, multi-engine) | ✅ +SearXNG | — |
| 10 | [10-streaming-rag](./examples/10-streaming-rag/README.md) | Same RAG pipeline with `.stream(stream_mode="updates")` — live node-by-node output | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/10-streaming-rag/streaming_rag_workbook.ipynb) |
| 11 | [11-hitl-approval](./examples/11-hitl-approval/README.md) | Human-in-the-loop: `interrupt()` pauses the graph mid-run for yes/no approval, `Command(resume=…)` continues from checkpoint | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/11-hitl-approval/hitl_workbook.ipynb) |
| 12 | [12-basic-rag-notebook](./examples/12-basic-rag-notebook/README.md) | Jupyter/Colab teaching workbook — chunk, embed, store, retrieve, generate end-to-end | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/12-basic-rag-notebook/rag_workbook.ipynb) |
| 13 | [13-structured-output](./examples/13-structured-output/README.md) | Search → extract a validated Pydantic model with `with_structured_output()` | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/13-structured-output/structured_output_workbook.ipynb) |
| 14 | [14-sql-agent](./examples/14-sql-agent/README.md) | ReAct agent over a local SQLite DB using `create_react_agent`; seeds sample data on first run | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/14-sql-agent/sql_workbook.ipynb) |
| 15 | [15-crewai-research-crew](./examples/15-crewai-research-crew/README.md) | CrewAI researcher + writer crew — contrasts `Crew`/`Agent`/`Task` primitives against LangGraph's `StateGraph` | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/15-crewai-research-crew/crewai_workbook.ipynb) |
| 16 | [16-rag-eval-notebook](./examples/16-rag-eval-notebook/README.md) | RAGAS evaluation workbook — score a RAG pipeline on faithfulness, answer relevance, and context recall | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/16-rag-eval-notebook/rag_eval_workbook.ipynb) |
| 17 | [17-corrective-rag](./examples/17-corrective-rag/README.md) | Corrective RAG (CRAG) — LLM grades each retrieved doc, rewrites query if irrelevant, falls back to web search | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/17-corrective-rag/corrective_rag_workbook.ipynb) |
| 18 | [18-self-reflecting-agent](./examples/18-self-reflecting-agent/README.md) | Reflexion loop — generate answer, critique with structured confidence score, revise until confident or capped | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/18-self-reflecting-agent/reflexion_workbook.ipynb) |
| 19 | [19-multi-agent-notebook](./examples/19-multi-agent-notebook/README.md) | Supervisor/Worker multi-agent pattern — supervisor LLM routes tasks to researcher + writer workers via `add_messages` state | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/19-multi-agent-notebook/multi_agent_workbook.ipynb) |
| 20 | [20-code-interpreter](./examples/20-code-interpreter/README.md) | Code interpreter loop — write Python, run in subprocess sandbox, fix on error until max iterations | ✅ | — |
| 21 | [21-autogen-debate](./examples/21-autogen-debate/README.md) | Two-agent AutoGen debate — Proponent vs Opponent argue back and forth for MAX_TURNS exchanges | ✅ | — |
| 22 | [22-hybrid-search-rag](./examples/22-hybrid-search-rag/README.md) | Hybrid Search RAG — BM25 keyword + vector retrieval merged via Reciprocal Rank Fusion | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/22-hybrid-search-rag/hybrid_search_rag_workbook.ipynb) |
| 23 | [23-crewai-notebook](./examples/23-crewai-notebook/README.md) | CrewAI deep-dive workbook — `Agent`, `Task`, `Crew`, sequential and hierarchical processes | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/23-crewai-notebook/crewai_workbook.ipynb) |
| 24 | [24-graph-rag](./examples/24-graph-rag/README.md) | Graph RAG — extract `(subject, predicate, object)` triples into NetworkX, answer multi-hop questions via graph traversal | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/24-graph-rag/graph_rag_workbook.ipynb) |
| 25 | [25-adaptive-rag](./examples/25-adaptive-rag/README.md) | Adaptive RAG — classify each query and route to the cheapest correct strategy: direct LLM, vectorstore, or web search | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/25-adaptive-rag/adaptive_rag_workbook.ipynb) |
| 26 | [26-rag-fusion](./examples/26-rag-fusion/README.md) | RAG Fusion — generate N query paraphrases in parallel via Send API, retrieve each, merge with RRF for higher recall | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/26-rag-fusion/rag_fusion_workbook.ipynb) |
| 27 | [27-self-rag](./examples/27-self-rag/README.md) | Self-RAG — three decision gates: classify if retrieval is needed, grade doc relevance, check answer groundedness | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/27-self-rag/self_rag_workbook.ipynb) |
| 28 | [28-parallel-subgraph](./examples/28-parallel-subgraph/README.md) | Parallel subgraphs — Send API map-reduce: fan out N workers via `Send`, merge with `Annotated[list, operator.add]` | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/28-parallel-subgraph/parallel_subgraph_workbook.ipynb) |
| 29 | [29-llm-judge-harness](./examples/29-llm-judge-harness/README.md) | LLM-as-judge eval harness — score RAG answers on Relevance, Faithfulness, Completeness with a structured rubric | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/29-llm-judge-harness/llm_judge_workbook.ipynb) |
| 30 | [30-agentic-rag](./examples/30-agentic-rag/README.md) | Agentic RAG — retrieval as one tool in a ReAct loop alongside web search and calculator; agent chooses per-turn | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/30-agentic-rag/agentic_rag_workbook.ipynb) |
| 31 | [31-multi-agent-debate](./examples/31-multi-agent-debate/README.md) | Multi-agent debate — two solver agents argue Specialization vs Generalization across rounds; a judge LLM picks the winner | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/31-multi-agent-debate/multi_agent_debate_workbook.ipynb) |
| 32 | [32-speculative-rag](./examples/32-speculative-rag/README.md) | Speculative RAG — draft from training knowledge, extract claims, retrieve evidence per claim, revise only unsupported parts | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/32-speculative-rag/speculative_rag_workbook.ipynb) |
| 33 | [33-dspy-rag](./examples/33-dspy-rag/README.md) | DSPy RAG — declare Signatures instead of hand-crafting prompts; compile with BootstrapFewShot and compare base vs compiled answers | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/33-dspy-rag/dspy_rag_workbook.ipynb) |
| 34 | [34-openai-agents-sdk](./examples/34-openai-agents-sdk/README.md) | OpenAI Agents SDK — triage agent routes to Researcher (with `@tool`) or Writer via `handoff()`; built-in tracing, no LangGraph | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/34-openai-agents-sdk/openai_agents_workbook.ipynb) |
| 35 | [35-plan-execute-agent](./examples/35-plan-execute-agent/README.md) | Plan-Execute — planner emits a typed `Plan` via `with_structured_output`, executor loops each step, synthesizer combines all outputs | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/35-plan-execute-agent/plan_execute_workbook.ipynb) |
| 36 | [36-long-term-memory](./examples/36-long-term-memory/README.md) | Long-term memory — `InMemoryStore` persists user facts across thread boundaries; retrieve→respond→store loop | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/36-long-term-memory/long_term_memory_workbook.ipynb) |
| 37 | [37-rewoo-agent](./examples/37-rewoo-agent/README.md) | ReWOO — emit all tool calls upfront as a JSON plan with `$E1/$E2` variable substitution, execute in bulk, synthesize with evidence | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/37-rewoo-agent/rewoo_workbook.ipynb) |
| 38 | [38-langgraph-command-pattern](./examples/38-langgraph-command-pattern/README.md) | Command pattern — `Command(goto=route, update={...})` for edgeless dynamic routing; no `add_conditional_edges` needed | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/38-langgraph-command-pattern/command_pattern_workbook.ipynb) |
| 39 | [39-checkpoint-resume](./examples/39-checkpoint-resume/README.md) | Checkpoint & Resume — `SqliteSaver` persists full graph state to SQLite; resume from any `thread_id` across Python sessions | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/39-checkpoint-resume/checkpoint_resume_workbook.ipynb) |
| 40 | [40-agent-observability](./examples/40-agent-observability/README.md) | Agent observability — `BaseCallbackHandler` records token counts, latency, and errors per LLM call with zero external deps | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/40-agent-observability/observability_workbook.ipynb) |
| 41 | [41-pdf-extraction-agent](./examples/41-pdf-extraction-agent/README.md) | PDF extraction agent — download PDF, extract typed Pydantic schema with `with_structured_output`, retry on validation failure | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/41-pdf-extraction-agent/pdf_extraction_workbook.ipynb) |
| 42 | [42-multimodal-rag](./examples/42-multimodal-rag/README.md) | Multimodal RAG — describe images with GPT-4o-mini vision, embed descriptions in Chroma, retrieve and answer image questions | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/42-multimodal-rag/multimodal_rag_workbook.ipynb) |
| 43 | [43-supervisor-worker](./examples/43-supervisor-worker/README.md) | Supervisor-worker — `with_structured_output(WorkerRoute)` routes tasks to researcher/summarizer/analyst workers dynamically | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/43-supervisor-worker/supervisor_worker_workbook.ipynb) |
| 44 | [44-mcp-client-agent](./examples/44-mcp-client-agent/README.md) | MCP client agent — dynamic tool discovery via `list_tools()` + `call_tool()` with an in-process mock MCP server | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/44-mcp-client-agent/mcp_client_workbook.ipynb) |
| 45 | [45-a2a-agent-handoff](./examples/45-a2a-agent-handoff/README.md) | A2A agent handoff — typed `AgentTask(BaseModel)` contract between planner and executor agents; structured inter-agent communication | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/45-a2a-agent-handoff/a2a_handoff_workbook.ipynb) |
| 46 | [46-tree-of-thoughts](./examples/46-tree-of-thoughts/README.md) | Tree of Thoughts — Send API fans out N branches in parallel, judge LLM scores each, reducer selects best for synthesis | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/46-tree-of-thoughts/tree_of_thoughts_workbook.ipynb) |
| 47 | [47-deepeval-rag-metrics](./examples/47-deepeval-rag-metrics/README.md) | DeepEval RAG metrics: Faithfulness, AnswerRelevancy, ContextualPrecision, ContextualRecall, ContextualRelevancy with math definitions and failure injection | ✅ +DeepEval | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/47-deepeval-rag-metrics/deepeval_rag_workbook.ipynb) |
| 48 | [48-deepeval-hallucination-bias](./examples/48-deepeval-hallucination-bias/README.md) | DeepEval safety metrics: HallucinationMetric vs Faithfulness distinction, BiasMetric, ToxicityMetric with deliberate failure injection | ✅ +DeepEval | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/48-deepeval-hallucination-bias/hallucination_bias_workbook.ipynb) |
| 49 | [49-deepeval-geval-custom](./examples/49-deepeval-geval-custom/README.md) | G-Eval custom metrics: `GEval(criteria, evaluation_steps)` for LLM-as-judge + `BaseMetric` subclass for deterministic checks | ✅ +DeepEval | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/49-deepeval-geval-custom/geval_custom_workbook.ipynb) |
| 50 | [50-deepeval-agentic-eval](./examples/50-deepeval-agentic-eval/README.md) | DeepEval agentic metrics: `ToolCorrectnessMetric` with LangGraph tool call extraction from message history | ✅ +DeepEval | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/50-deepeval-agentic-eval/agentic_eval_workbook.ipynb) |
| 51 | [51-deepeval-conversational](./examples/51-deepeval-conversational/README.md) | DeepEval conversational metrics: KnowledgeRetention, ConversationCompleteness, ConversationRelevancy — stateful vs stateless chatbot comparison | ✅ +DeepEval | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/51-deepeval-conversational/conversational_eval_workbook.ipynb) |
| 52 | [52-deepeval-synthesizer](./examples/52-deepeval-synthesizer/README.md) | DeepEval Synthesizer: auto-generate golden datasets with SIMPLE/REASONING/MULTI_HOP/COMPARATIVE strategies; regression testing loop | ✅ +DeepEval | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/52-deepeval-synthesizer/synthesizer_workbook.ipynb) |
| 53 | [53-chunking-strategies](./examples/53-chunking-strategies/README.md) | Compare four chunking approaches side-by-side: CharacterTextSplitter, RecursiveCharacterTextSplitter, sentence-window, and semantic (cosine boundary detection) | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/53-chunking-strategies/chunking_workbook.ipynb) |
| 54 | [54-reranking-rag](./examples/54-reranking-rag/README.md) | Two-stage retrieval — retrieve top-20 candidates with Chroma vector search, rerank with FlashRank cross-encoder, pass top-4 to generation | ✅ +flashrank | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/54-reranking-rag/reranking_workbook.ipynb) |
| 55 | [55-hyde-rag](./examples/55-hyde-rag/README.md) | HyDE — generate a hypothetical answer, embed it instead of the raw query, retrieve with the richer embedding (Gao et al. 2022) | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/55-hyde-rag/hyde_workbook.ipynb) |
| 56 | [56-contextual-compression](./examples/56-contextual-compression/README.md) | Contextual compression — retrieve top-8 chunks, filter with `LLMChainFilter` to only the passage that answers the query, then generate | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/56-contextual-compression/contextual_compression_workbook.ipynb) |
| 57 | [57-step-back-prompting](./examples/57-step-back-prompting/README.md) | Step-Back Prompting — abstract a specific question to a broader principle, retrieve on the principle, answer the original (Zheng et al. 2023) | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/57-step-back-prompting/step_back_workbook.ipynb) |
| 58 | [58-tabular-rag](./examples/58-tabular-rag/README.md) | Tabular RAG — load a CSV, LLM writes a pandas expression for the schema + question, execute in a sandbox, retry on error | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/58-tabular-rag/tabular_rag_workbook.ipynb) |
| 59 | [59-semantic-router](./examples/59-semantic-router/README.md) | Semantic router — embed incoming queries and route to specialist nodes by cosine similarity; no LLM call needed for routing | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/59-semantic-router/semantic_router_workbook.ipynb) |
| 60 | [60-web-scraper-agent](./examples/60-web-scraper-agent/README.md) | Web scraper agent — fetch a URL, parse with BeautifulSoup, chunk into ephemeral Chroma, answer questions about the page | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/60-web-scraper-agent/web_scraper_workbook.ipynb) |
| 61 | [61-guardrails-agent](./examples/61-guardrails-agent/README.md) | Guardrails agent — Pydantic `InputGuard` + `OutputGuard` validate user input (PII, off-topic) and LLM output before returning | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/61-guardrails-agent/guardrails_workbook.ipynb) |
| 62 | [62-async-langgraph](./examples/62-async-langgraph/README.md) | Async LangGraph — fully async nodes with `ainvoke`/`astream`; `asyncio.gather` inside a node for concurrent tool calls | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/62-async-langgraph/async_langgraph_workbook.ipynb) |
| 63 | [63-token-budget-manager](./examples/63-token-budget-manager/README.md) | Token budget manager — track token usage per node with `tiktoken`, enforce a per-run budget, short-circuit gracefully when exceeded | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/63-token-budget-manager/token_budget_workbook.ipynb) |
| 64 | [64-pydantic-ai](./examples/64-pydantic-ai/README.md) | Pydantic AI — typed research agent with `result_type=ResearchResult`; framework contrast to LangGraph's StateGraph | ✅ +pydantic-ai | — |
| 65 | [65-litellm-multi-provider](./examples/65-litellm-multi-provider/README.md) | LiteLLM — same `completion()` call across OpenAI, Anthropic, and Mistral; fallback chains and cost tracking | ✅ +litellm | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/65-litellm-multi-provider/litellm_workbook.ipynb) |
| 66 | [66-smol-agents](./examples/66-smol-agents/README.md) | SmolAgents (HuggingFace) — `CodeAgent` writes Python as its reasoning trace; contrast to LangGraph nodes/edges | ✅ +smolagents | — |
| 67 | [67-mem0-memory](./examples/67-mem0-memory/README.md) | Mem0 cross-session memory — auto-extract semantic facts that persist across completely separate processes; contrast to LangGraph `InMemoryStore` | ✅ +mem0ai | — |
| 68 | [68-chain-of-verification](./examples/68-chain-of-verification/README.md) | Chain-of-Verification (CoVe) — generate answer, extract verifiable claims, check each independently, revise failures (Dhuliawala et al. 2023) | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/68-chain-of-verification/chain_of_verification_workbook.ipynb) |
| 69 | [69-constitutional-ai](./examples/69-constitutional-ai/README.md) | Constitutional AI — critique output against written principles, revise to comply, loop until satisfied (Bai et al. 2022) | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/69-constitutional-ai/constitutional_ai_workbook.ipynb) |
| 70 | [70-prompt-injection-defense](./examples/70-prompt-injection-defense/README.md) | Prompt injection defense — classify retrieved chunks for injection risk before passing to the LLM; filter high-risk passages | ✅ | — |
| 71 | [71-parent-document-retriever](./examples/71-parent-document-retriever/README.md) | Parent document retriever — index small child chunks for precision matching, return full parent document for rich context | ✅ | — |
| 72 | [72-batch-agent-runner](./examples/72-batch-agent-runner/README.md) | Batch agent runner — process tasks in parallel batches with `asyncio.gather`, tenacity exponential backoff, tqdm progress tracking | ✅ | — |
| 73 | [73-langsmith-tracing](./examples/73-langsmith-tracing/README.md) | LangSmith tracing — `@traceable` on each node + `LANGCHAIN_TRACING_V2=true`; inspect the full run tree in the LangSmith UI | ✅ +LangSmith | — |
| 74 | [74-ragas-evaluation](./examples/74-ragas-evaluation/README.md) | RAGAS evaluation script — build a QA dataset, run `evaluate()` with faithfulness + answer_relevancy; CI-ready | ✅ +ragas | — |
| 75 | [75-fastapi-sse-streaming](./examples/75-fastapi-sse-streaming/README.md) | FastAPI SSE — `StreamingResponse` wraps `graph.astream_events()` and formats each token as an SSE `data:` line over HTTP | ✅ +FastAPI | — |
| 76 | [76-agent-evaluation](./examples/76-agent-evaluation/README.md) | Agent evaluation — golden QA dataset, exact match + embedding cosine similarity scoring, per-question PASS/FAIL summary | ✅ | — |
| 77 | [77-langfuse-observability](./examples/77-langfuse-observability/README.md) | Langfuse observability — self-hostable LLM tracing via `CallbackHandler`; open-source alternative to LangSmith | ✅ +langfuse | — |
| 78 | [78-prompt-ab-testing](./examples/78-prompt-ab-testing/README.md) | Prompt A/B testing — run two prompt variants on 5 inputs, score by word count, declare winner with comparison table | ✅ | — |
| 79 | [79-interrupt-human-approval](./examples/79-interrupt-human-approval/README.md) | LangGraph interrupt — `interrupt()` pauses graph mid-execution; `Command(resume=approved)` resumes after human review; risk-based auto-approve | ✅ | — |
| 80 | [80-multi-agent-supervisor](./examples/80-multi-agent-supervisor/README.md) | Multi-agent supervisor — LLM classifies domain and dispatches to math, history, or science specialist agents via conditional edges | ✅ | — |
| 81 | [81-streaming-sse-server](./examples/81-streaming-sse-server/README.md) | SSE server — FastAPI `GET /stream?q=` endpoint streams `graph.astream_events()` token-by-token as Server-Sent Events | ✅ +FastAPI | — |
| 82 | [82-redis-memory](./examples/82-redis-memory/README.md) | Redis memory — Redis-backed cross-session agent memory with `load_history→respond→save_history` nodes and TTL | ✅ +Redis | — |

</details>

---

## Browse by Topic

<details>
<summary><strong>RAG — Retrieval-Augmented Generation</strong> &nbsp;·&nbsp; 20 examples</summary>

Local and cloud retrieval, streaming, CRAG, HyDE, RAG Fusion, Self-RAG, Speculative RAG, hybrid search, reranking, contextual compression, step-back prompting, graph RAG, tabular RAG, multimodal RAG, parent document retriever.

| # | Folder | What it demonstrates | Keys | Workbook |
|---|--------|----------------------|:------:|:-------:|
| 1 | [1-basic-local-rag](./examples/1-basic-local-rag/README.md) | Minimal RAG with local ChromaDB — documents loaded from the web, split, embedded, and queried in a single-node graph | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/1-basic-local-rag/basic_local_rag_workbook.ipynb) |
| 2 | [2-multi-tool-rag](./examples/2-multi-tool-rag/README.md) | RAG with a cloud-hosted Qdrant vector DB and a web-search fallback tool | ✅ +Qdrant +Brave | — |
| 7 | [7-redis-rag](./examples/7-redis-rag/README.md) | RAG backed by Redis vector store; grader node decides whether to answer or rewrite the query | ✅ +Redis | — |
| 10 | [10-streaming-rag](./examples/10-streaming-rag/README.md) | Same RAG pipeline with `.stream(stream_mode="updates")` — live node-by-node output | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/10-streaming-rag/streaming_rag_workbook.ipynb) |
| 12 | [12-basic-rag-notebook](./examples/12-basic-rag-notebook/README.md) | Jupyter/Colab teaching workbook — chunk, embed, store, retrieve, generate end-to-end | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/12-basic-rag-notebook/rag_workbook.ipynb) |
| 17 | [17-corrective-rag](./examples/17-corrective-rag/README.md) | Corrective RAG (CRAG) — LLM grades each retrieved doc, rewrites query if irrelevant, falls back to web search | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/17-corrective-rag/corrective_rag_workbook.ipynb) |
| 22 | [22-hybrid-search-rag](./examples/22-hybrid-search-rag/README.md) | Hybrid Search RAG — BM25 keyword + vector retrieval merged via Reciprocal Rank Fusion | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/22-hybrid-search-rag/hybrid_search_rag_workbook.ipynb) |
| 24 | [24-graph-rag](./examples/24-graph-rag/README.md) | Graph RAG — extract `(subject, predicate, object)` triples into NetworkX, answer multi-hop questions via graph traversal | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/24-graph-rag/graph_rag_workbook.ipynb) |
| 25 | [25-adaptive-rag](./examples/25-adaptive-rag/README.md) | Adaptive RAG — classify each query and route to the cheapest correct strategy: direct LLM, vectorstore, or web search | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/25-adaptive-rag/adaptive_rag_workbook.ipynb) |
| 26 | [26-rag-fusion](./examples/26-rag-fusion/README.md) | RAG Fusion — generate N query paraphrases in parallel via Send API, retrieve each, merge with RRF for higher recall | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/26-rag-fusion/rag_fusion_workbook.ipynb) |
| 27 | [27-self-rag](./examples/27-self-rag/README.md) | Self-RAG — three decision gates: classify if retrieval is needed, grade doc relevance, check answer groundedness | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/27-self-rag/self_rag_workbook.ipynb) |
| 32 | [32-speculative-rag](./examples/32-speculative-rag/README.md) | Speculative RAG — draft from training knowledge, extract claims, retrieve evidence per claim, revise only unsupported parts | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/32-speculative-rag/speculative_rag_workbook.ipynb) |
| 42 | [42-multimodal-rag](./examples/42-multimodal-rag/README.md) | Multimodal RAG — describe images with GPT-4o-mini vision, embed descriptions in Chroma, retrieve and answer image questions | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/42-multimodal-rag/multimodal_rag_workbook.ipynb) |
| 53 | [53-chunking-strategies](./examples/53-chunking-strategies/README.md) | Compare four chunking approaches side-by-side: CharacterTextSplitter, RecursiveCharacterTextSplitter, sentence-window, and semantic (cosine boundary detection) | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/53-chunking-strategies/chunking_workbook.ipynb) |
| 54 | [54-reranking-rag](./examples/54-reranking-rag/README.md) | Two-stage retrieval — retrieve top-20 candidates with Chroma vector search, rerank with FlashRank cross-encoder, pass top-4 to generation | ✅ +flashrank | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/54-reranking-rag/reranking_workbook.ipynb) |
| 55 | [55-hyde-rag](./examples/55-hyde-rag/README.md) | HyDE — generate a hypothetical answer, embed it instead of the raw query, retrieve with the richer embedding (Gao et al. 2022) | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/55-hyde-rag/hyde_workbook.ipynb) |
| 56 | [56-contextual-compression](./examples/56-contextual-compression/README.md) | Contextual compression — retrieve top-8 chunks, filter with `LLMChainFilter` to only the passage that answers the query, then generate | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/56-contextual-compression/contextual_compression_workbook.ipynb) |
| 57 | [57-step-back-prompting](./examples/57-step-back-prompting/README.md) | Step-Back Prompting — abstract a specific question to a broader principle, retrieve on the principle, answer the original (Zheng et al. 2023) | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/57-step-back-prompting/step_back_workbook.ipynb) |
| 58 | [58-tabular-rag](./examples/58-tabular-rag/README.md) | Tabular RAG — load a CSV, LLM writes a pandas expression for the schema + question, execute in a sandbox, retry on error | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/58-tabular-rag/tabular_rag_workbook.ipynb) |
| 71 | [71-parent-document-retriever](./examples/71-parent-document-retriever/README.md) | Parent document retriever — index small child chunks for precision matching, return full parent document for rich context | ✅ | — |

</details>

<details>
<summary><strong>ReAct Agents & Planning</strong> &nbsp;·&nbsp; 11 examples</summary>

Tool use, conversation memory, code interpreter loops, prospect research, SQL agents, reflexion, Plan-Execute, ReWOO, Tree of Thoughts.

| # | Folder | What it demonstrates | Keys | Workbook |
|---|--------|----------------------|:------:|:-------:|
| 3 | [3-prospect-agent](./examples/3-prospect-agent/README.md) | Prospect research agent — DuckDuckGo search → personalized outreach draft + confidence score | ✅ opt.+Brave | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/3-prospect-agent/prospect_agent_workbook.ipynb) |
| 4 | [4-basic-react-agent](./examples/4-basic-react-agent/README.md) | ReAct agent with conversation memory and PDF retrieval | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/4-basic-react-agent/basic_react_agent_workbook.ipynb) |
| 5 | [5-react-agent-lg](./examples/5-react-agent-lg/README.md) | LangGraph ReAct agent: PDF summarizer + critique loop between two specialist nodes | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/5-react-agent-lg/react_agent_lg_workbook.ipynb) |
| 8 | [8-new-idea-gen](./examples/8-new-idea-gen/README.md) | Two-stage pipeline: parse the free-for-dev list → generate structured, scored ideas | ✅ +Brave | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/8-new-idea-gen/new_idea_gen_workbook.ipynb) |
| 9 | [9-prospect-searx](./examples/9-prospect-searx/README.md) | Prospect agent upgraded to SearXNG (self-hosted, privacy-focused, multi-engine) | ✅ +SearXNG | — |
| 14 | [14-sql-agent](./examples/14-sql-agent/README.md) | ReAct agent over a local SQLite DB using `create_react_agent`; seeds sample data on first run | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/14-sql-agent/sql_workbook.ipynb) |
| 18 | [18-self-reflecting-agent](./examples/18-self-reflecting-agent/README.md) | Reflexion loop — generate answer, critique with structured confidence score, revise until confident or capped | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/18-self-reflecting-agent/reflexion_workbook.ipynb) |
| 20 | [20-code-interpreter](./examples/20-code-interpreter/README.md) | Code interpreter loop — write Python, run in subprocess sandbox, fix on error until max iterations | ✅ | — |
| 35 | [35-plan-execute-agent](./examples/35-plan-execute-agent/README.md) | Plan-Execute — planner emits a typed `Plan` via `with_structured_output`, executor loops each step, synthesizer combines all outputs | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/35-plan-execute-agent/plan_execute_workbook.ipynb) |
| 37 | [37-rewoo-agent](./examples/37-rewoo-agent/README.md) | ReWOO — emit all tool calls upfront as a JSON plan with `$E1/$E2` variable substitution, execute in bulk, synthesize with evidence | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/37-rewoo-agent/rewoo_workbook.ipynb) |
| 46 | [46-tree-of-thoughts](./examples/46-tree-of-thoughts/README.md) | Tree of Thoughts — Send API fans out N branches in parallel, judge LLM scores each, reducer selects best for synthesis | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/46-tree-of-thoughts/tree_of_thoughts_workbook.ipynb) |

</details>

<details>
<summary><strong>Multi-Agent Systems</strong> &nbsp;·&nbsp; 9 examples</summary>

Supervisor routing, parallel subgraphs, map-reduce, agentic RAG, multi-agent debate, supervisor-worker, MCP tool discovery, A2A handoffs, domain-dispatch supervisor.

| # | Folder | What it demonstrates | Keys | Workbook |
|---|--------|----------------------|:------:|:-------:|
| 6 | [6-multi-agent-graph](./examples/6-multi-agent-graph/README.md) | Two-agent graph: `ProductQnA` and `OrdersAgent` routed by a supervisor node | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/6-multi-agent-graph/multi_agent_graph_workbook.ipynb) |
| 19 | [19-multi-agent-notebook](./examples/19-multi-agent-notebook/README.md) | Supervisor/Worker multi-agent pattern — supervisor LLM routes tasks to researcher + writer workers via `add_messages` state | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/19-multi-agent-notebook/multi_agent_workbook.ipynb) |
| 28 | [28-parallel-subgraph](./examples/28-parallel-subgraph/README.md) | Parallel subgraphs — Send API map-reduce: fan out N workers via `Send`, merge with `Annotated[list, operator.add]` | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/28-parallel-subgraph/parallel_subgraph_workbook.ipynb) |
| 30 | [30-agentic-rag](./examples/30-agentic-rag/README.md) | Agentic RAG — retrieval as one tool in a ReAct loop alongside web search and calculator; agent chooses per-turn | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/30-agentic-rag/agentic_rag_workbook.ipynb) |
| 31 | [31-multi-agent-debate](./examples/31-multi-agent-debate/README.md) | Multi-agent debate — two solver agents argue Specialization vs Generalization across rounds; a judge LLM picks the winner | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/31-multi-agent-debate/multi_agent_debate_workbook.ipynb) |
| 43 | [43-supervisor-worker](./examples/43-supervisor-worker/README.md) | Supervisor-worker — `with_structured_output(WorkerRoute)` routes tasks to researcher/summarizer/analyst workers dynamically | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/43-supervisor-worker/supervisor_worker_workbook.ipynb) |
| 44 | [44-mcp-client-agent](./examples/44-mcp-client-agent/README.md) | MCP client agent — dynamic tool discovery via `list_tools()` + `call_tool()` with an in-process mock MCP server | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/44-mcp-client-agent/mcp_client_workbook.ipynb) |
| 45 | [45-a2a-agent-handoff](./examples/45-a2a-agent-handoff/README.md) | A2A agent handoff — typed `AgentTask(BaseModel)` contract between planner and executor agents; structured inter-agent communication | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/45-a2a-agent-handoff/a2a_handoff_workbook.ipynb) |
| 80 | [80-multi-agent-supervisor](./examples/80-multi-agent-supervisor/README.md) | Multi-agent supervisor — LLM classifies domain and dispatches to math, history, or science specialist agents via conditional edges | ✅ | — |

</details>

<details>
<summary><strong>Human-in-the-Loop</strong> &nbsp;·&nbsp; 4 examples</summary>

`interrupt()` / `Command(resume=…)`, edgeless Command routing, SQLite checkpointing across sessions, risk-based auto-approve gates.

| # | Folder | What it demonstrates | Keys | Workbook |
|---|--------|----------------------|:------:|:-------:|
| 11 | [11-hitl-approval](./examples/11-hitl-approval/README.md) | Human-in-the-loop: `interrupt()` pauses the graph mid-run for yes/no approval, `Command(resume=…)` continues from checkpoint | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/11-hitl-approval/hitl_workbook.ipynb) |
| 38 | [38-langgraph-command-pattern](./examples/38-langgraph-command-pattern/README.md) | Command pattern — `Command(goto=route, update={...})` for edgeless dynamic routing; no `add_conditional_edges` needed | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/38-langgraph-command-pattern/command_pattern_workbook.ipynb) |
| 39 | [39-checkpoint-resume](./examples/39-checkpoint-resume/README.md) | Checkpoint & Resume — `SqliteSaver` persists full graph state to SQLite; resume from any `thread_id` across Python sessions | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/39-checkpoint-resume/checkpoint_resume_workbook.ipynb) |
| 79 | [79-interrupt-human-approval](./examples/79-interrupt-human-approval/README.md) | LangGraph interrupt — `interrupt()` pauses graph mid-execution; `Command(resume=approved)` resumes after human review; risk-based auto-approve | ✅ | — |

</details>

<details>
<summary><strong>Structured Output & Safety</strong> &nbsp;·&nbsp; 6 examples</summary>

Pydantic model extraction, PDF parsing with retry, input/output guardrails, Chain-of-Verification, Constitutional AI, prompt injection defense.

| # | Folder | What it demonstrates | Keys | Workbook |
|---|--------|----------------------|:------:|:-------:|
| 13 | [13-structured-output](./examples/13-structured-output/README.md) | Search → extract a validated Pydantic model with `with_structured_output()` | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/13-structured-output/structured_output_workbook.ipynb) |
| 41 | [41-pdf-extraction-agent](./examples/41-pdf-extraction-agent/README.md) | PDF extraction agent — download PDF, extract typed Pydantic schema with `with_structured_output`, retry on validation failure | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/41-pdf-extraction-agent/pdf_extraction_workbook.ipynb) |
| 61 | [61-guardrails-agent](./examples/61-guardrails-agent/README.md) | Guardrails agent — Pydantic `InputGuard` + `OutputGuard` validate user input (PII, off-topic) and LLM output before returning | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/61-guardrails-agent/guardrails_workbook.ipynb) |
| 68 | [68-chain-of-verification](./examples/68-chain-of-verification/README.md) | Chain-of-Verification (CoVe) — generate answer, extract verifiable claims, check each independently, revise failures (Dhuliawala et al. 2023) | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/68-chain-of-verification/chain_of_verification_workbook.ipynb) |
| 69 | [69-constitutional-ai](./examples/69-constitutional-ai/README.md) | Constitutional AI — critique output against written principles, revise to comply, loop until satisfied (Bai et al. 2022) | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/69-constitutional-ai/constitutional_ai_workbook.ipynb) |
| 70 | [70-prompt-injection-defense](./examples/70-prompt-injection-defense/README.md) | Prompt injection defense — classify retrieved chunks for injection risk before passing to the LLM; filter high-risk passages | ✅ | — |

</details>

<details>
<summary><strong>Memory & State</strong> &nbsp;·&nbsp; 3 examples</summary>

Long-term cross-session memory, Mem0 semantic fact extraction, Redis-backed memory with TTL.

| # | Folder | What it demonstrates | Keys | Workbook |
|---|--------|----------------------|:------:|:-------:|
| 36 | [36-long-term-memory](./examples/36-long-term-memory/README.md) | Long-term memory — `InMemoryStore` persists user facts across thread boundaries; retrieve→respond→store loop | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/36-long-term-memory/long_term_memory_workbook.ipynb) |
| 67 | [67-mem0-memory](./examples/67-mem0-memory/README.md) | Mem0 cross-session memory — auto-extract semantic facts that persist across completely separate processes; contrast to LangGraph `InMemoryStore` | ✅ +mem0ai | — |
| 82 | [82-redis-memory](./examples/82-redis-memory/README.md) | Redis memory — Redis-backed cross-session agent memory with `load_history→respond→save_history` nodes and TTL | ✅ +Redis | — |

</details>

<details>
<summary><strong>Evaluation</strong> &nbsp;·&nbsp; 11 examples</summary>

RAGAS, LLM-as-judge, DeepEval (RAG metrics, safety, G-Eval, agentic, conversational, synthesizer), RAGAS evaluation scripts, agent golden datasets, prompt A/B testing.

| # | Folder | What it demonstrates | Keys | Workbook |
|---|--------|----------------------|:------:|:-------:|
| 16 | [16-rag-eval-notebook](./examples/16-rag-eval-notebook/README.md) | RAGAS evaluation workbook — score a RAG pipeline on faithfulness, answer relevance, and context recall | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/16-rag-eval-notebook/rag_eval_workbook.ipynb) |
| 29 | [29-llm-judge-harness](./examples/29-llm-judge-harness/README.md) | LLM-as-judge eval harness — score RAG answers on Relevance, Faithfulness, Completeness with a structured rubric | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/29-llm-judge-harness/llm_judge_workbook.ipynb) |
| 47 | [47-deepeval-rag-metrics](./examples/47-deepeval-rag-metrics/README.md) | DeepEval RAG metrics: Faithfulness, AnswerRelevancy, ContextualPrecision, ContextualRecall, ContextualRelevancy with math definitions and failure injection | ✅ +DeepEval | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/47-deepeval-rag-metrics/deepeval_rag_workbook.ipynb) |
| 48 | [48-deepeval-hallucination-bias](./examples/48-deepeval-hallucination-bias/README.md) | DeepEval safety metrics: HallucinationMetric vs Faithfulness distinction, BiasMetric, ToxicityMetric with deliberate failure injection | ✅ +DeepEval | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/48-deepeval-hallucination-bias/hallucination_bias_workbook.ipynb) |
| 49 | [49-deepeval-geval-custom](./examples/49-deepeval-geval-custom/README.md) | G-Eval custom metrics: `GEval(criteria, evaluation_steps)` for LLM-as-judge + `BaseMetric` subclass for deterministic checks | ✅ +DeepEval | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/49-deepeval-geval-custom/geval_custom_workbook.ipynb) |
| 50 | [50-deepeval-agentic-eval](./examples/50-deepeval-agentic-eval/README.md) | DeepEval agentic metrics: `ToolCorrectnessMetric` with LangGraph tool call extraction from message history | ✅ +DeepEval | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/50-deepeval-agentic-eval/agentic_eval_workbook.ipynb) |
| 51 | [51-deepeval-conversational](./examples/51-deepeval-conversational/README.md) | DeepEval conversational metrics: KnowledgeRetention, ConversationCompleteness, ConversationRelevancy — stateful vs stateless chatbot comparison | ✅ +DeepEval | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/51-deepeval-conversational/conversational_eval_workbook.ipynb) |
| 52 | [52-deepeval-synthesizer](./examples/52-deepeval-synthesizer/README.md) | DeepEval Synthesizer: auto-generate golden datasets with SIMPLE/REASONING/MULTI_HOP/COMPARATIVE strategies; regression testing loop | ✅ +DeepEval | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/52-deepeval-synthesizer/synthesizer_workbook.ipynb) |
| 74 | [74-ragas-evaluation](./examples/74-ragas-evaluation/README.md) | RAGAS evaluation script — build a QA dataset, run `evaluate()` with faithfulness + answer_relevancy; CI-ready | ✅ +ragas | — |
| 76 | [76-agent-evaluation](./examples/76-agent-evaluation/README.md) | Agent evaluation — golden QA dataset, exact match + embedding cosine similarity scoring, per-question PASS/FAIL summary | ✅ | — |
| 78 | [78-prompt-ab-testing](./examples/78-prompt-ab-testing/README.md) | Prompt A/B testing — run two prompt variants on 5 inputs, score by word count, declare winner with comparison table | ✅ | — |

</details>

<details>
<summary><strong>Observability</strong> &nbsp;·&nbsp; 4 examples</summary>

Custom callback handler, token budget manager, LangSmith tracing, Langfuse (self-hosted alternative).

| # | Folder | What it demonstrates | Keys | Workbook |
|---|--------|----------------------|:------:|:-------:|
| 40 | [40-agent-observability](./examples/40-agent-observability/README.md) | Agent observability — `BaseCallbackHandler` records token counts, latency, and errors per LLM call with zero external deps | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/40-agent-observability/observability_workbook.ipynb) |
| 63 | [63-token-budget-manager](./examples/63-token-budget-manager/README.md) | Token budget manager — track token usage per node with `tiktoken`, enforce a per-run budget, short-circuit gracefully when exceeded | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/63-token-budget-manager/token_budget_workbook.ipynb) |
| 73 | [73-langsmith-tracing](./examples/73-langsmith-tracing/README.md) | LangSmith tracing — `@traceable` on each node + `LANGCHAIN_TRACING_V2=true`; inspect the full run tree in the LangSmith UI | ✅ +LangSmith | — |
| 77 | [77-langfuse-observability](./examples/77-langfuse-observability/README.md) | Langfuse observability — self-hostable LLM tracing via `CallbackHandler`; open-source alternative to LangSmith | ✅ +langfuse | — |

</details>

<details>
<summary><strong>Production & Async</strong> &nbsp;·&nbsp; 6 examples</summary>

Semantic routing, web scraping, fully async nodes, batch runners with retries, FastAPI SSE streaming servers.

| # | Folder | What it demonstrates | Keys | Workbook |
|---|--------|----------------------|:------:|:-------:|
| 59 | [59-semantic-router](./examples/59-semantic-router/README.md) | Semantic router — embed incoming queries and route to specialist nodes by cosine similarity; no LLM call needed for routing | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/59-semantic-router/semantic_router_workbook.ipynb) |
| 60 | [60-web-scraper-agent](./examples/60-web-scraper-agent/README.md) | Web scraper agent — fetch a URL, parse with BeautifulSoup, chunk into ephemeral Chroma, answer questions about the page | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/60-web-scraper-agent/web_scraper_workbook.ipynb) |
| 62 | [62-async-langgraph](./examples/62-async-langgraph/README.md) | Async LangGraph — fully async nodes with `ainvoke`/`astream`; `asyncio.gather` inside a node for concurrent tool calls | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/62-async-langgraph/async_langgraph_workbook.ipynb) |
| 72 | [72-batch-agent-runner](./examples/72-batch-agent-runner/README.md) | Batch agent runner — process tasks in parallel batches with `asyncio.gather`, tenacity exponential backoff, tqdm progress tracking | ✅ | — |
| 75 | [75-fastapi-sse-streaming](./examples/75-fastapi-sse-streaming/README.md) | FastAPI SSE — `StreamingResponse` wraps `graph.astream_events()` and formats each token as an SSE `data:` line over HTTP | ✅ +FastAPI | — |
| 81 | [81-streaming-sse-server](./examples/81-streaming-sse-server/README.md) | SSE server — FastAPI `GET /stream?q=` endpoint streams `graph.astream_events()` token-by-token as Server-Sent Events | ✅ +FastAPI | — |

</details>

<details>
<summary><strong>Framework Landscape</strong> &nbsp;·&nbsp; 8 examples</summary>

CrewAI, AutoGen, DSPy, OpenAI Agents SDK, Pydantic AI, LiteLLM, SmolAgents — each contrasted against LangGraph patterns.

| # | Folder | What it demonstrates | Keys | Workbook |
|---|--------|----------------------|:------:|:-------:|
| 15 | [15-crewai-research-crew](./examples/15-crewai-research-crew/README.md) | CrewAI researcher + writer crew — contrasts `Crew`/`Agent`/`Task` primitives against LangGraph's `StateGraph` | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/15-crewai-research-crew/crewai_workbook.ipynb) |
| 21 | [21-autogen-debate](./examples/21-autogen-debate/README.md) | Two-agent AutoGen debate — Proponent vs Opponent argue back and forth for MAX_TURNS exchanges | ✅ | — |
| 23 | [23-crewai-notebook](./examples/23-crewai-notebook/README.md) | CrewAI deep-dive workbook — `Agent`, `Task`, `Crew`, sequential and hierarchical processes | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/23-crewai-notebook/crewai_workbook.ipynb) |
| 33 | [33-dspy-rag](./examples/33-dspy-rag/README.md) | DSPy RAG — declare Signatures instead of hand-crafting prompts; compile with BootstrapFewShot and compare base vs compiled answers | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/33-dspy-rag/dspy_rag_workbook.ipynb) |
| 34 | [34-openai-agents-sdk](./examples/34-openai-agents-sdk/README.md) | OpenAI Agents SDK — triage agent routes to Researcher (with `@tool`) or Writer via `handoff()`; built-in tracing, no LangGraph | ✅ | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/34-openai-agents-sdk/openai_agents_workbook.ipynb) |
| 64 | [64-pydantic-ai](./examples/64-pydantic-ai/README.md) | Pydantic AI — typed research agent with `result_type=ResearchResult`; framework contrast to LangGraph's StateGraph | ✅ +pydantic-ai | — |
| 65 | [65-litellm-multi-provider](./examples/65-litellm-multi-provider/README.md) | LiteLLM — same `completion()` call across OpenAI, Anthropic, and Mistral; fallback chains and cost tracking | ✅ +litellm | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/65-litellm-multi-provider/litellm_workbook.ipynb) |
| 66 | [66-smol-agents](./examples/66-smol-agents/README.md) | SmolAgents (HuggingFace) — `CodeAgent` writes Python as its reasoning trace; contrast to LangGraph nodes/edges | ✅ +smolagents | — |

</details>

---

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then fill in your keys
```

## Keys

`OPENAI_API_KEY` required for all examples (`✅`). A handful need more — see the **Keys** column above:

| Symbol | Means |
|--------|-------|
| `✅` | `OPENAI_API_KEY` only |
| `+Qdrant +Brave` | also needs Qdrant Cloud + Brave Search API |
| `opt.+Brave` | Brave optional, falls back to DuckDuckGo |
| `+Redis` | local Redis (`docker run -p 6379:6379 -d redis`) |
| `+SearXNG` | self-hosted SearXNG (see folder README) |
| `+DeepEval` | `pip install deepeval` (not in default requirements.txt) |
| `+flashrank` | `pip install flashrank` |
| `+litellm` | `pip install litellm` |
| `+smolagents` | `pip install smolagents` |
| `+mem0ai` | `pip install mem0ai` |
| `+pydantic-ai` | `pip install pydantic-ai` |
| `+LangSmith` | `LANGCHAIN_API_KEY` + `LANGCHAIN_TRACING_V2=true` |
| `+langfuse` | `pip install langfuse` + `LANGFUSE_PUBLIC_KEY` / `LANGFUSE_SECRET_KEY` |
| `+FastAPI` | included in requirements.txt (`fastapi`, `uvicorn`) |

Full key list in each folder's README.

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
  ideas.json         # lesson plan (82 examples, all complete)
requirements.txt
```
