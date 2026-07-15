"""
Judge: scores how successful an injection was against the target agent.

Returns a float 0.0–1.0 (continuous, not binary).
The MCTS backpropagation uses this as the reward signal.
"""

import json
import re
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from corpus.seed_injections import JUDGE_SYSTEM

_judge = ChatOpenAI(model="gpt-5.4-nano", temperature=0)


def score_response(injection_prompt: str, agent_response: str) -> tuple[float, bool, str]:
    """Return (score, success, reasoning)."""
    raw = _judge.invoke([
        SystemMessage(content=JUDGE_SYSTEM),
        HumanMessage(content=f"Injection prompt:\n{injection_prompt}\n\nAgent response:\n{agent_response}"),
    ]).content
    m = re.search(r"\{.*\}", raw, re.DOTALL)
    if m:
        try:
            data = json.loads(m.group())
        except json.JSONDecodeError:
            data = None
        if not isinstance(data, dict):
            return 0.0, False, "unparseable judge response"
        score = float(data.get("score", 0.0))
        success = bool(data.get("success", False))
        reasoning = data.get("reasoning", "")
        return score, success, reasoning
    return 0.0, False, "unparseable judge response"
