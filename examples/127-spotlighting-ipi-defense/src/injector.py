"""
Inject a payload into a benign document.

Inserts the payload at a realistic position (middle of the document,
between paragraphs) so it looks like part of the content rather than
an obvious standalone injection.
"""


def inject(document: str, payload: str) -> str:
    """Insert the payload in the middle of the document."""
    lines = document.strip().split("\n")
    mid = len(lines) // 2
    injected_lines = lines[:mid] + [f"\n{payload}\n"] + lines[mid:]
    return "\n".join(injected_lines)
