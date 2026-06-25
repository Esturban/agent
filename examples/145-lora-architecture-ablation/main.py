import os
from dotenv import load_dotenv
from src.workflow import create_workflow

load_dotenv()

if __name__ == "__main__":
    workflow = create_workflow()

    state = {
        "model_name": "HuggingFaceTB/SmolLM2-135M-Instruct",
        "n_steps": 20,
        "results": [],
    }

    print(f"Running LoRA ablation on {state['model_name']}...\n")
    result = workflow(state)

    print(f"{'Label':<12} {'Rank':<6} {'Targets':<30} {'Trainable%':<12} {'Loss'}")
    print("-" * 72)
    for r in result["results"]:
        targets = "+".join(r["targets"])
        pct = r["params"]["pct"]
        print(f"{r['label']:<12} {r['r']:<6} {targets:<30} {pct:<12.4f} {r['final_loss']}")
