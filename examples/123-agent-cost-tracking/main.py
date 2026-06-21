"""
123 — Agent Cost Tracking
Entry point: run 3-node agent with cost tracking and budget enforcement.
Run: python examples/123-agent-cost-tracking/main.py
"""

from dotenv import load_dotenv

load_dotenv()

from src.workflow import create_workflow


def main():
    print("=== 123 — Agent Cost Tracking ===")
    print("Per-node token counting via tiktoken + budget enforcement in LangGraph\n")
    result = create_workflow(max_budget_usd=0.05)
    print(f"\nFinal summary: {result['summary'][:150]}...")
    report = result["cost_report"]
    print(f"\nTotal cost: ${report['total_cost_usd']:.6f}")
    print(f"Tokens used: {report['total_input_tokens'] + report['total_output_tokens']} total")


if __name__ == "__main__":
    main()
