# 119 — MCP Server Builder

Implements a stdio MCP server using the `mcp` Python SDK that exposes 3 typed domain tools: weather lookup, knowledge base search, and unit conversion.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/119-mcp-server-builder/mcp_server_builder_workbook.ipynb)

## What it does

- Exposes `get_weather`, `search_knowledge_base`, and `convert_units` as MCP tools
- Runs as a stdio server connectable from Claude Desktop or any MCP client
- Falls back to demo mode if the `mcp` package is not installed

## How to run

```bash
# Demo mode (no mcp package needed)
python examples/119-mcp-server-builder/main.py

# As a stdio MCP server (requires: pip install mcp)
pip install mcp
python examples/119-mcp-server-builder/main.py
```

## Connect from Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "domain-tools": {
      "command": "python",
      "args": ["/absolute/path/to/examples/119-mcp-server-builder/main.py"]
    }
  }
}
```
