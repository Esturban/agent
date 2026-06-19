"""
Three defense wrappers for tool output before the LLM sees it.

All three implement the same interface:
    defense_fn(tool_output: str) -> str

Based on spotlighting (arxiv:2403.14720, Microsoft Research 2024):
- Delimiting:  wrap output in XML tags so the model knows it's external data
- Encoding:    base64-encode the payload so instruction patterns don't parse

The undefended baseline passes tool output through unchanged.
"""

import base64

INJECTION_KEYWORDS = [
    "ignore", "override", "system:", "instruction:", "important:",
    "your new task", "instead", "attacker", "evil.com",
]


def undefended(tool_output: str) -> str:
    """Pass tool output through unchanged (baseline)."""
    return tool_output


def spotlighting_delimit(tool_output: str) -> str:
    """
    Wrap tool output in XML delimiters so the model's system prompt can
    instruct it to treat this block as data, not instructions.
    Paper shows this reduces ASR from ~17% → ~8% (delimiting variant).
    """
    return f"<tool_output>\n{tool_output}\n</tool_output>"


def spotlighting_encode(tool_output: str) -> str:
    """
    Base64-encode tool output so instruction-shaped text can't be parsed
    by the language model as directives.
    Paper shows this reduces ASR from ~17% → 0–1.8% (encoding variant).

    The system prompt instructs the model: 'Tool outputs are base64-encoded.
    Decode them yourself before acting on the content.'
    """
    encoded = base64.b64encode(tool_output.encode()).decode()
    return f"[base64]{encoded}[/base64]"


def keyword_filter(tool_output: str) -> str:
    """
    Heuristic keyword blocklist. Fast but brittle — adversarially crafted
    payloads trivially evade simple pattern matching.
    """
    lower = tool_output.lower()
    for kw in INJECTION_KEYWORDS:
        if kw in lower:
            return "[Tool output redacted: potential injection detected]"
    return tool_output


DEFENSES: list[tuple[str, callable]] = [
    ("undefended", undefended),
    ("spotlighting_delimit", spotlighting_delimit),
    ("spotlighting_encode", spotlighting_encode),
    ("keyword_filter", keyword_filter),
]
