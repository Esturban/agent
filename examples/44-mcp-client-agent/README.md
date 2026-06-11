# 44-mcp-client-agent

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Esturban/agent/blob/master/examples/44-mcp-client-agent/mcp_client_workbook.ipynb)

Demonstrates the MCP (Model Context Protocol) client pattern: an agent dynamically discovers tools from a server at runtime, selects the right one, invokes it, and synthesizes a final answer. Uses an in-process mock server — no subprocess needed.

**Keys:** `OPENAI_API_KEY`

```bash
python examples/44-mcp-client-agent/main.py
```

---

### Graph

```
START → discover (list tools, LLM selects) → invoke (call tool) → synthesize → END
```

### MCP Pattern

| Step | MCP concept | This example |
|------|-------------|--------------|
| Discovery | `client.list_tools()` | `_server.list_tools()` |
| Invocation | `client.call_tool(name, args)` | `_server.call_tool(name, args)` |
| Transport | stdio / HTTP+SSE | In-process mock |
| Tool schema | JSON Schema per tool | Description string per tool |
