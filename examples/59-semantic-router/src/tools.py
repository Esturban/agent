import numpy as np
from langchain_openai import OpenAIEmbeddings

SIMILARITY_THRESHOLD = 0.6

ROUTES = {
    "code": [
        "How do I write a Python function?",
        "Debug my code",
        "What is a list comprehension?",
        "Explain async/await in Python",
        "How do I use pandas DataFrames?",
    ],
    "billing": [
        "How do I upgrade my plan?",
        "What does the pro subscription include?",
        "Can I get a refund?",
        "How much does the API cost?",
        "Where is my invoice?",
    ],
    "general": [
        "What is your company?",
        "Who made this product?",
        "What are your hours?",
        "How do I contact support?",
    ],
}

SAMPLE_QUERIES = [
    "How do I reverse a list in Python?",
    "I need to cancel my subscription",
    "What time do you open?",
    "Can you help me fix a syntax error?",
    "What are your pricing tiers?",
]


def cosine_similarity(a: list[float], b: list[float]) -> float:
    a_arr = np.array(a)
    b_arr = np.array(b)
    return float(np.dot(a_arr, b_arr) / (np.linalg.norm(a_arr) * np.linalg.norm(b_arr)))


def build_route_embeddings(embeddings: OpenAIEmbeddings) -> dict[str, list[list[float]]]:
    return {route: embeddings.embed_documents(phrases) for route, phrases in ROUTES.items()}


def find_best_route(query_vec: list[float], route_vecs: dict[str, list[list[float]]]) -> tuple[str, dict[str, float]]:
    scores: dict[str, float] = {}
    for route, vecs in route_vecs.items():
        scores[route] = max(cosine_similarity(query_vec, v) for v in vecs)
    best = max(scores, key=lambda r: scores[r])
    if scores[best] < SIMILARITY_THRESHOLD:
        best = "general"
    return best, scores
