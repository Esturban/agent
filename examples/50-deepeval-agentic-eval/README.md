# 50-deepeval-agentic-eval

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none

```bash
pip install deepeval
python examples/50-deepeval-agentic-eval/main.py
```

Evaluate a LangGraph ReAct agent with DeepEval's `ToolCorrectnessMetric` and `TaskCompletionMetric`. Shows how to extract tool call history from LangGraph message state and map it to DeepEval's `tools_called` + `expected_tools` fields.

---

### Graph

```
START
  |
ReAct agent   ← create_react_agent with [search_web, calculate, lookup_fact]
  |           ← loops: think → tool call → observe
END           (tool call history extracted → deepeval.evaluate())
```

### Why agent eval is harder than RAG eval

| Challenge | RAG | Agent |
|-----------|-----|-------|
| Non-determinism | Low (same retrieval) | High (tool order varies) |
| Multi-step reasoning | No | Yes — errors compound |
| Tool side effects | No | Yes — tools change state |
| Evaluation unit | Answer | Full trajectory |

### LLMTestCase fields for agents

```python
LLMTestCase(
    input="task description",
    actual_output="final answer",
    tools_called=[ToolCall(name="search_web", input_parameters={...}, output="...")],
    expected_tools=[ExpectedTool(name="search_web"), ExpectedTool(name="calculate")],
)
```
