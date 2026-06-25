import os
from dotenv import load_dotenv
from src.workflow import create_workflow

load_dotenv()

if __name__ == "__main__":
    workflow = create_workflow()

    state = {
        "model_a": "HuggingFaceTB/SmolLM2-135M-Instruct",
        "model_b": "HuggingFaceTB/SmolLM2-360M-Instruct",
        "t": 0.5,
        "outputs_a": [],
        "outputs_b": [],
        "outputs_merged": [],
    }

    print(f"Merging: {state['model_a']} + {state['model_b']}")
    print(f"SLERP coefficient t={state['t']} (0.0=A, 1.0=B)\n")
    result = workflow(state)

    prompts = [
        "What is the capital of France?",
        "Explain gradient descent in one sentence.",
        "Write a haiku about Python.",
    ]
    for i, prompt in enumerate(prompts):
        print(f"Prompt: {prompt}")
        print(f"  Model A: {result['outputs_a'][i][:80]}")
        print(f"  Model B: {result['outputs_b'][i][:80]}")
        print(f"  Merged:  {result['outputs_merged'][i][:80]}\n")
