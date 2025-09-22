# Research: Dedup check for external vector store ingestion

Decision: Use deterministic content checksum (SHA256) computed from normalized text
as the canonical dedup key. Use Qdrant payload metadata field `content_checksum`.

Rationale: Content checksum is language- and embedding-agnostic, cheap to compute,
and deterministic, making it ideal for idempotent ingestion. Embedding similarity
is not used for dedup because it is probabilistic and may produce false negatives.

Alternatives considered:
- Use embedding similarity + threshold to dedup (rejected: imprecise, costly).
- Use source-provided stable IDs (rejected: not always available across datasets).

Edge considerations:
- Ensure metadata fields are written atomically with vector upserts when possible.
- Qdrant filter capabilities differ across versions; use `scroll` or point lookups
  as a fallback and batch requests to minimize roundtrips.


