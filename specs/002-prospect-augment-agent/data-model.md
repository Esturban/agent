# Data Model: RAG Web-Search CSV Prospecting Agent

## Entities

- ProspectRow
  - id: string (generated UUID for augmented rows)
  - first_name: string
  - last_name: string
  - linkedin_url: string
  - email: string|null
  - company: string
  - position: string
  - connected_on: date
  - generated_message: string|null
  - confidence: float (0.0 - 1.0)
  - source_summary: string (short text summarizing found sources)
  - processed_at: datetime
  - email_read: bool (true if email was read; for this feature always false / not read)

- RunConfig
  - input_path: string
  - output_dir: string
  - date_filter_start: date|null
  - date_filter_end: date|null
  - sample_size: int|null
  - concurrency: int (default 4)

## Validation Rules
- `linkedn_url` must be a valid URL if present
- `confidence` between 0.0 and 1.0
- `connected_on` parsed from `Connected On` column; if unparseable -> mark row as invalid


