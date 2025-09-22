---
approved: true
approved_by: Esteban
approved_at: 2025-09-22T16:00:00Z
spec_version: 1
---

# Minimal tools-only StateGraph workflow plan

Goal:
- Implement a minimal StateGraph workflow in `examples/2-external-vdb/main.py` that uses only tool nodes and a single agent node, keeping the file short and simple.

Assumptions:
- `export_stategraph` exists in `examples/2-external-vdb/src/utils.py` and works as expected.
- The environment variables for Qdrant and Brave (if used) are set, but the implementation should run without requiring them for the minimal workflow.

Constraints:
- Keep the implementation concise (<100 lines added/modified).
- Use only tools and the agent node; avoid extra nodes or complex routing.
- Maintain existing imports where useful.

Design:
- Create a `ToolNode` with a small set of tools (re-using `hf_retriever_tool`, `transformer_retriever_tool`, `search_tool`).
- Create a single `agent` node that calls the LLM bound with tools.
- Use `add_edge` and `add_conditional_edges` to cycle between `agent` and `tools` until the model returns no tool call.
- Export the graph using `export_stategraph`.

Tasks:
1. Update `specs/minimal-tools-workflow-plan.md` (this file) and mark approved=true when ready.
2. Implement the minimal workflow in `examples/2-external-vdb/main.py`.

References:
- `examples/2-external-vdb/src/utils.py` (for `export_stategraph`)
- `examples/1-basic/main.py` (simple StateGraph usage example)

Acceptance criteria:
- Running `python examples/2-external-vdb/main.py` should start the agent and print assistant output for a sample query.
- `examples/2-external-vdb/assets/stategraph.png` is produced by calling `export_stategraph`.
