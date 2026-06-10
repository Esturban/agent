# 3-prospect-agent

Prospect research agent: reads LinkedIn connections from a CSV, searches the web for each person, and writes a personalized outreach message with a confidence score.

**Keys:** `OPENAI_API_KEY` · optional `BRAVE_API_KEY` · optional `OPENROUTER_API_KEY`
**Files:** `data/Connections.csv` — a sample is at `examples/3-prospect-agent/data/sample_connections.csv`

```bash
python examples/3-prospect-agent/main.py --input examples/3-prospect-agent/data/sample_connections.csv
```

Output is written to `data/aug/connections_aug_<timestamp>.csv`. The `source_summary` column contains up to 3 semicolon-separated URLs from the researcher.