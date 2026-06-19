"""
Example 129 — Tool Output Injection
Sources: arxiv:2503.15547, 2504.11703 (tool injection surveys)

What this shows:
  The attack surface for LLM agents is NOT the user — it's the environment.
  Tool outputs (API responses, search results, retrieved memory) are processed
  by the LLM as context, which means a compromised tool can inject instructions.

  This example shows 4 injection strategies across 4 tools:
    calculator   — extra 'system' key in JSON response
    web_search   — injection in one search snippet
    weather_api  — injection in the 'advisory' field
    memory_read  — injection in a stored value

  Two runs per query: undefended (LLM sees raw tool output) vs defended
  (validator scans tool output before it reaches the LLM).

What to watch:
  - Undefended agent often echoes or follows the injected instruction
  - Defended agent sanitizes the output and responds to the original query
  - The validator catches explicit keywords (layer 1) and semantic patterns (layer 2)

Run:
  python main.py
"""

from dotenv import load_dotenv
load_dotenv()

from tools.poisoned import calculator, web_search, weather_api, memory_read  # noqa: E402
from src.workflow import run_undefended, run_defended                          # noqa: E402

RED   = "\033[91m"
GREEN = "\033[92m"
BOLD  = "\033[1m"
DIM   = "\033[2m"
RESET = "\033[0m"

QUERIES = [
    ("What is 47 times 13?",       "calculator"),
    ("Find information about AI agents",  "web_search"),
    ("What is the weather in London?",    "weather_api"),
    ("What is my current session_id?",    "memory_read"),
]


def main() -> None:
    poisoned_tools = [calculator, web_search, weather_api, memory_read]

    print(f"{BOLD}Tool Output Injection (arxiv:2503.15547, 2504.11703){RESET}")
    print("The attack surface is the environment — tools, not the user.\n")

    for query, _ in QUERIES:
        print(f"{'─' * 60}")
        print(f"{BOLD}Query: {query}{RESET}\n")

        undefended = run_undefended(query, poisoned_tools)
        defended   = run_defended(query, poisoned_tools)

        safe_color = RED if not undefended["is_safe"] else GREEN
        print(f"{BOLD}Undefended:{RESET}")
        print(f"  Tool used  : {undefended['tool_used']}")
        print(f"  Raw output : {undefended['raw_output'][:100].replace(chr(10), ' ')}...")
        print(f"  Response   : {RED}{undefended['response'][:150].replace(chr(10), ' ')}{RESET}\n")

        print(f"{BOLD}Defended:{RESET}")
        safe_label = f"{GREEN}CLEAN{RESET}" if defended["is_safe"] else f"{RED}INJECTION DETECTED{RESET}"
        print(f"  Validation : {safe_label} — {defended['reason'][:80]}")
        print(f"  Response   : {GREEN}{defended['response'][:150].replace(chr(10), ' ')}{RESET}\n")

    print(f"\n{BOLD}Key lesson:{RESET}")
    print("The attack is in the tool's RETURN VALUE, not the user's input.")
    print("Validator layer runs between tool execution and LLM context injection.")
    print("See examples 127 (spotlighting) and 128 (hierarchy) for complementary defenses.")


if __name__ == "__main__":
    main()
