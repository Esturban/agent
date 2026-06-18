from dotenv import load_dotenv

load_dotenv()

from src.tools import DEMO_QUERIES, INITIAL_MEMORY  # noqa: E402
from src.workflow import create_workflow  # noqa: E402


def main() -> None:
    print("=== 88 · Memory Architecture — Episodic / Semantic / Procedural ===")
    print("Ref: Tulving (1972) + MemGPT (Packer et al. 2023, arxiv 2310.08560)\n")

    app = create_workflow()
    memory = dict(INITIAL_MEMORY)  # start with seeded knowledge

    print("Initial memory state:")
    print(f"  Episodic  ({len(memory['episodic'])} entries): {memory['episodic']}")
    print(f"  Semantic  ({len(memory['semantic'])} keys):    {list(memory['semantic'].keys())}")
    print(f"  Procedural ({len(memory['procedural'])} rules): {memory['procedural'][:1]}...\n")

    for query in DEMO_QUERIES:
        result = app.invoke({
            "memory": memory,
            "query": query,
            "answer": "",
        })
        # Carry memory forward — each turn can add to any tier.
        memory = result["memory"]
        print(f"Q: {query}")
        print(f"A: {result['answer']}")
        print(f"   [memory now: {len(memory['episodic'])} episodic, "
              f"{len(memory['semantic'])} semantic, "
              f"{len(memory['procedural'])} procedural]\n")


if __name__ == "__main__":
    main()
