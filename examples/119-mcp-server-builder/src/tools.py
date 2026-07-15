"""
119 — MCP Server Builder
Tool implementations: weather mock, knowledge base search, unit conversion.
"""

WEATHER_DATA = {
    "london": {"temp_c": 15, "condition": "cloudy", "humidity": 72},
    "new york": {"temp_c": 22, "condition": "sunny", "humidity": 55},
    "tokyo": {"temp_c": 28, "condition": "partly cloudy", "humidity": 80},
    "paris": {"temp_c": 18, "condition": "rainy", "humidity": 85},
    "sydney": {"temp_c": 20, "condition": "clear", "humidity": 60},
}

KNOWLEDGE_BASE = [
    "Python was created by Guido van Rossum in 1991.",
    "LangGraph is a library for building stateful multi-actor applications with LLMs.",
    "The MCP protocol uses JSON-RPC 2.0 for communication between clients and servers.",
    "Stdio transport pipes JSON messages through stdin/stdout.",
    "SSE (Server-Sent Events) transport uses HTTP for browser-compatible MCP servers.",
    "Tool schemas in MCP are defined using JSON Schema.",
    "Claude Desktop supports MCP servers via its config file at ~/Library/Application Support/Claude/claude_desktop_config.json.",
    "LangGraph nodes are Python functions that receive and return state dicts.",
    "OpenAI's gpt-5.4-nano is a cost-efficient model for tool-calling tasks.",
    "Pydantic v2 is the recommended validation library for LangChain/LangGraph projects.",
]

UNIT_CONVERSIONS = {
    ("km", "miles"): 0.621371,
    ("miles", "km"): 1.60934,
    ("kg", "lbs"): 2.20462,
    ("lbs", "kg"): 0.453592,
    ("c", "f"): None,  # special case
    ("f", "c"): None,  # special case
}


def get_weather(city: str) -> dict:
    """Return mock weather data for a city."""
    key = city.lower().strip()
    data = WEATHER_DATA.get(key, {"temp_c": 20, "condition": "unknown", "humidity": 50})
    return {
        "city": city,
        "temperature_c": data["temp_c"],
        "temperature_f": round(data["temp_c"] * 9 / 5 + 32, 1),
        "condition": data["condition"],
        "humidity_pct": data["humidity"],
    }


def search_knowledge_base(query: str) -> list[str]:
    """Search the hardcoded knowledge base for facts matching the query."""
    query_lower = query.lower()
    matches = [fact for fact in KNOWLEDGE_BASE if any(word in fact.lower() for word in query_lower.split())]
    return matches or ["No matching facts found."]


def convert_units(value: float, from_unit: str, to_unit: str) -> dict:
    """Convert between km/miles, kg/lbs, or C/F."""
    from_u = from_unit.lower().strip()
    to_u = to_unit.lower().strip()

    if from_u == "c" and to_u == "f":
        result = value * 9 / 5 + 32
    elif from_u == "f" and to_u == "c":
        result = (value - 32) * 5 / 9
    else:
        factor = UNIT_CONVERSIONS.get((from_u, to_u))
        if factor is None:
            return {"error": f"Unsupported conversion: {from_unit} → {to_unit}"}
        result = value * factor

    return {
        "input": value,
        "from_unit": from_unit,
        "to_unit": to_unit,
        "result": round(result, 4),
    }


def get_tool_schemas() -> list[dict]:
    """Return JSON Schema definitions for all 3 tools (MCP-compatible format)."""
    return [
        {
            "name": "get_weather",
            "description": "Get current weather data for a city.",
            "inputSchema": {
                "type": "object",
                "properties": {"city": {"type": "string", "description": "City name"}},
                "required": ["city"],
            },
        },
        {
            "name": "search_knowledge_base",
            "description": "Search a knowledge base of facts about Python, LLMs, and MCP.",
            "inputSchema": {
                "type": "object",
                "properties": {"query": {"type": "string", "description": "Search query"}},
                "required": ["query"],
            },
        },
        {
            "name": "convert_units",
            "description": "Convert between km/miles, kg/lbs, or Celsius/Fahrenheit.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "value": {"type": "number"},
                    "from_unit": {"type": "string", "description": "km, miles, kg, lbs, C, or F"},
                    "to_unit": {"type": "string", "description": "km, miles, kg, lbs, C, or F"},
                },
                "required": ["value", "from_unit", "to_unit"],
            },
        },
    ]
