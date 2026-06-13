VARIANT_A_PROMPT = (
    "You are a concise assistant. Answer the following question in exactly one short sentence: {question}"
)

VARIANT_B_PROMPT = (
    "You are a thorough assistant. Provide a detailed, informative answer to the following question, "
    "explaining the key concepts clearly: {question}"
)

TEST_INPUTS = [
    "What is photosynthesis?",
    "How does the internet work?",
    "What is quantum entanglement?",
    "Why is the sky blue?",
    "What is the difference between RAM and storage?",
]


def score_response(response: str) -> float:
    word_count = len(response.split())
    return round(min(word_count / 100, 1.0), 4)
