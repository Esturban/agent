"""
Crescendomation planner: generate the next turn prompt.

Given:
  - conversation_history: list of {role, content} dicts (what's been said so far)
  - current_level: which escalation level we're on (1-5)
  - objective: the target elicitation goal
  - domain: the benign topic domain used for L1/L2 framing

Returns the next user message to send to the target.

At L1-L4 we use the template-based approach.
At L5+ we use the LLM planner to generate a context-aware final request.
"""

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from prompts.escalation_templates import (
    L1_SYSTEM, L1_USER, L2_USER, L3_USER, L4_USER, L5_USER,
    PLANNER_SYSTEM, LEVEL_GOALS,
)

_planner = ChatOpenAI(model="gpt-5.4-nano", temperature=0.7)


def _format_conversation(history: list[dict]) -> str:
    lines = []
    for turn in history:
        role = turn["role"].upper()
        lines.append(f"{role}: {turn['content'][:300]}")
    return "\n\n".join(lines)


def generate_next_turn(
    objective: str,
    domain: str,
    conversation_history: list[dict],
    current_level: int,
) -> str:
    """Return the next user message for the given escalation level."""
    prev_response = ""
    if conversation_history:
        last_assistant = next(
            (t["content"] for t in reversed(conversation_history) if t["role"] == "assistant"),
            "",
        )
        prev_response = last_assistant[:400]

    # L1: use template directly (no prior context needed)
    if current_level == 1:
        return L1_USER.format(domain=domain)

    # L2-L4: LLM planner generates turn using template as seed
    if current_level <= 4:
        template_map = {2: L2_USER, 3: L3_USER, 4: L4_USER}
        template = template_map[current_level]
        seed = template.format(
            key_concept_from_l1=domain,
            topic_aspect=domain,
            objective=objective,
        )
        system = PLANNER_SYSTEM.format(
            objective=objective,
            level=current_level,
            level_goal=LEVEL_GOALS[current_level],
            prev_response=prev_response,
        )
        reply = _planner.invoke([
            SystemMessage(content=system),
            HumanMessage(content=f"Seed template for this level:\n{seed}\n\nGenerate the turn:"),
        ]).content
        return reply.strip()

    # L5+: free-form planner with full context
    system = PLANNER_SYSTEM.format(
        objective=objective,
        level=5,
        level_goal=LEVEL_GOALS[5],
        prev_response=prev_response,
    )
    conversation_text = _format_conversation(conversation_history)
    reply = _planner.invoke([
        SystemMessage(content=system),
        HumanMessage(content=f"Full conversation so far:\n{conversation_text}\n\nGenerate the final escalation turn:"),
    ]).content
    return reply.strip()
