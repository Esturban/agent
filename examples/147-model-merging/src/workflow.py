from typing import TypedDict
from .tools import merge_state_dicts, eval_on_prompts

EVAL_PROMPTS = [
    "What is the capital of France?",
    "Explain gradient descent in one sentence.",
    "Write a haiku about Python.",
]


class MergeState(TypedDict):
    model_a: str
    model_b: str
    t: float
    outputs_a: list[str]
    outputs_b: list[str]
    outputs_merged: list[str]


def run_merge(state: MergeState) -> MergeState:
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer_a = AutoTokenizer.from_pretrained(state["model_a"])
    tokenizer_b = AutoTokenizer.from_pretrained(state["model_b"])

    model_a = AutoModelForCausalLM.from_pretrained(state["model_a"])
    model_b = AutoModelForCausalLM.from_pretrained(state["model_b"])

    outputs_a = eval_on_prompts(model_a, tokenizer_a, EVAL_PROMPTS)
    outputs_b = eval_on_prompts(model_b, tokenizer_b, EVAL_PROMPTS)

    merged_sd = merge_state_dicts(model_a.state_dict(), model_b.state_dict(), state.get("t", 0.5))
    model_a.load_state_dict(merged_sd)
    outputs_merged = eval_on_prompts(model_a, tokenizer_a, EVAL_PROMPTS)

    return {**state, "outputs_a": outputs_a, "outputs_b": outputs_b, "outputs_merged": outputs_merged}


def create_workflow():
    def run(state: MergeState) -> MergeState:
        return run_merge(state)
    return run
