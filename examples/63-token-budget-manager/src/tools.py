import tiktoken

BUDGET_LIMIT = 800

RESEARCH_TOPIC = "Explain the history and key contributions of neural networks"

RESEARCH_STEPS = [
    "Step 1: Briefly describe the perceptron (1958) and its limitations.",
    "Step 2: Explain the backpropagation breakthrough (1986).",
    "Step 3: Describe the deep learning revolution (2012, AlexNet).",
    "Step 4: Summarize the transformer architecture (2017, Attention is All You Need).",
]

_enc = tiktoken.encoding_for_model("gpt-4o")


def count_tokens(text: str) -> int:
    return len(_enc.encode(text))
