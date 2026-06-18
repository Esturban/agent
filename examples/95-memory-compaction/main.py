import os
from dotenv import load_dotenv

load_dotenv()

from src.tools import DEMO_TURNS         # noqa: E402
from src.workflow import create_workflow  # noqa: E402


def main() -> None:
    print("=== 95 · Memory Compaction ===")
    print("hot (verbatim) → warm (LLM summaries) → cold (archive)\n")

    app = create_workflow()
    state: dict = {
        "query": "", "response": "",
        "hot_tier": [], "warm_tier": [], "cold_tier": [], "context": "",
    }

    for i, turn in enumerate(DEMO_TURNS, start=1):
        state = app.invoke({**state, "query": turn})
        h, w, c = len(state["hot_tier"]), len(state["warm_tier"]), len(state["cold_tier"])
        flag = " ← compacted" if (w + c) > 0 else ""

        print(f"[{i:02d}] {turn[:70]}")
        print(f"      {state['response'][:90]}...")
        print(f"      hot={h}  warm={w}  cold={c}{flag}\n")

    print("Final tiers:")
    print(f"  Hot  {len(state['hot_tier'])} turns   — verbatim, always in context")
    print(f"  Warm {len(state['warm_tier'])} blocks  — LLM summaries, always in context")
    print(f"  Cold {len(state['cold_tier'])} blocks  — archived, never auto-loaded")


if __name__ == "__main__":
    main()
