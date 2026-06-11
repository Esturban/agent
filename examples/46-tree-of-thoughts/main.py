from dotenv import load_dotenv

from src.tools import N_BRANCHES, SAMPLE_PROBLEMS
from src.workflow import create_workflow


def main():
    load_dotenv()
    app = create_workflow()

    for problem in SAMPLE_PROBLEMS:
        print(f"\nPROBLEM: {problem}")
        print("─" * 60)
        result = app.invoke({"problem": problem, "branches": [], "best_thought": "", "final_answer": ""})
        print(f"\nBranch scores:")
        for b in sorted(result["branches"], key=lambda x: x["score"], reverse=True):
            print(f"  Branch {b['branch_id']+1}: {b['score']}/10")
        print(f"\nFinal Answer (from best of {N_BRANCHES} branches):")
        print(result["final_answer"][:500])


if __name__ == "__main__":
    main()
