from dotenv import load_dotenv

load_dotenv()

from src.tools import SEED_TURNS, USER_ID, store_turn  # noqa: E402
from src.workflow import create_workflow  # noqa: E402

QUERIES = [
    "What's my name and what do I work on?",         # should recall: Alex, ML engineer
    "What programming frameworks do I like?",        # should recall: PyTorch, transformers
    "Remind me about the paper I mentioned.",        # should recall: Mamba architecture
    "What language do I prefer?",                    # should recall: Python
]


def main() -> None:
    print("=== 87 · Vector Memory Agent ===")
    print("Contrast: Redis LRANGE (all history) vs ChromaDB top-k (relevant only)\n")

    # Seed the vector store with prior conversation context
    print(f"Seeding {len(SEED_TURNS)} turns into vector memory...")
    for turn in SEED_TURNS:
        store_turn(turn, user_id=USER_ID)
    print("Seed complete.\n")

    app = create_workflow()

    for query in QUERIES:
        result = app.invoke({
            "user_id": USER_ID,
            "query": query,
            "memories": [],
            "answer": "",
        })
        print(f"Q: {query}")
        print(f"Retrieved memories ({len(result['memories'])}):")
        for m in result["memories"]:
            print(f"  · {m[:80]}...")
        print(f"A: {result['answer']}\n")


if __name__ == "__main__":
    main()
