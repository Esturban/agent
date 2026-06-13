from smolagents import CodeAgent, OpenAIServerModel

from src.tools import RISKY_CODE_EXAMPLE, multiply, word_count

_MODEL = OpenAIServerModel(model_id="gpt-5-nano")


def create_agent(safe_mode: bool = True) -> CodeAgent:
    kwargs: dict = {}
    if safe_mode:
        kwargs["additional_authorized_imports"] = ["math"]
    return CodeAgent(tools=[multiply, word_count], model=_MODEL, **kwargs)


def run_sandboxed_demo() -> None:
    print("=" * 60)
    print("SANDBOXING: THE CORE SECURITY CONCERN")
    print("=" * 60)
    print("CodeAgent executes real Python locally. Without restrictions,")
    print("a model could generate and run:")
    print()
    print(RISKY_CODE_EXAMPLE)

    print("MITIGATION: additional_authorized_imports restricts imports.")
    print("  agent = CodeAgent(..., additional_authorized_imports=['math'])")
    print("  Any other import raises ImportError during execution.")
    print()

    # Demonstrate the restriction in action
    restricted_agent = create_agent(safe_mode=True)
    print("--- Trying an unauthorized import task on the restricted agent ---")
    try:
        result = restricted_agent.run(
            "Use the os module to print the current working directory."
        )
        print(f"Result: {result}")
    except Exception as exc:
        print(f"BLOCKED as expected: {type(exc).__name__}: {exc}")
    print()
