import numpy as np
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

GOLDEN_QA_SET = [
    {"question": "What is the capital of France?", "expected": "Paris"},
    {"question": "What is 2 + 2?", "expected": "4"},
    {"question": "Who wrote Romeo and Juliet?", "expected": "Shakespeare"},
    {"question": "What is the boiling point of water in Celsius?", "expected": "100"},
    {"question": "What planet is closest to the Sun?", "expected": "Mercury"},
]

_agent_llm = ChatOpenAI(model="gpt-5-nano", temperature=0)
_embed_model = OpenAIEmbeddings(model="text-embedding-3-small")


def run_agent(question: str) -> str:
    response = _agent_llm.invoke([HumanMessage(content=f"Answer briefly in one sentence: {question}")])
    return response.content.strip()


def evaluate_answer(expected: str, actual: str) -> dict:
    exact_match = expected.lower() in actual.lower()

    exp_vec = np.array(_embed_model.embed_query(expected))
    act_vec = np.array(_embed_model.embed_query(actual))
    cosine_sim = float(np.dot(exp_vec, act_vec) / (np.linalg.norm(exp_vec) * np.linalg.norm(act_vec)))
    semantic_match = cosine_sim >= 0.80

    return {
        "exact_match": exact_match,
        "semantic_match": semantic_match,
        "cosine_similarity": round(cosine_sim, 4),
        "score": 1.0 if (exact_match or semantic_match) else round(cosine_sim, 4),
    }
