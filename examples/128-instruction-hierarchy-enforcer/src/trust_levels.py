"""
Trust level model from the OpenAI Instruction Hierarchy paper.
arxiv: 2404.13208, OpenAI 2024.

The paper proposes a privilege hierarchy:
  SYSTEM (3) > OPERATOR (2) > USER (1) > TOOL (0)

Instructions from a lower-trust source that conflict with a higher-trust
source should be blocked. This module defines the data model.

Key insight from the paper:
  - Most attacks succeed by getting user or tool-level content treated as
    system-level instructions (privilege escalation via context injection)
  - A trained instruction hierarchy model refuses ~95% of escalation attempts
  - Even without training, explicit enforcement logic helps significantly

Terminology:
  - SYSTEM:   the system prompt set by the deployment operator/developer
  - OPERATOR: operator-level instructions in the conversation (e.g. API calls)
  - USER:     messages typed by the end user
  - TOOL:     outputs from tool calls (retrieved documents, API responses, etc.)
"""

from dataclasses import dataclass
from enum import IntEnum


class TrustLevel(IntEnum):
    TOOL     = 0  # tool outputs, retrieved content — lowest trust
    USER     = 1  # user messages
    OPERATOR = 2  # operator API-level instructions
    SYSTEM   = 3  # system prompt — highest trust


@dataclass
class Instruction:
    """A single instruction with its source trust level."""
    content: str
    trust_level: TrustLevel
    source_label: str  # human-readable, e.g. "system_prompt", "user_message"


@dataclass
class TrustContext:
    """
    The current trust context: what is the highest-trust source's intent?
    The enforcer checks whether an incoming instruction conflicts with this.
    """
    system_instruction: str        # the protected instruction from SYSTEM level
    allowed_topics: list[str]      # topics the system prompt permits
    forbidden_actions: list[str]   # actions the system prompt explicitly bans

    def to_prompt_fragment(self) -> str:
        """Serialize this context for the LLM enforcer to reason about."""
        topics = ", ".join(self.allowed_topics) if self.allowed_topics else "any appropriate topic"
        banned = ", ".join(self.forbidden_actions) if self.forbidden_actions else "none specified"
        return (
            f"System intent: {self.system_instruction}\n"
            f"Permitted topics: {topics}\n"
            f"Forbidden actions: {banned}"
        )
