import json

from langchain_core.messages import HumanMessage
from langgraph.graph import END, StateGraph

from .tools import MCPState, build_mock_server, llm

_server = build_mock_server()

DISCOVER_PROMPT = """You have access to these tools from an MCP server:
{tools}

For this query: "{query}"
Which tool should be called? Respond as JSON: {{"tool": "tool_name", "args": {{...}}}}
If no tool fits, respond: {{"tool": "none", "args": {{}}}}"""

ANSWER_PROMPT = """Query: {query}
Tool called: {tool_name}
Tool result: {tool_result}
Provide a helpful final answer."""


def discover_and_select(state: MCPState) -> dict:
    tools = _server.list_tools()
    tools_text = "\n".join(f"- {t['name']}: {t['description']}" for t in tools)
    prompt = DISCOVER_PROMPT.format(tools=tools_text, query=state["query"])
    result = llm.invoke([HumanMessage(content=prompt)])
    try:
        text = result.content.strip()
        if text.startswith("```"):
            text = "\n".join(text.split("\n")[1:-1])
        parsed = json.loads(text)
        print(f"  Selected: {parsed.get('tool')} with args {parsed.get('args')}")
        return {"available_tools": tools, "tool_name": parsed.get("tool", "none"), "tool_args": parsed.get("args", {})}
    except Exception:
        return {"available_tools": tools, "tool_name": "none", "tool_args": {}}


def invoke_tool(state: MCPState) -> dict:
    if state["tool_name"] == "none":
        return {"tool_result": "No tool selected"}
    result = _server.call_tool(state["tool_name"], state["tool_args"])
    print(f"  Tool result: {result}")
    return {"tool_result": result}


def synthesize(state: MCPState) -> dict:
    prompt = ANSWER_PROMPT.format(
        query=state["query"], tool_name=state["tool_name"], tool_result=state["tool_result"]
    )
    result = llm.invoke([HumanMessage(content=prompt)])
    return {"final_answer": result.content}


def create_workflow():
    graph = StateGraph(MCPState)
    graph.add_node("discover", discover_and_select)
    graph.add_node("invoke", invoke_tool)
    graph.add_node("synthesize", synthesize)
    graph.set_entry_point("discover")
    graph.add_edge("discover", "invoke")
    graph.add_edge("invoke", "synthesize")
    graph.add_edge("synthesize", END)
    return graph.compile()
