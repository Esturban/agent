"""
Monte Carlo Tree Search (MCTS) implementation for prompt fuzzing.
Based on: AgentVigil (arxiv:2505.05849), Berkeley 2025.

No LLM calls in this file — pure tree logic.
LLM calls happen in mutators.py (expansion) and judge.py (simulation).

MCTS loop per iteration:
  1. Select:     walk the tree using UCB1 to pick the most promising node
  2. Expand:     apply a mutation operator to create a child
  3. Simulate:   run the child prompt against the target agent, get a score
  4. Backprop:   propagate the score up through all ancestors

UCB1 = avg_reward + C * sqrt(ln(parent.visits) / node.visits)
  C = sqrt(2) balances exploration vs exploitation.
  Unvisited nodes have infinite UCB1 (always expanded first).
"""

import math


class Node:
    """A node in the MCTS tree. Represents one prompt variant."""

    def __init__(self, prompt: str, parent: "Node | None" = None, mutation_applied: str = "seed"):
        self.prompt = prompt
        self.parent = parent
        self.mutation_applied = mutation_applied  # which mutator created this node
        self.children: list["Node"] = []
        self.visits: int = 0
        self.total_reward: float = 0.0
        self.best_score: float = 0.0

    @property
    def avg_reward(self) -> float:
        return self.total_reward / self.visits if self.visits > 0 else 0.0

    def ucb1(self, exploration_constant: float = math.sqrt(2)) -> float:
        if self.visits == 0:
            return float("inf")
        if self.parent is None or self.parent.visits == 0:
            return self.avg_reward
        return self.avg_reward + exploration_constant * math.sqrt(
            math.log(self.parent.visits) / self.visits
        )

    def is_leaf(self) -> bool:
        return len(self.children) == 0

    def add_child(self, prompt: str, mutation_applied: str) -> "Node":
        child = Node(prompt=prompt, parent=self, mutation_applied=mutation_applied)
        self.children.append(child)
        return child

    def lineage(self) -> list[str]:
        """Return list of mutations from root to this node."""
        path = []
        node = self
        while node.parent is not None:
            path.append(node.mutation_applied)
            node = node.parent
        return list(reversed(path))


def select(node: Node) -> Node:
    """Walk the tree, always choosing the child with highest UCB1."""
    while not node.is_leaf():
        node = max(node.children, key=lambda c: c.ucb1())
    return node


def backpropagate(node: Node, reward: float) -> None:
    """Propagate reward up through all ancestors."""
    current = node
    while current is not None:
        current.visits += 1
        current.total_reward += reward
        current.best_score = max(current.best_score, reward)
        current = current.parent


def best_path(root: Node) -> list[Node]:
    """Return the path from root to the best-scoring descendant."""
    path = [root]
    node = root
    while node.children:
        node = max(node.children, key=lambda c: c.best_score)
        path.append(node)
    return path
