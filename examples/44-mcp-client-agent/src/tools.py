from dataclasses import dataclass
from typing import Any, Callable, TypedDict

from langchain_openai import ChatOpenAI

SAMPLE_QUERIES = [
    "What is the weather like in Tokyo?",
    "Calculate 15% tip on a $47.50 bill.",
    "What time is it in London right now?",
]


@dataclass
class MCPTool:
    name: str
    description: str
    fn: Callable


class MockMCPServer:
    """Simulates an MCP server's tool registry over stdio."""

    def __init__(self):
        self._tools: dict[str, MCPTool] = {}

    def register(self, name: str, description: str, fn: Callable):
        self._tools[name] = MCPTool(name=name, description=description, fn=fn)

    def list_tools(self) -> list[dict]:
        return [{"name": t.name, "description": t.description} for t in self._tools.values()]

    def call_tool(self, name: str, args: dict) -> str:
        if name not in self._tools:
            return f"Unknown tool: {name}"
        return str(self._tools[name].fn(**args))


def build_mock_server() -> MockMCPServer:
    server = MockMCPServer()
    server.register("get_weather", "Get current weather for a city", lambda city: f"Sunny, 22°C in {city}")
    server.register("calculate_tip", "Calculate tip amount", lambda bill, pct: f"${bill * pct / 100:.2f} tip")
    server.register("get_time", "Get current time in a timezone", lambda city: f"12:34 PM in {city}")
    return server


class MCPState(TypedDict):
    query: str
    available_tools: list[dict]
    tool_name: str
    tool_args: dict
    tool_result: str
    final_answer: str


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
