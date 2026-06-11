# Contributing

Thanks for your interest. This repo is a collection of small, self-contained
LangGraph / agent examples. Each one should be readable in a couple of minutes.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt   # ruff, etc.
```

Add your `OPENAI_API_KEY` (and any example-specific keys) to a local `.env`.

Optionally enable the git hooks so lint/format run on every commit:

```bash
pip install pre-commit && pre-commit install
```

## Adding an example

Examples live in `examples/{number-slug}/` and follow this shape:

```
examples/{slug}/
├── main.py          # entry point, loads .env, has an if __name__ == "__main__" block
├── README.md        # what it does + how to run
└── src/
    ├── __init__.py
    ├── workflow.py  # create_workflow()
    └── tools.py     # tool definitions
```

Keep it simple and focused — small files, no speculative abstractions, and reuse
the dependencies already in `requirements.txt`.

## Lint & format

The CI gate runs ruff. Before opening a PR:

```bash
make check   # ruff check + ruff format --check (read-only, same as CI)
make fix     # auto-fix lint issues and reformat
```

## Data & secrets

Never commit secrets or personal data. `.env` and the `data/` directory are
gitignored — keep real connection exports, prospect lists, and API keys there.

## Pull requests

- Branch off `dev` (e.g. `feat/my-example`); open the PR against `dev`.
- Use a [conventional commit](https://www.conventionalcommits.org/) title,
  e.g. `feat(examples/27-self-rag): add workflow`.
- Make sure `make check` passes and fill in the PR template checklist.
