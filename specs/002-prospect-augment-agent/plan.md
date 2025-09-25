# Implementation Plan: Prospect Augment Agent

**Branch**: `002-prospect-augment-agent` | **Date**: 2025-09-23 | **Spec**: `/Users/EVA/Desktop/eva/03_development/_dev/repos/4_agents/py/agent/specs/002-prospect-augment-agent/spec.md`
**Input**: Feature specification at `/Users/EVA/Desktop/eva/03_development/_dev/repos/4_agents/py/agent/specs/002-prospect-augment-agent/spec.md`

## Summary
Create a minimal, easy-to-follow implementation plan for a CLI RAG agent that ingests a LinkedIn export CSV from `data/`, enriches each row via Brave web search and a sequential-thinking MCP tool (LangGraph), generates a personalized open-ended outreach message with a confidence score, and writes a timestamped augmented CSV to `outputs/`.

## Technical Context
**Language/Version**: Python 3.11  
**Primary Dependencies**: `langgraph==0.6.7`, `langchain==0.3.27`, `langchain-mcp-adapters`, `pandas==2.3.2`, `typer` for CLI  
**Storage**: File-based CSV IO (default folders: `data/` and `outputs/`)  
**Testing**: `pytest` with contract/unit/integration split; network calls mocked  
**Target Platform**: Linux/macOS CLI  
**Project Type**: Single Python CLI project under `src/cli/`  
**Performance Goals**: Batch processing with concurrency default 4; no strict p95 for MVP  
**Constraints**: Respect MCP tool rate limits; avoid storing extra PII  
**Scale/Scope**: MVP targets CSVs up to 50k rows (sampling/batching recommended)

## Constitution Check (initial)
- Code Quality: MUST include typing.  
- Testing Standards: Contract and unit tests required.  
- UX Consistency: CLI contract exists.  
- Performance: No strict targets for MVP.

## One-shot (YOLO) Sequential Plan for a Junior Developer
1. Environment & repo prep
   - Ensure Python 3.11 and `pip install -r requirements.txt`. Add `langchain-mcp-adapters` if missing.
2. CLI scaffold
   - Add `src/cli/prospect_agent.py` using `typer` with flags: `--input`, `--output`, `--date-start`, `--date-end`, `--sample`, `--concurrency`.
3. CSV loader & validator
   - Implement `csv_loader` with pandas and a `ProspectRow` dataclass. Unit tests for parsing.
4. Search tool integration (Brave as community tool + MCP for sequential thinking)
   - Implement Brave as a pluggable community tool module `src/tools/brave_search.py` (non-MCP). Implement MCP adapter only for the sequential-thinking tool (MCP-backed reasoning) in `src/tools/mcp_adapters.py` to bind the sequential thinker when configured. Top-3 results per query. Exponential backoff with full jitter and max_retries=3.
5. Sequential thinking orchestration (LangGraph)
   - Build a small `StateGraph` with `call_model` and `tools` nodes. Use `ToolNode` bound to MCP tools, iterate until stopping criteria.
6. Message generation and confidence
   - Prompt template for open-ended outreach. Confidence heuristic: supported_assertions/total_assertions.
7. Output writer & summary
   - Write timestamped CSV with added columns; output JSON summary with stats.
8. Tests & quickstart
   - Contract tests for CLI, unit tests for loader/confidence, integration test mocking MCP.
9. Review & polish
   - Type annotations, linters, README updates, env var docs.

## Loading `data/` from sibling project folder
CLI default should resolve repo root and use `repo_root / 'data' / 'Connections.csv'`, but accept `--input` override. Use `Path(__file__).resolve().parents[3]` to compute repo root.

## LangGraph / LangChain + MCP integration notes
- Use `langchain-mcp-adapters.MultiServerMCPClient` to get tools and pass them into `create_react_agent` or bind them to the LLM via `model.bind_tools(tools)`.
- Install `langchain-mcp-adapters` and pin version compatible with `langgraph==0.6.7`.

## Compatibility checks
- `requirements.txt` contains `langgraph==0.6.7` and `langchain==0.3.27`. In Phase 1, run a virtualenv test to ensure `langchain-mcp-adapters` installs without dependency conflicts.

## Clarifying questions (answer these to finalise Phase 2 tasks)
1. What stopping criteria for the sequential thinker? (max tool calls per prospect, min corroborated facts, or timeout)
2. PII policy: redact emails in logs/outputs or keep them in augmented CSV?
3. Disambiguation preference when multiple profiles match (prefer LinkedIn URL if present?)
4. Is Brave search the only external web source for Phase 1 or include others (Bing/Google)?
5. Typical CSV size for runs (sample 50, batch 5k, large 50k)?
6. Brand voice for outreach messages (formal/casual/concise)?
7. Output location policy: overwrite `data/` or always write to `outputs/`?

Answering these lets me generate `tasks.md` with ordered, test-driven tasks and ready-to-run test templates.


