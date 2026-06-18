from dotenv import load_dotenv

load_dotenv()

from src.tools import HAZARD_CATEGORIES, TEST_QUERIES  # noqa: E402
from src.workflow import create_workflow                # noqa: E402


def main() -> None:
    print("=== 93 · LlamaGuard Guardrails ===")
    print("Ref: Inan et al. 2023 — arxiv.org/abs/2312.06674\n")
    print("Pattern: classify EVERY input → route SAFE to agent, UNSAFE to refuse.\n")
    print(f"Hazard categories: {', '.join(f'{k}={v}' for k, v in HAZARD_CATEGORIES.items())}\n")

    app = create_workflow()

    for query in TEST_QUERIES:
        print(f"Query: {query}")
        result = app.invoke({
            "query": query,
            "classification": "",
            "hazard_category": "",
            "response": "",
        })

        # Show classification result with visual indicator.
        tag = "✓ SAFE" if result["classification"] == "SAFE" else f"✗ UNSAFE ({result['hazard_category']})"
        print(f"Guard: {tag}")
        print(f"Response: {result['response'][:150]}")
        print("-" * 60)

    print("\nNote: swap the guard_llm for Groq's `llama-guard-3-8b` in workflow.py")
    print("for production-grade classification with Meta's fine-tuned model.")


if __name__ == "__main__":
    main()
