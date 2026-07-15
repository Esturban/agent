"""
123 — Agent Cost Tracking
Tools: tiktoken token counting, cost estimation, pricing table, CostTracker class.
"""

from dataclasses import dataclass, field
from typing import Optional

import tiktoken

# OpenAI pricing as of 2026-07 (USD per 1K tokens).
PRICING = {
    "gpt-5.4-nano": {"input": 0.0002, "output": 0.00125},
    "gpt-4o": {"input": 0.005, "output": 0.015},
    "gpt-4o-mini": {"input": 0.000150, "output": 0.000600},
    "gpt-4-turbo": {"input": 0.010, "output": 0.030},
    "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
}

DEFAULT_MODEL = "gpt-5.4-nano"


def count_tokens(text: str, model: str = DEFAULT_MODEL) -> int:
    """Count tokens in text using tiktoken."""
    try:
        enc = tiktoken.encoding_for_model(model)
    except KeyError:
        enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text))


def estimate_cost(input_tokens: int, output_tokens: int, model: str = DEFAULT_MODEL) -> float:
    """Estimate cost in USD for a single LLM call."""
    prices = PRICING.get(model, PRICING[DEFAULT_MODEL])
    cost = (input_tokens / 1000) * prices["input"] + (output_tokens / 1000) * prices["output"]
    return round(cost, 8)


@dataclass
class NodeRecord:
    node_name: str
    input_tokens: int
    output_tokens: int
    cost_usd: float


@dataclass
class CostTracker:
    """Accumulates per-node token usage and cost across a LangGraph run."""
    model: str = DEFAULT_MODEL
    _records: list[NodeRecord] = field(default_factory=list)

    def record(self, node_name: str, input_tokens: int, output_tokens: int) -> float:
        """Record a node's token usage and return the cost for this node."""
        cost = estimate_cost(input_tokens, output_tokens, self.model)
        self._records.append(NodeRecord(node_name, input_tokens, output_tokens, cost))
        return cost

    def total_cost(self) -> float:
        """Return total cost in USD across all recorded nodes."""
        return round(sum(r.cost_usd for r in self._records), 8)

    def report(self) -> dict:
        """Return a structured cost report."""
        node_costs = {r.node_name: r.cost_usd for r in self._records}
        most_expensive = max(self._records, key=lambda r: r.cost_usd, default=None)
        return {
            "total_cost_usd": self.total_cost(),
            "node_count": len(self._records),
            "per_node": node_costs,
            "most_expensive_node": most_expensive.node_name if most_expensive else None,
            "total_input_tokens": sum(r.input_tokens for r in self._records),
            "total_output_tokens": sum(r.output_tokens for r in self._records),
        }
