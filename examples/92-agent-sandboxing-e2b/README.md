---
teaching_ready: true
---
# 92 · Agent Sandboxing — E2B

Generates Python code with an LLM and executes it inside an E2B ephemeral cloud microVM. `stdout`, `stderr`, and exceptions are captured as structured data — no generated code touches the host. Three-node graph: `generate_code → execute_in_sandbox → interpret_result`.

```bash
pip install e2b-code-interpreter
cd examples/92-agent-sandboxing-e2b
python main.py
```

Requires: `OPENAI_API_KEY` and `E2B_API_KEY` in `.env` (free tier at e2b.dev).
