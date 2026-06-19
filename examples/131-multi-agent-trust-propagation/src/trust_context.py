"""
Trust context with TTL hop-count enforcement.

Problem: in multi-agent pipelines, trust granted to the orchestrator should NOT
automatically transfer to every sub-agent it spawns. An attacker who compromises
a low-trust subagent shouldn't be able to claim orchestrator-level privilege.

Solution: TrustContext carries both a TrustLevel and a ttl_hops counter.
Each delegation hop decrements ttl_hops. When it hits zero, no further
delegation is allowed — the pipeline terminates rather than blindly trusting.

Based on: arxiv:2502.10236 "Compromising LLM Agents in Multi-Agent Systems"
and OpenAI instruction hierarchy (arxiv:2404.13208).
"""

from dataclasses import dataclass, field
from enum import IntEnum
from typing import Optional


class TrustLevel(IntEnum):
    UNTRUSTED  = 0   # external data / injected tool outputs
    USER       = 1   # end-user messages
    OPERATOR   = 2   # operator system prompt
    SYSTEM     = 3   # top-level orchestrator / developer


@dataclass
class TrustContext:
    level: TrustLevel
    source_label: str             # human-readable: "orchestrator", "web_fetch", etc.
    ttl_hops: int = 3             # max further delegation hops before blocking
    delegation_chain: list[str] = field(default_factory=list)
    allowed_actions: list[str] = field(default_factory=list)
    forbidden_actions: list[str] = field(default_factory=list)

    def delegate(self, to_label: str, level_override: Optional[TrustLevel] = None) -> "TrustContext":
        """
        Return a new TrustContext for a sub-agent, decrementing ttl_hops.
        The delegated level is at most the parent's level (trust can't escalate).
        Raises RuntimeError if ttl_hops is exhausted.
        """
        if self.ttl_hops <= 0:
            raise RuntimeError(
                f"TrustContext TTL exhausted: {self.source_label} cannot delegate further. "
                f"Chain: {' → '.join(self.delegation_chain)}"
            )
        new_level = min(level_override or self.level, self.level)
        return TrustContext(
            level=new_level,
            source_label=to_label,
            ttl_hops=self.ttl_hops - 1,
            delegation_chain=self.delegation_chain + [self.source_label],
            allowed_actions=self.allowed_actions.copy(),
            forbidden_actions=self.forbidden_actions.copy(),
        )

    def can_perform(self, action: str) -> bool:
        if action in self.forbidden_actions:
            return False
        if self.allowed_actions:
            return action in self.allowed_actions
        return self.level >= TrustLevel.USER

    def summary(self) -> str:
        chain = " → ".join(self.delegation_chain + [self.source_label])
        return (
            f"TrustContext(level={self.level.name}, ttl_hops={self.ttl_hops}, "
            f"chain=[{chain}])"
        )


def root_context(
    allowed_actions: list[str] | None = None,
    forbidden_actions: list[str] | None = None,
    ttl_hops: int = 3,
) -> TrustContext:
    """Create the top-level SYSTEM trust context for an orchestrator."""
    return TrustContext(
        level=TrustLevel.SYSTEM,
        source_label="orchestrator",
        ttl_hops=ttl_hops,
        allowed_actions=allowed_actions or [],
        forbidden_actions=forbidden_actions or [],
    )
