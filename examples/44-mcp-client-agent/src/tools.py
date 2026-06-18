import requests
from dataclasses import dataclass
from typing import Callable, TypedDict

from langchain_openai import ChatOpenAI

SAMPLE_QUERIES = [
    "What is the weather like in Tokyo?",
    "Calculate 15% tip on a $47.50 bill.",
    "What time is it in London right now?",
]


def _live_weather(city: str) -> str:
    # wttr.in format=3 returns "Tokyo: ⛅️ +18°C" as plain text — no API key.
    r = requests.get(f"https://wttr.in/{city}?format=3", timeout=5)
    return r.text.strip() if r.ok else f"Weather unavailable for {city}"


def _live_time(city: str) -> str:
    # Open-Meteo geocoding resolves city → timezone, then World Time API returns current datetime.
    # Both are completely free with no API key required.
    geo = requests.get(
        f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1", timeout=5
    )
    tz = geo.json()["results"][0]["timezone"]
    t = requests.get(f"https://worldtimeapi.org/api/timezone/{tz}", timeout=5)
    return t.json()["datetime"][:19].replace("T", " ")


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
    server.register("get_weather", "Get current weather for a city", _live_weather)
    server.register(
        "calculate_tip", "Calculate tip amount", lambda bill, pct: f"${bill * pct / 100:.2f} tip"
    )
    server.register("get_time", "Get current time for a city", _live_time)
    return server


class MCPState(TypedDict):
    query: str
    available_tools: list[dict]
    tool_name: str
    tool_args: dict
    tool_result: str
    final_answer: str


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
