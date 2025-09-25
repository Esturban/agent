---
approved: true
approved_by: "Esturban"
approved_at: "2025-09-23T20:12:00Z"
spec_version: 1
---

# Feature Specification: RAG Web-Search CSV Prospecting Agent

**Feature Branch**: `002-prospect-augment-agent`  
**Created**: 2025-09-23  
**Status**: Draft  
**Input**: User description: "we wanna make a new rag agent that will actually search the Internet and use brave web search to search about any relevant information regarding a prospect pass through in a CSV..."

## Execution Flow (main)
```
1. User invokes CLI with path to a CSV of LinkedIn connections (defaults to `data/`)
2. System validates CSV format and required columns (name, title, company, connected_at, linkedin_url)
3. For each row (or filtered sample):
   a. Run Brave web search for the prospect (name + company + title)
   b. Use sequential thinking tool (MCP-backed reasoning) to structure search and decide when enough evidence exists (max 4 thoughts)
   c. Extract relevant facts (company news, role responsibilities, recent posts, public profiles)
   d. Generate a personalized, open-ended outreach message and a confidence score (0.0 - 1.0)
4. Append generated message, confidence, and summary of sources to the row
5. Write augmented CSV to `data/aug/` with timestamped filename `connections_aug_<timestamp>.csv`
6. Exit with a summary report (counts, average confidence, rows needing manual review)
```

---

## ⚡ Quick Guidelines
- ✅ Focus on WHAT users need and WHY
- ❌ Avoid implementation details beyond required tool choices for clarity
- 👥 Intended user: Sales or growth operator with CSV of LinkedIn connections

### Section Requirements
- **Mandatory sections**: Completed below

## User Scenarios & Testing *(mandatory)*

### Primary User Story
As a sales operator, I want to feed a CSV of LinkedIn connections into a CLI tool so that the tool searches the web for context and generates personalized, open-ended outreach messages with confidence scores saved back to a timestamped CSV.

### Acceptance Scenarios
1. **Given** a valid CSV and default options, **When** the CLI runs, **Then** it produces an augmented CSV in `data/aug/` with generated messages and confidence scores for each row.
2. **Given** a filter (date range or sample size), **When** the CLI runs, **Then** only the filtered rows are processed and exported.
3. **Given** incomplete CSV rows (missing name/company), **When** the CLI runs, **Then** those rows are written with an empty message and confidence=0.0 and reported in the summary.

### Edge Cases
- What happens when Brave search rate limits occur? Retry/backoff strategy: implement exponential backoff with full-jitter, max_retries=3, initial_delay=0.5s, max_delay=8s. On repeated failures, mark row as needing manual review and continue. Log rate-limit events.
- How to handle rows with identical names? Disambiguation preference: prefer `URL` from the CSV if present. If missing, include company + position in search terms and prefer results that match both company and title. If ambiguity remains, flag the row for manual review and set confidence=0.0.
-- CSV encoding or locale issues: default to UTF-8; attempt fallback to `windows-1252` if UTF-8 decode fails. Treat dates using `dateutil.parser.parse` with dayfirst=False by default; provide CLI flag `--date-format` for override.

## Clarifications
#### Session 2025-09-23
- Q1: Orchestrator MCP tool name → A: `sequentialthinking` (the sequential thinker runs as a dockerized MCP service that can be run locally)
- Q2: BraveSearch result format → A: **structured list** (title, snippet, url) for downstream parsing and message generation
- Q3: Stopping criteria → A: **4** thoughts per prospect (enforced)
- Q4: PII / email handling → A: **NEVER** pass email addresses or email content to any LLM or tool; redact or omit before model input
- Q5: Logging / observability → A: **Yes** — emit structured logs for every tool call including tool name, prospect id, duration, and success/failure

Edge case additions based on clarifications:
- PII/email handling: Do not send email addresses to models; redact or omit them before any model input. Emails may remain in CSV output but must not be included in prompts.

## Requirements *(mandatory)*

### Functional Requirements
- **FR-001**: System MUST accept a path to a CSV file and validate required columns
- **FR-002**: System MUST allow filtering by connected date range and sampling size
- **FR-003**: System MUST perform Brave web searches for each prospect and collect source snippets
- **FR-004**: System MUST perform a single prioritized web search to gather context: search the person first (name + company + position); if person search yields insufficient context, search recent positive news about the company. Do NOT send email addresses to models.
- **FR-005**: System MUST generate a personalized open-ended outreach message per prospect
- **FR-006**: System MUST compute and store a confidence metric between 0.0 and 1.0 for each generated message
- **FR-007**: System MUST write an augmented CSV to `outputs/` with a timestamped filename
- **FR-008**: System MUST produce a summary report at completion including counts and average confidence

### Key Entities
- **ProspectRow**: Represents a single CSV row with attributes: name, title, company, connected_at, linkedin_url, generated_message, confidence, source_summary
- **RunConfig**: CLI options: input_path, output_dir, date_filter_start, date_filter_end, sample_size, concurrency

---

## Review & Acceptance Checklist

### Content Quality
- [x] No deep implementation code
- [x] Focused on user value
- [x] Mandatory sections completed

### Constitution Alignment
- [ ] Includes tests and acceptance criteria pointers

### Requirement Completeness
- [ ] All [NEEDS CLARIFICATION] markers resolved

---

## Execution Status

- [x] User description parsed
- [x] Key concepts extracted
- [x] Ambiguities marked
- [x] User scenarios defined
- [x] Requirements generated
- [x] Entities identified
- [ ] Review checklist passed

---

## Tasks
- Draft spec for RAG web-search CSV agent (in_progress)
- Create acceptance criteria and test scenarios for the spec (pending)
- Add example CSV and README usage to examples/ (pending)

## References
- Brave web search (via MCP Brave Search) for web queries
- MCP sequential thinking tool for structured reasoning

## Acceptance Criteria
- Produces augmented CSV with generated_message and confidence columns for valid rows
- Provides a CLI option to filter by date and sample size
- Exports output to `outputs/` with a timestamped filename
- Rows missing required fields are reported and omitted from generation (message empty, confidence=0)


