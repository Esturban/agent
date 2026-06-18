from dotenv import load_dotenv

from src.tools import N_ATTACKS, SEED_GOAL
from src.workflow import create_workflow

load_dotenv()


def main() -> None:
    print(f"Red-team goal : {SEED_GOAL}")
    print(f"Attack chains : {N_ATTACKS} (parallel)")
    print("=" * 60)

    app = create_workflow()
    result = app.invoke({
        "goal": SEED_GOAL,
        "results": [],
        "attack_success_rate": 0.0,
    })

    for i, r in enumerate(result["results"], 1):
        status = "SUCCEEDED" if r["success"] else "blocked"
        print(f"\n[{i}] {status}")
        print(f"     Attack : {r['attack']}")
        print(f"     Reason : {r['reason']}")

    asr = result["attack_success_rate"]
    print(f"\nAttack Success Rate: {asr:.0%} ({int(asr * N_ATTACKS)}/{N_ATTACKS} attacks succeeded)")


if __name__ == "__main__":
    main()
