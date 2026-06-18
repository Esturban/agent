# 101 · SWE-Agent Code Editing

SWE-agent style code repair: the agent gets a buggy Python file and a failing test suite, then uses `view_file`, `edit_file`, and `run_tests` tools to iterate until all tests pass — no human involvement (Yang et al. 2024).

## Run

```bash
cp .env.example .env   # add OPENAI_API_KEY
python examples/101-swe-agent-code-editing/main.py
```

## Key concepts

- **ACI (agent-computer interface)**: a minimal tool set (view / edit / run) lets the model act like a developer inside a repo
- `create_react_agent` drives the loop — the model keeps calling tools until it emits a response with no further tool calls
- Two deliberate bugs: bad initialisation in `find_max` and an off-by-one in `average`; both are fixable from test output alone
