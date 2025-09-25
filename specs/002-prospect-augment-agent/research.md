# Research: RAG Web-Search CSV Prospecting Agent

## Goal
Resolve open questions necessary for a junior developer to implement the feature: how to integrate Brave web search via MCP, how to use LangGraph within the current repo constraints, how to structure CLI input/output, and how to compute confidence scores.

## Decisions & Rationale

- Decision: Use Brave web search via MCP Brave Search tool for external web queries.
  Rationale: Initially considered using Brave via MCP; user prefers Brave as a local/community "tool" integrated directly (similar to the `@2-multi-tool-rag` example). The plan will treat Brave as a pluggable tool module rather than an external MCP server.

- Decision: Use LangGraph for orchestration where longer-running, stateful sequential thinking is needed.
  Rationale: LangGraph offers durable execution and is compatible with the project's agent patterns; selected Context7 library `/langchain-ai/langgraph`.

- Decision: Keep implementation as a CLI under `src/cli/prospect_agent.py` with config read from `data/` by default.
  Rationale: Simplicity for initial MVP and matches repo style.

## Unknowns (resolved)

- Retry/backoff strategy when Brave search rate-limits: Implement exponential backoff with full jitter. Parameters: max_retries=3, initial_delay=0.5s, max_delay=8s. On final failure, mark the row as requiring manual review and continue to next row. Log rate-limit events with counts.
- Disambiguation strategy for identical names: Prefer CSV `URL` if present. Otherwise include `company` and `position` in the search query and prefer results matching both. If ambiguity remains after search, set `confidence=0.0` and flag row for manual review.
- Expected CSV encodings/locales: Default to UTF-8; fallback to `windows-1252` if decode errors occur. Parse dates using `dateutil.parser.parse` (dayfirst=False) and provide a CLI flag `--date-format` to override.

## Implementation notes for developer
- Read `data/Connections.csv` or user-provided path; validate columns: `First Name,Last Name,URL,Email Address,Company,Position,Connected On`.
- Use pandas for CSV reading and filtering; use `sample(n=...)` for sampling; filter by parsed `Connected On` dates.
- For each row, call MCP Brave Search with query: `"{first} {last} {company} {position}"` and parse top 3 results.
- Use an MCP sequential thinking tool to iterate on search queries and gather more context until stopping criteria met (e.g., 3 good matches or timeout).
 - Use a sequential-thinking orchestration (LangGraph StateGraph) to iterate on search queries and gather more context until stopping criteria met: maximum of 4-5 thoughts per prospect.
- Generate message via an LLM prompt template and compute confidence via heuristic: fraction of statements substantiated by sources and presence of role/company-specific facts.

## Research artifacts to create next
- `data-model.md` (Phase 1)
- `quickstart.md` (Phase 1)
- `contracts/cli_contract.md` (Phase 1)


