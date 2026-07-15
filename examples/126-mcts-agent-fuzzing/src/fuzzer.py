"""
MCTS fuzzer: orchestrates the select → mutate → run → judge → backprop loop.

Each iteration:
  1. Select: pick the most promising node in the tree (UCB1)
  2. Mutate: apply a mutation operator to create a child prompt
  3. Run: execute the child against the target agent
  4. Judge: score the response (0.0-1.0)
  5. Backpropagate: update all ancestors with the reward

Returns the best prompt found and the final tree root for visualisation.
"""

import random
from .mcts import Node, select, backpropagate, best_path
from .mutators import mutate
from .target_agent import run_target
from .judge import score_response


def run_mcts(
    seed_prompt: str,
    budget: int = 10,
    success_threshold: float = 0.5,
    verbose: bool = True,
) -> tuple[str, float, Node, list[dict]]:
    """
    Run MCTS fuzzing on one seed prompt.

    Returns:
      (best_prompt, best_score, root_node, history)
      history is a list of {iteration, prompt, score, operator, success} dicts.
    """
    root = Node(prompt=seed_prompt, mutation_applied="seed")
    history: list[dict] = []
    best_prompt = seed_prompt
    best_score = 0.0

    for i in range(budget):
        # 1. Select
        node = root if len(root.children) < 3 else select(root)

        # 2. Expand: apply a random mutation
        # Occasionally combine two high-scoring nodes if we have options
        other_node = None
        if len(root.children) > 1 and random.random() < 0.2:
            candidates = [c for c in root.children if c != node and c.visits > 0]
            if candidates:
                other_node = max(candidates, key=lambda n: n.avg_reward)

        mutated, operator = mutate(
            node.prompt,
            other_prompt=other_node.prompt if other_node else None,
        )
        child = node.add_child(mutated, mutation_applied=operator)

        # 3. Simulate
        response = run_target(mutated)

        # 4. Judge
        score, success, reasoning = score_response(mutated, response)

        # 5. Backpropagate
        backpropagate(child, score)

        history.append({
            "iteration": i + 1,
            "prompt": mutated[:100],
            "operator": operator,
            "score": score,
            "success": success,
            "reasoning": reasoning[:80],
        })

        if score > best_score:
            best_score = score
            best_prompt = mutated

        if verbose:
            bar = "█" * int(score * 10) + "░" * (10 - int(score * 10))
            mark = " ← SUCCESS" if success else ""
            print(f"  [{i+1:2d}] {operator:12} score=[{bar}] {score:.2f}{mark}")

        if success and score >= success_threshold:
            if verbose:
                print(f"  [EARLY STOP] Success found at iteration {i+1}")
            break

    return best_prompt, best_score, root, history
