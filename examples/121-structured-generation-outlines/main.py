"""
121 — Structured Generation with Outlines
Entry point: demonstrate constrained decoding vs instructor retry.
Run: python examples/121-structured-generation-outlines/main.py
"""

from dotenv import load_dotenv

load_dotenv()

from src.workflow import create_workflow


def main():
    print("Key concept: outlines guarantees valid output via CFG sampling in one pass.")
    print("instructor uses tool-calling + Pydantic retry — may take multiple API calls.\n")
    result = create_workflow()
    print("\nDone. See workbook for full CFG sampling explanation.")


if __name__ == "__main__":
    main()
