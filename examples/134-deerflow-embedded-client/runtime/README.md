# DeerFlow Runtime Setup

DeerFlow is not on PyPI. Run it as a separate service alongside this repo.

## Bootstrap (one-time)

```bash
# Clone DeerFlow into a sibling directory
git clone https://github.com/bytedance/deer-flow ../deer-flow
cd ../deer-flow

# Python 3.12+ required
python -m venv .venv && source .venv/bin/activate
pip install -e .

# Copy and fill in your config
cp conf/config.example.yaml conf/config.yaml
# Set OPENAI_API_KEY (or your provider key) in conf/config.yaml
```

## Start the service

```bash
cd ../deer-flow
make dev          # hot-reload dev server on http://localhost:8000
# or
python -m uvicorn src.server.app:app --reload --port 8000
```

## Verify

```bash
curl http://localhost:8000/api/health
# → {"status": "ok"}
```

Then run the example from the repo root:

```bash
cd /path/to/py/agent
DEERFLOW_BASE_URL=http://localhost:8000 python examples/134-deerflow-embedded-client/main.py
```

## Note on dependencies

DeerFlow pins a newer LangGraph/LangChain stack. Do **not** install it into this repo's virtual environment — run it in its own `.venv` as shown above.
