import os
from dotenv import load_dotenv

load_dotenv()

if not os.environ.get("OPENAI_API_KEY", "").startswith("sk-"):
    raise RuntimeError("OPENAI_API_KEY is required for best-of-N sampling.")

from src.tools import PROBLEMS, N_SAMPLES   # noqa: E402
from src.workflow import create_workflow     # noqa: E402


def main() -> None:
    print(f"=== 97 · Best-of-N Sampling | N={N_SAMPLES} | process reward model ===")
    print("Ref: Cobbe et al. 2021 — arxiv.org/abs/2110.14168\n")

    app = create_workflow()

    for problem in PROBLEMS:
        print(f"[{problem['label']}]  {problem['question']}\n")

        result = app.invoke({
            "question":   problem["question"],
            "candidates": [],
            "scored":     [],
            "best":       "",
        })

        # Print all scored candidates from worst to best so the winner is last.
        ranked = sorted(result["scored"], key=lambda c: c["score"])
        for i, c in enumerate(ranked, start=1):
            print(f"  Chain {i}  score={c['score']}/10  → {c['answer'][:80]}")
            print(f"          {c['critique']}")
        print()
        print(f"  BEST ANSWER: {result['best']}")
        print("-" * 70)
        print()

    print("Takeaway: best-of-N scales inference compute instead of training compute.")
    print("A process reward model scores intermediate steps — not just the final answer.")


if __name__ == "__main__":
    main()
