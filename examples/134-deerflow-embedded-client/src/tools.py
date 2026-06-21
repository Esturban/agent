SAMPLE_CORPUS = """\
# Agent Framework Patterns

## State Graph
Explicit directed graph; nodes process state. Best for structured pipelines.

## Reactive Loop
Agent calls tools until done. Best for open-ended tasks and code generation.

## Multi-Agent
Supervisor delegates to specialists. Best for parallelizable research tasks.
"""

SAMPLE_QUERIES = [
    "Summarize the three patterns in one sentence each.",
    "Which pattern is best for a research report? One sentence.",
]

_ICONS = {"message_chunk": "·", "tool_call": "⚙", "tool_result": "✓", "end": "■"}


def format_event(event_type: str, data: dict) -> str:
    icon = _ICONS.get(event_type, "?")
    if event_type == "message_chunk":
        return f"{icon} {data.get('content', '')}"
    if event_type == "tool_call":
        return f"{icon} tool={data.get('tool_name', '?')}"
    if event_type == "tool_result":
        return f"{icon} result={str(data.get('content', ''))[:60]!r}"
    return f"{icon} [{event_type}]"
