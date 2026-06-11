from agents import tool

DOCS = [
    "OpenAI Agents SDK was released by OpenAI in early 2025.",
    "OpenAI Agents SDK uses Agent, Runner, tool, and handoff as its core primitives.",
    "An Agent is defined with a name, instructions, model, tools, and optional handoffs.",
    "Handoffs transfer control from one agent to another, like routing in LangGraph.",
    "Runner.run_sync() executes an agent synchronously and returns a RunResult.",
    "Built-in tracing in the Agents SDK records every step without external setup.",
    "The @tool decorator wraps a Python function into a tool callable by any Agent.",
    "LangGraph uses nodes and edges to build graphs; Agents SDK uses handoffs between agents.",
    "The Agents SDK supports parallel tool calls and structured output natively.",
    "Agents SDK agents can share tools — a tool defined once can be used by any agent.",
]

SAMPLE_QUESTIONS = [
    "What are the core primitives of the OpenAI Agents SDK?",
    "How does the Agents SDK differ from LangGraph?",
    "How does built-in tracing work in the Agents SDK?",
]


@tool
def keyword_search(query: str) -> str:
    """Search the knowledge base for relevant facts about the OpenAI Agents SDK."""
    words = set(query.lower().split())
    scored = [(sum(w in d.lower() for w in words), d) for d in DOCS]
    scored.sort(reverse=True)
    top = [d for _, d in scored[:3] if _ > 0]
    return "\n".join(top) if top else "No relevant facts found."
