from typing import TypedDict
from .tools import build_preference_dataset, get_orpo_config, eval_preference_rate


class ORPOState(TypedDict):
    model_name: str
    n_train_pairs: int
    max_steps: int
    preference_rate_before: float
    preference_rate_after: float
    final_loss: float


def run_orpo(state: ORPOState) -> ORPOState:
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from trl import ORPOTrainer

    tokenizer = AutoTokenizer.from_pretrained(state["model_name"])
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    model = AutoModelForCausalLM.from_pretrained(state["model_name"])
    dataset = build_preference_dataset(state.get("n_train_pairs", 20))

    rate_before = eval_preference_rate(model, tokenizer, dataset)

    orpo_cfg = get_orpo_config("/tmp/orpo", state.get("max_steps", 30))
    trainer = ORPOTrainer(model=model, args=orpo_cfg,
                          train_dataset=dataset, tokenizer=tokenizer)
    result = trainer.train()
    rate_after = eval_preference_rate(model, tokenizer, dataset)

    return {**state, "preference_rate_before": rate_before,
            "preference_rate_after": rate_after,
            "final_loss": round(result.training_loss, 4)}


def create_workflow():
    def run(state: ORPOState) -> ORPOState:
        return run_orpo(state)
    return run
