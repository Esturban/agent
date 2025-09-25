# Data Model: Dedup ingestion

Entities:

- Document
  - id: string (doc_id, derived from checksum)
  - source: string
  - raw_text: text
  - normalized_text: text
  - content_checksum: string (SHA256)

- EmbeddingEntry
  - vector: float[]
  - metadata:
    - doc_id: string
    - content_checksum: string
    - source: string
    - ingested_at: timestamp


