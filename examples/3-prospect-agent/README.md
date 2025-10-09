# Prospect Agent Example

This example demonstrates a minimal CLI using the Prospect Augment Agent. Place a `Connections.csv` in the repository `data/` folder or use the provided sample CSV in `examples/3-prospect-agent/data/sample_connections.csv`.

Run the example from this directory:

```bash
python main.py --input examples/3-prospect-agent/data/sample_connections.csv
```

Output will be written to `data/aug/connections_aug_<timestamp>.csv` relative to the repo root.

Note: This tool continues to grow from a basic example. Almost worth duplicating since the original example was written to do some research. But now, this does research and creates a draft message with confidence.


# Inspiration
https://www.pinecone.io/learn/langgraph-research-agent/