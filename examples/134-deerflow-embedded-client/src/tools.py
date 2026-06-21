import textwrap

SAMPLE_CORPUS = textwrap.dedent("""\
    # Agent Framework Patterns

    This document covers three patterns for building production AI agents.

    ## Pattern 1: State Graph
    Build explicit directed graphs where nodes process state.
    Best for: structured pipelines, branching logic.

    ## Pattern 2: Reactive Loop
    Agent calls tools until it decides to stop.
    Best for: open-ended tasks, code generation.

    ## Pattern 3: Multi-Agent
    Supervisor delegates to specialist subagents.
    Best for: parallelizable research and report tasks.
""")

SAMPLE_QUERIES = [
    "Summarize the three patterns in one sentence each.",
    "Which pattern is best for a research report? One sentence.",
]

_EVENT_ICONS: dict[str, str] = {
    "message_chunk": "·",
    "tool_call": "⚙",
    "tool_result": "✓",
    "error": "✗",
    "end": "■",
}


def format_event(event_type: str, data: dict) -> str:
    icon = _EVENT_ICONS.get(event_type, "?")
    if event_type == "message_chunk":
        return f"{icon} {data.get('content', '')}"
    if event_type == "tool_call":
        return f"{icon} tool={data.get('tool_name', '?')}  args={data.get('args', {})}"
    if event_type == "tool_result":
        snippet = str(data.get("content", ""))[:60]
        return f"{icon} result={snippet!r}"
    return f"{icon} [{event_type}] {data}"
