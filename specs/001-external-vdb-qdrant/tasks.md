# Tasks for 001-build-a-dedup

T001 [P] Create `examples/2-external-vdb/src/checksum.py`: deterministic checksum util (unit tests)
T002 [P] Create `examples/2-external-vdb/src/dedup.py`: batch lookup helper for Qdrant metadata (unit tests + integration test)
T003 [P] Integrate dedup into `examples/2-external-vdb/main.py` ingestion path (integration test)
T004 [ ] Add contract tests in `specs/001-build-a-dedup/contracts/` simulating existing vector entries
T005 [ ] Add performance smoke test script for batches up to 1000 documents
T006 [ ] Update `specs/001-build-a-dedup/quickstart.md` and README with dedup behavior notes
T007 [ ] Add CI job or workflow snippet to run dedup integration tests against a local Qdrant instance


