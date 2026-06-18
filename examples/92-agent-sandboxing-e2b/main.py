from dotenv import load_dotenv

load_dotenv()

from src.tools import CODING_TASKS  # noqa: E402
from src.workflow import create_workflow  # noqa: E402


def main() -> None:
    print("=== 92 · Agent Sandboxing — E2B ===")
    print("Docs: e2b.dev | Requires: E2B_API_KEY\n")
    print("All code executes in an isolated cloud microVM — nothing runs on this host.\n")

    app = create_workflow()

    for task in CODING_TASKS:
        print(f"Task: {task}")
        print("-" * 60)

        result = app.invoke({
            "task": task,
            "code": "",
            "stdout": "",
            "stderr": "",
            "interpretation": "",
        })

        # Show the generated code.
        print("Generated code:")
        for line in result["code"].split("\n"):
            print(f"  {line}")

        # Show sandbox output — distinguish success from error.
        if result["stderr"]:
            print(f"\nSandbox STDERR:\n  {result['stderr'][:200]}")
        if result["stdout"]:
            print(f"\nSandbox STDOUT:\n  {result['stdout'][:200]}")

        print(f"\nInterpretation: {result['interpretation']}")
        print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
