def get_bnb_config():
    from transformers import BitsAndBytesConfig
    import torch
    return BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.float16,
    )


def load_quantized_model(model_name: str, bnb_config):
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"
    model = AutoModelForCausalLM.from_pretrained(model_name, quantization_config=bnb_config, device_map="auto")
    return model, tokenizer


def get_vram_mb() -> float:
    try:
        import subprocess
        out = subprocess.check_output(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"])
        return float(out.decode().strip().split("\n")[0])
    except Exception:
        return 0.0


def count_trainable(model) -> dict:
    total = sum(p.numel() for p in model.parameters())
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    return {"trainable": trainable, "total": total, "pct": round(100 * trainable / total, 4)}


def load_sample_dataset(n: int = 50) -> list[dict]:
    qa_pairs = [
        ("What is gradient descent?", "Gradient descent is an optimization algorithm that iteratively adjusts parameters to minimize a loss function."),
        ("What is backpropagation?", "Backpropagation computes gradients of the loss with respect to each weight using the chain rule."),
        ("What is a transformer?", "A transformer is a neural network architecture using self-attention to process sequences in parallel."),
        ("What is overfitting?", "Overfitting occurs when a model learns training data too well, failing to generalize to new examples."),
        ("What is a learning rate?", "The learning rate controls how large a step the optimizer takes toward the gradient minimum each iteration."),
    ]
    return [{"prompt": q, "response": a} for q, a in qa_pairs * (n // len(qa_pairs) + 1)][:n]
