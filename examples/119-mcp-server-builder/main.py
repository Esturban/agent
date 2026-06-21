"""
119 — MCP Server Builder
Entry point: starts a stdio MCP server exposing 3 domain tools.
Run: python examples/119-mcp-server-builder/main.py
"""

import asyncio
import json
import sys

from dotenv import load_dotenv

load_dotenv()

# Try to import mcp SDK; fall back to demo mode
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import TextContent, Tool
    HAS_MCP = True
except ImportError:
    HAS_MCP = False

from src.tools import convert_units, get_tool_schemas, get_weather, search_knowledge_base
from src.workflow import create_workflow


def main():
    if not HAS_MCP:
        print("[INFO] mcp package not installed — running demo mode.")
        print("[INFO] Install with: pip install mcp")
        print()
        create_workflow()
        return

    app = Server("domain-tools")
    schemas = get_tool_schemas()

    @app.list_tools()
    async def list_tools():
        return [
            Tool(name=s["name"], description=s["description"], inputSchema=s["inputSchema"])
            for s in schemas
        ]

    @app.call_tool()
    async def call_tool(name: str, arguments: dict):
        if name == "get_weather":
            result = get_weather(arguments["city"])
        elif name == "search_knowledge_base":
            result = search_knowledge_base(arguments["query"])
        elif name == "convert_units":
            result = convert_units(
                arguments["value"], arguments["from_unit"], arguments["to_unit"]
            )
        else:
            result = {"error": f"Unknown tool: {name}"}
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    print("[MCP] domain-tools server starting on stdio...", file=sys.stderr)
    asyncio.run(stdio_server(app))


if __name__ == "__main__":
    main()
