import json
import os
from dotenv import load_dotenv
from src.workflow import create_workflow

load_dotenv()

if __name__ == "__main__":
    workflow = create_workflow()

    state = {
        "model_name": "HuggingFaceTB/SmolLM2-135M-Instruct",
        "lora_rank": 8,
        "n_steps": 30,
        "vram_before_mb": 0.0,
        "vram_after_mb": 0.0,
        "param_stats": {},
        "final_loss": 0.0,
    }

    print(f"Training {state['model_name']} with 4-bit QLoRA (r={state['lora_rank']})...\n")
    result = workflow(state)

    print(f"VRAM before: {result['vram_before_mb']:.0f} MB")
    print(f"VRAM after:  {result['vram_after_mb']:.0f} MB")
    print(f"\nTrainable params: {json.dumps(result['param_stats'], indent=2)}")
    print(f"\nFinal loss: {result['final_loss']}")
    print(f"\nQLoRA keeps {result['param_stats'].get('pct', 0):.4f}% of params trainable.")
