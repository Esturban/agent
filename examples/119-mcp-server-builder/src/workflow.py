"""
119 — MCP Server Builder
Workflow: demonstrates all 3 tools and shows MCP server configuration.
"""

from .tools import convert_units, get_tool_schemas, get_weather, search_knowledge_base


def create_workflow() -> dict:
    """
    Demonstrate all 3 domain tools and show the MCP server configuration.
    No LangGraph graph needed — the workflow IS the MCP server.
    """
    print("=== 119 — MCP Server Builder ===\n")

    # 1. Weather tool
    print("Tool 1: get_weather")
    for city in ["London", "Tokyo", "Sydney"]:
        w = get_weather(city)
        print(f"  {w['city']}: {w['temperature_c']}°C / {w['temperature_f']}°F, {w['condition']}")

    # 2. Knowledge base search
    print("\nTool 2: search_knowledge_base")
    for query in ["MCP protocol", "LangGraph", "Claude Desktop"]:
        results = search_knowledge_base(query)
        print(f"  Query '{query}': {results[0][:70]}...")

    # 3. Unit conversion
    print("\nTool 3: convert_units")
    conversions = [
        (100, "km", "miles"),
        (70, "kg", "lbs"),
        (100, "C", "F"),
    ]
    for val, frm, to in conversions:
        r = convert_units(val, frm, to)
        print(f"  {r['input']} {r['from_unit']} = {r['result']} {r['to_unit']}")

    # 4. Show tool schemas
    print("\nMCP Tool Schemas:")
    schemas = get_tool_schemas()
    for schema in schemas:
        print(f"  {schema['name']}: {schema['description']}")

    # 5. Explain how to connect a client
    print("\nHow to connect from Claude Desktop:")
    print('  Add to ~/Library/Application Support/Claude/claude_desktop_config.json:')
    print('  {')
    print('    "mcpServers": {')
    print('      "domain-tools": {')
    print('        "command": "python",')
    print('        "args": ["examples/119-mcp-server-builder/main.py"]')
    print('      }')
    print('    }')
    print('  }')

    return {
        "tools_demonstrated": 3,
        "schemas": schemas,
        "transport": "stdio",
    }
