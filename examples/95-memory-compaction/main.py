import os
from dotenv import load_dotenv

load_dotenv()

from src.tools import DEMO_TURNS        # noqa: E402
from src.workflow import create_workflow # noqa: E402


def main() -> None:
    print("=== 95 · Memory Compaction ===")
    print("3-tier memory: hot (verbatim) → warm (LLM summaries) → cold (archive)")
    print("Based on MemGPT architecture — Packer et al. 2023 (arxiv.org/abs/2310.08560)\n")

    app = create_workflow()

    # Seed state with empty tiers — each invoke updates and returns the full state.
    state: dict = {
        "query": "", "response": "",
        "hot_tier": [], "warm_tier": [], "cold_tier": [], "context": "",
    }

    for i, turn in enumerate(DEMO_TURNS, start=1):
        state = app.invoke({**state, "query": turn})

        hot_n  = len(state["hot_tier"])
        warm_n = len(state["warm_tier"])
        cold_n = len(state["cold_tier"])
        compacted = " ← compacted" if (warm_n + cold_n) > 0 else ""

        print(f"[Turn {i:02d}] {turn[:65]}")
        print(f"         → {state['response'][:90]}...")
        print(f"         Tiers: hot={hot_n}  warm={warm_n}  cold={cold_n}{compacted}")
        print()

    print("=== Final memory state ===")
    print(f"Hot  ({len(state['hot_tier'])} turns)   — always injected verbatim")
    print(f"Warm ({len(state['warm_tier'])} blocks) — LLM summaries, always in context")
    print(f"Cold ({len(state['cold_tier'])} blocks) — archived; never auto-loaded")
    print("\nNote: high-signal turns ('remember…', 'never…') score higher and stay")
    print("in hot longer. Lowest-importance turns compact first.")


if __name__ == "__main__":
    main()
