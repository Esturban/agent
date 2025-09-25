# Feature Specification: Dedup check for external vector store ingestion

**Feature Branch**: `001-build-a-dedup`  
**Created**: 2025-09-22  
**Status**: Draft  
**Input**: Build a dedup check for external vector store: add a simple pre-fill verification
in `examples/2-external-vdb/main.py` to check whether document embeddings already exist
in the external vector DB and skip re-indexing if present. Target: quality RAG example
using external vector DB; spec should document behavior, tests, performance expectations,
and required tasks.

## Execution Flow (main)
```
1. Parse user description from Input
2. Identify target example folder: `examples/2-external-vdb`
3. Define ingestion flow and where to insert dedup check (before `from_documents` call)
4. Design dedup verification strategy: fingerprint documents, query vector DB metadata
5. If documents already present (by checksum/doc_id), skip indexing for those items
6. Produce failing tests: unit for fingerprinting, integration test that simulates
   existing entries in an external vector store and verifies skip behavior
7. Implement, run CI checks, and validate performance targets
```

---

## ⚡ Quick Guidelines
- Focus on preventing duplicate embeddings in the external vector DB by verifying
  document presence before re-indexing.
- Keep the dedup check lightweight and deterministic: use stable content fingerprinting
  and vector-store metadata lookup rather than embedding similarity.
- Preserve the RAG example's retriever behavior: dedup is an ingestion optimization only.

### Section Requirements
- **Mandatory sections**: User Scenarios & Testing, Requirements, Key Entities, Review & Acceptance

### For AI Generation
1. Mark all ambiguities with [NEEDS CLARIFICATION] (e.g., preferred fingerprint algorithm).
2. Do not hardcode production credentials or environment-specific assumptions.

---

## User Scenarios & Testing *(mandatory)*

### Primary User Story
As a developer maintaining the RAG example, I want the ingestion process to detect and
skip documents already stored in the external vector DB so that re-running ingestion does
not create duplicate embeddings or waste credits/time.

### Acceptance Scenarios
1. Given an empty collection, when ingesting N new documents, then all N documents are
   indexed and stored with metadata including `doc_id` and `content_checksum`.
2. Given a collection that already contains a document with the same `content_checksum`,
   when ingesting the same document, then the ingestion process skips indexing that
   document and logs that it was skipped.
3. Given a partial overlap between incoming and existing documents, when ingesting,
   then only the new documents are indexed; the skipped count is reported.
4. Given a document whose content changed (different checksum), when ingesting,
   then the document is re-indexed and metadata updated.

### Edge Cases
- Documents with identical normalized content but different source IDs: dedup MUST rely on
  content checksum, not external source ID, unless a stable `doc_id` policy is defined.
- If the vector store is unreachable, ingestion MUST fail fast with an explicit error and
  leave no partial state (or document the expected repair/migration step).
- Large batches: ensure dedup check supports batched metadata queries to avoid O(N^2).

## Requirements *(mandatory)*

### Functional Requirements
- **FR-001**: The system MUST compute a deterministic `content_checksum` (e.g., SHA256 of
  normalized text) for each document prior to embedding.
- **FR-002**: The ingestion flow MUST query the external vector DB for existing items by
  `content_checksum` metadata and determine which documents are already present.
- **FR-003**: The ingestion flow MUST skip indexing documents found in the external DB and
  proceed to index only missing documents.
- **FR-004**: For each indexed document, the system MUST store metadata fields: `doc_id`,
  `content_checksum`, `source`, and `ingested_at`.
- **FR-005**: The ingestion process MUST log counts: total input, skipped, newly indexed,
  and any failures, with correlation IDs for debugging.
- **FR-006**: The dedup check implementation MUST support batch queries to the vector DB
  (e.g., lookup by list of checksums) to avoid per-document network roundtrips.

### Performance Requirements
- **PR-001**: For ingestion batches up to 1000 documents, the dedup verification step
  (checksum computation + batched metadata lookup) SHOULD complete with p95 < 5s in CI
  with a local/simulated vector DB; production SLAs TBD per deployment profile.
- **PR-002**: The dedup step MUST not increase peak memory usage by more than 2x the
  baseline ingestion memory footprint for the same batch size.

## Key Entities *(include if feature involves data)*
- **Document**: { source, raw_text, normalized_text, content_checksum, doc_id }
- **EmbeddingEntry**: { vector, metadata: { doc_id, content_checksum, source, ingested_at } }
- **VectorCollection**: external vector DB collection name where embeddings live

---

## Review & Acceptance Checklist
*GATE: Automated checks run during main() execution*

### Content Quality
- [ ] Spec focuses on WHAT and WHY (no implementation details beyond the required behavior)

### Constitution Alignment
- [ ] Spec lists required tests (unit/integration/contract) and their acceptance criteria
- [ ] Spec includes performance targets and validation approach when applicable
- [ ] Spec documents expected error shapes and user-facing behaviors for new interfaces

### Requirement Completeness
- [ ] No [NEEDS CLARIFICATION] markers remain
- [ ] Requirements are testable and unambiguous
- [ ] Success criteria are measurable

---

## Execution Status
*Updated by main() during processing*

- [ ] User description parsed
- [ ] Key concepts extracted
- [ ] Ambiguities marked
- [ ] User scenarios defined
- [ ] Requirements generated
- [ ] Entities identified
- [ ] Review checklist passed

---

## Suggested Tasks (Phase 2 / tasks.md inputs)
- T001 Create `utils/checksum.py`: deterministic content normalization + SHA256 checksum function (unit tests)
- T002 Add `ingest/dedup_check.py`: function to batch query vector DB metadata by checksum and return missing docs (unit + integration tests)
- T003 Integrate dedup_check into `examples/2-external-vdb/main.py` ingestion path; ensure metadata is written on index (integration test)
- T004 Add contract tests that simulate an external vector DB with pre-existing entries and validate skip behavior
- T005 Add performance smoke test for batches up to 1000 documents (benchmark script)
- T006 Update docs/quickstart.md for `2-external-vdb` describing dedup behavior and how to reset the collection


