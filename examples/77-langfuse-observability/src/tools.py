import os

LANGFUSE_HOST = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")

SAMPLE_TASKS = [
    "What is machine learning in one sentence?",
    "Explain neural networks in one sentence.",
    "What is gradient descent in one sentence?",
    "What is overfitting in one sentence?",
    "What is a transformer model in one sentence?",
]
