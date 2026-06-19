"""
Spotlighting functions: transform external text to make it distinguishable from instructions.
Based on: arxiv:2403.14720, Microsoft Research 2024.

Each function takes raw external text and returns a transformed version
that, when combined with the matching system prompt variant, tells the
model this is untrusted data rather than an executable instruction.
"""

import base64


def delimit(text: str) -> str:
    """Wrap external text in XML-style tags. Simplest spotlighting method."""
    return f"<external_data>\n{text}\n</external_data>"


def datamark(text: str) -> str:
    """
    Prepend each word with U+2062 (INVISIBLE TIMES).
    The invisible character acts as a data marker — the model's system prompt
    tells it that marked words are data, not instructions.
    Human-readable but machine-detectable.
    """
    invisible = "⁢"  # U+2062 INVISIBLE TIMES
    words = text.split(" ")
    marked = " ".join(invisible + word for word in words)
    return marked


def encode(text: str) -> str:
    """
    Base64-encode the external text.
    The system prompt instructs the model to decode and summarize,
    never to execute instructions within the decoded content.
    Most effective spotlighting method — near-zero ASR under standard attacks.
    """
    return base64.b64encode(text.encode()).decode()


SPOTLIGHTING_FUNCTIONS = {
    "none":        lambda text: text,  # no transformation — baseline
    "delimiting":  delimit,
    "datamarking": datamark,
    "encoding":    encode,
}
