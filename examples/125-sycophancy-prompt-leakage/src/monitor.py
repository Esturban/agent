"""
Post-response leakage scanner.

Two layers of detection:
  1. Canary check — deterministic: did the canary token appear in the response?
  2. Pattern classifier — probabilistic: does the response look like a leaked prompt?

In production, layer 1 is run synchronously (zero latency — just string search).
Layer 2 runs async and feeds an alert queue.
"""

import json
import re
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from prompts.defenses import CONVERSATION_MONITOR_PROMPT

_monitor = ChatOpenAI(model="gpt-5.4-nano", temperature=0)

# Known canary tokens from system_prompt.py variants
KNOWN_CANARIES = ["ZEBRA-7749", "PARROT-3821", "FALCON-9042", "CONDOR-5517"]


def check_canary(response: str) -> tuple[bool, list[str]]:
    """Return (leaked, [matched_canaries]). O(1) — just string search."""
    found = [c for c in KNOWN_CANARIES if c in response]
    return bool(found), found


def classify_sycophancy_attack(user_message: str) -> dict:
    """Classify whether a user message is a sycophancy attack (LLM judge)."""
    raw = _monitor.invoke([
        SystemMessage(content=CONVERSATION_MONITOR_PROMPT.format(user_message=user_message)),
        HumanMessage(content="Analyse the user message above."),
    ]).content
    m = re.search(r"\{.*\}", raw, re.DOTALL)
    if m:
        try:
            parsed = json.loads(m.group())
        except json.JSONDecodeError:
            parsed = None
        if isinstance(parsed, dict):
            return parsed
    return {
        "is_attack": True,
        "confidence": 1.0,
        "patterns_detected": ["unparseable_monitor_output"],
        "reasoning": "monitor output was not valid JSON",
    }


def scan(response: str, user_message: str) -> dict:
    """Full scan: canary check + sycophancy classification."""
    canary_leaked, canaries_found = check_canary(response)
    attack_signal = classify_sycophancy_attack(user_message)
    return {
        "canary_leaked": canary_leaked,
        "canaries_found": canaries_found,
        "is_sycophancy_attack": attack_signal.get("is_attack", False),
        "attack_confidence": attack_signal.get("confidence", 0.0),
        "patterns": attack_signal.get("patterns_detected", []),
    }
