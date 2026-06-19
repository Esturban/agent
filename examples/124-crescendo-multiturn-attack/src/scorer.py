"""
Crescendo judge: score the target's latest response.

Returns a tuple: (score: int, reasoning: str, what_worked: str, should_continue: bool)
"""

import json
import re
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from prompts.judge_prompt import JUDGE_SYSTEM, JUDGE_USER

_judge = ChatOpenAI(model="gpt-4o-mini", temperature=0)


def _format_conversation(history: list[dict]) -> str:
    lines = []
    for turn in history:
        role = "User" if turn["role"] == "user" else "Assistant"
        lines.append(f"{role}: {turn['content'][:250]}")
    return "\n\n".join(lines)


def score_response(
    objective: str,
    conversation_history: list[dict],
    latest_response: str,
    threshold: int,
    max_turns: int,
    current_turn: int,
) -> tuple[int, str, str, bool]:
    system = JUDGE_SYSTEM.format(threshold=threshold, max_turns=max_turns)
    user = JUDGE_USER.format(
        objective=objective,
        conversation=_format_conversation(conversation_history),
        latest_response=latest_response[:600],
    )
    raw = _judge.invoke([
        SystemMessage(content=system),
        HumanMessage(content=user),
    ]).content
    m = re.search(r"\{.*\}", raw, re.DOTALL)
    if m:
        data = json.loads(m.group())
        score = int(data.get("score", 1))
        reasoning = data.get("reasoning", "")
        what_worked = data.get("what_worked", "")
        # Override should_continue if we've hit the budget
        should_continue = bool(data.get("should_continue", False)) and current_turn < max_turns
        return score, reasoning, what_worked, should_continue
    return 1, "parse error", "", False
