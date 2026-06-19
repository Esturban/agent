"""Entry point for example 65 — LiteLLM multi-provider agent.

Runs a LangGraph workflow that:
1. Estimates cost and picks the best model within a USD budget.
2. Calls that model via ChatLiteLLM.
3. Compares responses across all providers whose API keys are set.

Usage:
    python main.py

Required env:
    OPENAI_API_KEY

Optional env (enables additional provider comparisons):
    ANTHROPIC_API_KEY, GEMINI_API_KEY, COHERE_API_KEY
"""

from dotenv import load_dotenv

load_dotenv()

from src.workflow import create_workflow  # noqa: E402 (after load_dotenv)

DEMO_PROMPT = "Explain neural networks in exactly one sentence."
BUDGET_USD = 0.001  # generous enough for gpt-4o-mini, may downgrade from gpt-4o


def main() -> None:
    workflow = create_workflow()

    print("=" * 60)
    print("LiteLLM Multi-Provider — Example 65")
    print("=" * 60)
    print(f"Prompt : {DEMO_PROMPT}")
    print(f"Budget : ${BUDGET_USD}")
    print()

    result = workflow.invoke(
        {
            "prompt": DEMO_PROMPT,
            "budget_usd": BUDGET_USD,
            "chosen_model": "",
            "answer": "",
            "comparison": [],
        }
    )

    print(f"Model chosen : {result['chosen_model']}")
    print(f"Answer       : {result['answer']}")
    print()

    if result["comparison"]:
        print(f"{'Provider':<35} {'Cost USD':>12} {'Latency':>10}")
        print("-" * 60)
        for r in result["comparison"]:
            print(
                f"{r['model']:<35} ${r['cost_usd']:>10.6f}"
                f" {r['latency_ms']:>8.0f}ms"
            )


if __name__ == "__main__":
    main()
