# Prospect Agent Example

This example demonstrates a minimal CLI using the Prospect Augment Agent. Place a `Connections.csv` in the repository `data/` folder or use the provided sample CSV in `examples/3-prospect-agent/data/sample_connections.csv`.

Run the example from this directory:

```bash
python main.py --input examples/3-prospect-agent/data/sample_connections.csv
```

Output will be written to `data/aug/connections_aug_<timestamp>.csv` relative to the repo root.

Note: This tool continues to grow from a basic example. Almost worth duplicating since the original example was written to do some research. But now, this does research and creates a draft message with confidence.


CSV output change: `source_summary` now contains a semicolon-separated list of the top 2–3 URLs the researcher found (replacing the copywriter's free-text source summary). This keeps CSV rows compact and ensures URLs are machine-parseable.

Behavior details:
- If the researcher found no recent URLs, `source_summary` will contain: `No recent information found for this prospect.`
- At most 3 URLs are included, separated by `; ` (semicolon + space) to avoid breaking CSV commas.

# Inspiration
https://www.pinecone.io/learn/langgraph-research-agent/