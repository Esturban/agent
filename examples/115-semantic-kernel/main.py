from dotenv import load_dotenv

load_dotenv()

from src.workflow import create_workflow, run_task_sync  # noqa: E402


RESEARCH_GOALS = [
    "Search for information about climate change and give me a 2-sentence summary of the key facts.",
    "Find out about large language models and extract the 3 most important points.",
    "Search for renewable energy information and summarize what you find.",
]


def main() -> None:
    print("=== 115 — Semantic Kernel: Plugins and Auto Function Calling ===\n")
    print("Building kernel with WebSearch and Summarizer plugins...\n")

    kernel = create_workflow()

    print(f"Registered plugins: {list(kernel.plugins.keys())}\n")

    for i, goal in enumerate(RESEARCH_GOALS, 1):
        print(f"{'=' * 65}")
        print(f"Task {i}: {goal}")
        print("-" * 65)

        result = run_task_sync(kernel, goal)

        print(f"Response:\n{result['response']}")
        print()

    print("=" * 65)
    print("\nKey insight:")
    print("The Kernel selected and sequenced plugin calls automatically.")
    print("Compare to LangGraph: here the orchestration is implicit (inside the")
    print("LLM's function-calling loop), not an explicit graph you define.")


if __name__ == "__main__":
    main()
