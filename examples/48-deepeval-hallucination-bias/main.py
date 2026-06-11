from dotenv import load_dotenv

from src.tools import HALLUCINATION_CASES
from src.workflow import create_grounded_workflow, create_freeform_workflow


def main():
    load_dotenv()
    grounded = create_grounded_workflow()
    freeform = create_freeform_workflow()

    print("Comparing grounded vs freeform outputs:\n")
    for case in HALLUCINATION_CASES:
        q = "What can you tell me about this topic?"
        g = grounded.invoke({"input": q, "context": case["context"], "output": ""})
        f = freeform.invoke({"input": q, "context": [], "output": ""})
        print(f"Context: {case['context'][0][:80]}...")
        print(f"Grounded: {g['output'][:150]}")
        print(f"Freeform: {f['output'][:150]}\n")


if __name__ == "__main__":
    main()
