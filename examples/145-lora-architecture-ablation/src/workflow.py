from typing import TypedDict
from .tools import make_lora_config, run_training_run

ABLATION_CONFIGS = [
    {"r": 4,  "target_modules": ["q_proj"],                     "label": "r4-q"},
    {"r": 8,  "target_modules": ["q_proj", "v_proj"],           "label": "r8-qv"},
    {"r": 16, "target_modules": ["q_proj", "v_proj"],           "label": "r16-qv"},
    {"r": 32, "target_modules": ["q_proj", "v_proj", "o_proj"], "label": "r32-qvo"},
]


class AblationState(TypedDict):
    model_name: str
    n_steps: int
    results: list[dict]


def run_ablation(state: AblationState) -> AblationState:
    results = []
    for cfg in ABLATION_CONFIGS:
        lora_cfg = make_lora_config(cfg["r"], cfg["target_modules"])
        outcome = run_training_run(state["model_name"], lora_cfg, state.get("n_steps", 20))
        results.append({"label": cfg["label"], "r": cfg["r"],
                        "targets": cfg["target_modules"], **outcome})
    return {**state, "results": results}


def create_workflow():
    def run(state: AblationState) -> AblationState:
        return run_ablation(state)
    return run
