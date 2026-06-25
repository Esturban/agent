---
teaching_ready: true
---
# 66-smol-agents

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none -- tools and sandboxing demo are inline in src/tools.py
**Deps:** `smolagents`

```bash
python examples/66-smol-agents/main.py
```

SmolAgents (HuggingFace): the LLM writes real Python as its reasoning trace, then executes it locally. Demonstrates: (1) `@tool`-decorated functions the agent can call; (2) the sandboxing concern — an unconstrained model could run `os.system`, `subprocess`, or exfiltration code; (3) `additional_authorized_imports` as the mitigation — unauthorized imports raise `ImportError` at runtime; (4) framework contrast: LangGraph (nodes + edges) vs CrewAI (roles + tasks) vs SmolAgents (code generation + direct execution).

---

### Graph

```
run_sandboxed_demo():  show risky code → restrict with authorized_imports → BLOCKED
  ↓
create_agent(safe_mode=True): CodeAgent with [multiply, word_count] tools
  ↓
agent.run(task) × 3 sample tasks (math + word count)
  ↓
framework contrast table
```
