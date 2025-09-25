# Quickstart: Prospect Augment Agent (CLI)

Prerequisites:
- Python 3.11+
- Install dependencies: `pip install -r requirements.txt`

Usage:

1. Place your CSV in the project `data/` folder, e.g. `data/Connections.csv`.
2. Run the CLI (example):

```bash
python -m src.cli.prospect_agent --input data/Connections.csv --output outputs/ --sample 50
```

Options:
- `--input`: path to CSV (default `data/Connections.csv`)
- `--output`: directory to write augmented CSV (default `outputs/`)
- `--date-start`, `--date-end`: filter by `Connected On` dates
- `--sample`: process a random sample of rows

Output:
- `outputs/connections_augmented_<timestamp>.csv` with added columns `generated_message`, `confidence`, `source_summary`


