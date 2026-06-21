from dotenv import load_dotenv

load_dotenv()

from src.workflow import create_workflow, run_questions  # noqa: E402


def main() -> None:
    print("=== 116 — LlamaIndex ReAct Agent over Multi-Document Collection ===\n")
    print("Building 3 VectorStoreIndex instances (science, history, technology)...")
    print("Wrapping as QueryEngineTool objects and creating ReActAgent...\n")

    agent, questions = create_workflow()

    print(f"Agent tools: science_tool, history_tool, technology_tool")
    print(f"Questions to answer: {len(questions)}\n")

    results = run_questions(agent, questions)

    for i, r in enumerate(results, 1):
        print(f"{'=' * 65}")
        print(f"Q{i}: {r['question']}")
        print(f"Routing: {r['routing_note']}")
        print(f"\nAnswer:\n{r['answer'][:500]}")
        if len(r["answer"]) > 500:
            print("... [truncated]")
        print()

    print("=" * 65)
    print("\nKey insight:")
    print("LlamaIndex wraps the ReAct loop internally — you see tool routing")
    print("happen automatically. LangGraph makes the same loop explicit as nodes.")


if __name__ == "__main__":
    main()
