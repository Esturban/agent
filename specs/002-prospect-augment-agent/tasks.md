# Tasks: Prospect Augment Agent (TDD-first, minimal-bloat)

Feature: Prospect Augment Agent
Location: `/Users/EVA/Desktop/eva/03_development/_dev/repos/4_agents/py/agent`

Notes:
- Keep code minimal and local-first. Brave search will be implemented as a community tool module (non-MCP) under `examples/3-prospect-agent/src/tools/` following the `@2-external-vdb` approach.
- This feature DOES NOT rely on an MCP sequential thinker; the orchestrator is a single-search flow (person -> company positive news) per spec.
- Output: augmented CSV written to `data/aug/connections_aug_<timestamp>.csv`.
- Tests are TDD-first: write failing tests, then implement.

T001 Setup: environment & dependencies [P]
- Files: `/Users/EVA/Desktop/eva/03_development/_dev/repos/4_agents/py/agent/requirements.txt`
- Action: Create virtualenv and install pinned deps; ensure `langgraph==0.6.7`, `langchain==0.3.27`, `pandas==2.3.2`, `typer` are available. Add `langchain-mcp-adapters` only if needed later.
- Command examples:
  - python -m venv .venv && source .venv/bin/activate
  - pip install -r requirements.txt
- Dependency: none
 - Status: [X] Completed

T002 Data model: create `ProspectRow` dataclass and validation [P]
- Files to add: `src/models/prospect.py`, tests: `tests/unit/test_prospect_model.py`
- Action: Implement `ProspectRow` dataclass with fields from `specs/002-prospect-augment-agent/data-model.md` and simple validators (URL check, date parse). Write unit tests first (invalid date, missing required fields).
- Command examples:
  - pytest tests/unit/test_prospect_model.py
- Depends on: T001
 - Status: [X] Completed

T003 CSV loader: implement CSV loader (pandas) and parsing tests [P]
- Files: `src/services/csv_loader.py`, tests: `tests/unit/test_csv_loader.py`
- Action: Write tests that assert loader raises on missing columns and correctly parses `Connected On` into datetime. Implement minimal loader that yields `ProspectRow` objects.
- Command examples:
  - pytest tests/unit/test_csv_loader.py
- Depends on: T002
 - Status: [X] Completed
T004 CLI contract tests (failing) [P]
- Files: `specs/002-prospect-augment-agent/contracts/cli_contract.md`, tests: `tests/contract/test_cli_contract.py`
- Action: Write a contract test that runs CLI with `--input` pointing to small example CSV and asserts output file is created with expected headers. Use tmpdir and run CLI entrypoint `src/cli/prospect_agent.py`.
- Command examples:
  - pytest tests/contract/test_cli_contract.py
 - Depends on: T001, T002, T003
 - Status: [X] Completed

T005 Implement CLI scaffold (src) (sequential)
- Files: `src/cli/prospect_agent.py` (root-level implementation), tests referenced by T004
- Action: Implement CLI per `specs/002-prospect-augment-agent/contracts/cli_contract.md` and `quickstart.md`. CLI must default to `data/Connections.csv` and write to `data/aug/`.
- Command examples:
  - python -m src.cli.prospect_agent --input data/Connections.csv --output data/aug/
 - Depends on: T001, T002, T003, T004
 - Status: [X] Completed

T006 Brave tool: implement community tool adapter (langchain-community) [P]
- Files: `examples/3-prospect-agent/src/tools/brave_search.py`, tests: `examples/3-prospect-agent/tests/unit/test_brave_tool.py`
- Action: Use the LangChain community `BraveSearch` tool (package: `langchain_community.tools`) — do NOT implement scraping. Implement a thin adapter that:
  - Instantiates `BraveSearch.from_api_key(api_key, search_kwargs={"count": 3})` and calls `.run(query)`
  - Returns the raw search results to the caller (string or tool-specific object)
  - Exposes a simple `search_tool(query: str, brave_key: Optional[str] = None) -> str` signature
  - Implements retry/backoff for transient failures using exponential backoff with full jitter (max_retries=3, initial_delay=0.5s, max_delay=8s)
- Tests:
  - Unit test asserting missing API key raises a clear error
  - Unit test injecting a fake `BraveSearch` double and asserting adapter returns expected results
  - Unit test mocking transient errors to assert backoff is attempted
- Note: Keep interface minimal so the orchestrator can call it synchronously. This task is complete in example folder.
- Depends on: T001
- Status: [X] Completed
 - Note: Keep interface minimal so the orchestrator can call it synchronously. This task is complete in example folder.
 - Depends on: T001
 - Status: [X] Completed

T007 Sequential thinker: simplified single-search orchestrator (no MCP) [P]
- Files: `examples/3-prospect-agent/src/orchestrator/langgraph_runner.py`, tests: `examples/3-prospect-agent/tests/unit/test_langgraph_runner.py`
- Action: Implement an MCP-backed sequential orchestrator that uses the repo's Brave adapter and an MCP `sequentialthinking` tool (do NOT reimplement LLM reasoning locally):
  - Implement a simplified single-search orchestrator that:
    - Accepts a prospect context (ProspectRow fields except email) and performs ONE prioritized web search:
      1) Person search: `"{first_name} {last_name} {company}"`
      2) If no useful results: Company positive-news search `"{company} positive news"`
    - Aggregate up to 3 structured facts (title, snippet, url) for downstream use
    - Emit structured logs for the search call (query, prospect id, duration_ms, success/failure)
Tests to add:
  - Unit test that injects a fake Brave adapter and asserts the orchestrator returns facts and source_summary when person search yields results and when fallback triggers.
  - Test that verifies emails are not included in prompts and no PII is sent to any search or model input (assert context used for query excludes email).
 - Depends on: T001, T006
 - Status: [X] Completed


T008 Message generator: prompt template + tests [P]
- Files: `examples/3-prospect-agent/src/services/message_generator.py`, tests: `examples/3-prospect-agent/tests/unit/test_message_generator.py`
- Action: Implement a concise message generator that consumes Prospect context and structured facts and returns a professional, concise, open-ended outreach message. Enforce limits: <= 3 sentences, <= 45 words. Provide `generate_message(prospect, facts, llm_invoke=None)` with an injectable `llm_invoke` for testing.
- Tests:
  - Unit test asserting output <= 45 words and includes a question or sentence ending.
  - Additional tests will mock LLM provider when integrated.
- Depends on: T001, T007
- Status: [X] Completed

T009 Confidence scorer: implement and test [P]
- Files: `examples/3-prospect-agent/src/services/confidence.py`, tests: `examples/3-prospect-agent/tests/unit/test_confidence.py`
- Action: Implement a simple, deterministic confidence heuristic:
  - If no facts → 0.0
  - base = min(1.0, len(facts)/3)
  - boost +0.2 if any fact mentions the prospect company/position
  - clamp to [0.0,1.0], round to 3 decimals
- Tests:
  - Unit test for no facts
  - Unit test for base + boost behavior
- Depends on: T007
- Status: [X] Completed

T010 Pipeline service: integrate loader, runner, generator, confidence, writer (sequential)
- Files: `examples/3-prospect-agent/src/services/pipeline.py`, tests: `examples/3-prospect-agent/tests/integration/test_pipeline_end2end.py`
- Action: TDD: write integration test that uses mocked brave_search and LLM to run the pipeline on a sample CSV and assert output CSV includes `generated_message`, `confidence`, `source_summary`, `processed_at` and that messages conform to the word/sentence limits.
- Depends on: T005, T006, T007, T008, T009
- Status: [X] Completed

T011 Output writer: write to `data/aug/connections_aug_<timestamp>.csv` and report summary (sequential)
- Files: `examples/3-prospect-agent/src/services/output_writer.py` (used by pipeline), tests: `examples/3-prospect-agent/tests/unit/test_output_writer.py`
- Action: Implement CSV writer that accepts an iterable of ProspectRow instances and writes a timestamped CSV to `data/aug/`. Include a small summary report of counts and average confidence returned to caller.
- Tests:
  - Unit test ensures file is created, headers present, and contains expected rows.
- Depends on: T010
- Status: [X] Completed

T012 Integration & contract tests (end-to-end) [P]
- Files: `examples/3-prospect-agent/tests/integration/test_pipeline_end2end.py`, `examples/3-prospect-agent/tests/contract/test_cli_contract.py`
- Action: Ensure end-to-end tests run with mocked network (respx/vcr) and validate CSV output and summary JSON. These tests should run in CI or locally and be fast; use small sample CSV (<=1MB).
- Command:
  - pytest examples/3-prospect-agent/tests/integration -q
  - pytest examples/3-prospect-agent/tests/contract -q
- Depends on: T010, T011
- Status: [X] Completed

T013 Examples & docs (examples/3-prospect-agent) [P]
- Files: `examples/3-prospect-agent/data/sample_connections.csv`, `examples/3-prospect-agent/README.md` (update)
- Action: Add a small sample CSV (~10 rows), update example README with exact run command, and show expected output file path.
- Depends on: T005, T011
- Status: [X] Completed

T014 Polish: typing, linting, CI, and cleanup [P]
- Files: repo root lint config, add `pre-commit` if desired
- Action: Run linters, type checks, fix issues; update quickstart and top-level README. Ensure all tests pass.
- Command: tox -e py or flake8/ruff + pytest
- Depends on: all tasks
- Status: [ ] Pending

Parallel groups examples:
- Group A [P]: T002, T003, T006 (models, loader, brave tool) can be developed in parallel
- Group B [P]: T008, T009 (generator & confidence) can be developed in parallel after T007 is stubbed

Execution agents (developer commands):
- To run unit tests for a component:
  - pytest tests/unit/test_csv_loader.py -q
- To run contract test for CLI:
  - pytest tests/contract/test_cli_contract.py -q


### Clarifying Questions (for tasks refinement)
1. Should the orchestrator prefer an MCP-hosted `sequential_thinker` tool name exactly `sequential_thinker`, or should it discover available tool names dynamically? (recommend fixed name `sequential_thinker`) It is called sequentialthinking and it's a docker run command that can be locally run
2. For BraveSearch results, do you prefer raw text concatenation, a structured list of (title, snippet, url), or both exposed from the adapter? (recommend structured list) structured list that can be parsed and used in the personalized message
3. Confirm stopping criteria: **4** thoughts per prospect is final? (spec currently says 4) 4 thoughts
4. PII policy: should email addresses be included in augmented CSV or redacted? (spec default: include but do not read email contents) NEVER pass the email to the model
5. Logging/observability: should each tool call emit structured logs (yes/no)? (recommend yes) yes
6. Should the orchestrator enforce a maximum number of thoughts per prospect? (spec currently says 4)