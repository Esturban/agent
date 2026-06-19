"""
131 — Multi-Agent Trust Propagation
====================================
Demonstrates how trust should degrade as it propagates through a multi-agent
pipeline — and how to block privilege escalation attacks at each hop.

Key concepts:
  - TrustLevel (SYSTEM > OPERATOR > USER > UNTRUSTED)
  - TTL hop-count: each delegation decrements ttl_hops; at 0, pipeline halts
  - Verifier layer: subagent output is verified before orchestrator acts on it
  - Injection via tool output: attacker claims elevated privilege in env data

Based on: OpenAI Instruction Hierarchy (arxiv:2404.13208)
          and multi-agent compromise research (arxiv:2502.10236)
"""

from dotenv import load_dotenv

load_dotenv()

from src.trust_context import root_context
from src.orchestrator import SCENARIOS, run_scenario

GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
BOLD   = "\033[1m"
RESET  = "\033[0m"


def main():
    print(f"\n{BOLD}=== 131 — Multi-Agent Trust Propagation ==={RESET}")
    print("Papers: arxiv:2404.13208 (OpenAI), arxiv:2502.10236\n")

    base_ctx = root_context(
        allowed_actions=["summarize", "translate", "fetch_report", "store_result"],
        forbidden_actions=["send_email", "delete_records", "export_customer_data"],
        ttl_hops=3,
    )
    print(f"Root context: {base_ctx.summary()}\n")
    print("-" * 70)

    results = []
    for scenario in SCENARIOS:
        print(f"\n[{scenario['name']}]")
        result = run_scenario(scenario, base_ctx)
        results.append(result)

        if "ttl_error" in result:
            status = GREEN if result["correct"] else RED
            label = "BLOCKED (TTL)" if result["correct"] else "WRONG"
            print(f"  {status}{label}{RESET} — {result['ttl_error'][:80]}")
        elif "verifier_clean" in result:
            status = GREEN if result["correct"] else RED
            label = "CORRECT" if result["correct"] else "WRONG"
            clean_str = "CLEAN" if result["verifier_clean"] else f"VIOLATION:{result['violation_type']}"
            print(f"  {status}{label}{RESET} | verifier={clean_str}")
            print(f"  Trust chain: {result.get('trust_chain', '')}")
            if result.get("verifier_explanation"):
                print(f"  Explanation: {result['verifier_explanation'][:100]}")
        else:
            print(f"  ERROR: {result.get('error', 'unknown')}")

    print("\n" + "=" * 70)
    correct = sum(1 for r in results if r.get("correct", False))
    total = len(results)
    pct = GREEN if correct == total else YELLOW
    print(f"\n{BOLD}Results: {pct}{correct}/{total} scenarios handled correctly{RESET}")
    print()
    print(f"{BOLD}Key lessons:{RESET}")
    print("  1. Trust MUST degrade at every hop — subagents can't inherit full SYSTEM trust.")
    print("  2. ttl_hops prevents unbounded recursive delegation (pipeline bomb).")
    print("  3. Injected instructions claiming elevated privilege must be rejected by policy,")
    print("     not by model judgment alone — the verifier enforces this structurally.")
    print("  4. The verifier is the trust boundary: every subagent output crosses it")
    print("     before the orchestrator acts. Never skip it for performance.")


if __name__ == "__main__":
    main()
