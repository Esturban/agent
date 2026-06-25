import os
from dotenv import load_dotenv
from src.workflow import create_workflow

load_dotenv()

if __name__ == "__main__":
    workflow = create_workflow()

    state = {
        "model_name": "HuggingFaceTB/SmolLM2-135M-Instruct",
        "n_train_pairs": 20,
        "max_steps": 30,
        "preference_rate_before": 0.0,
        "preference_rate_after": 0.0,
        "final_loss": 0.0,
    }

    print(f"ORPO alignment on {state['model_name']}")
    print(f"Training steps: {state['max_steps']}, pairs: {state['n_train_pairs']}\n")
    result = workflow(state)

    print(f"Preference rate before: {result['preference_rate_before']:.1%}")
    print(f"Preference rate after:  {result['preference_rate_after']:.1%}")
    delta = result["preference_rate_after"] - result["preference_rate_before"]
    print(f"Improvement:            {delta:+.1%}")
    print(f"Final loss:             {result['final_loss']}")
