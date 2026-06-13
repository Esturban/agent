# 44-mcp-client-agent

## Prerequisites
**Keys:** `OPENAI_API_KEY`
**Files:** none

```bash
python examples/44-mcp-client-agent/main.py
```

Demonstrates the MCP (Model Context Protocol) client pattern: an agent dynamically discovers tools from a server at runtime, selects the right one, invokes it, and synthesizes a final answer. Uses an in-process mock server — no subprocess needed.

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
