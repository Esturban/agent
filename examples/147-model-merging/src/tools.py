import torch


def slerp(t: float, v0: torch.Tensor, v1: torch.Tensor) -> torch.Tensor:
    """Spherical linear interpolation between two weight tensors."""
    v0_f = v0.float()
    v1_f = v1.float()
    dot = (v0_f * v1_f).sum() / (v0_f.norm() * v1_f.norm() + 1e-8)
    dot = dot.clamp(-1, 1)
    omega = torch.acos(dot)
    if omega.abs() < 1e-4:
        return ((1 - t) * v0_f + t * v1_f).to(v0.dtype)
    so = torch.sin(omega)
    return (torch.sin((1 - t) * omega) / so * v0_f + torch.sin(t * omega) / so * v1_f).to(v0.dtype)


def merge_state_dicts(sd_a: dict, sd_b: dict, t: float) -> dict:
    """Merge two model state dicts with SLERP at coefficient t."""
    merged = {}
    for key in sd_a:
        if key in sd_b and sd_a[key].shape == sd_b[key].shape and sd_a[key].is_floating_point():
            merged[key] = slerp(t, sd_a[key], sd_b[key])
        else:
            merged[key] = sd_a[key]
    return merged


def generate(model, tokenizer, prompt: str, max_new_tokens: int = 64) -> str:
    inputs = tokenizer(prompt, return_tensors="pt")
    with torch.no_grad():
        out = model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False, pad_token_id=tokenizer.eos_token_id)
    return tokenizer.decode(out[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True).strip()


def eval_on_prompts(model, tokenizer, prompts: list[str]) -> list[str]:
    return [generate(model, tokenizer, p) for p in prompts]
