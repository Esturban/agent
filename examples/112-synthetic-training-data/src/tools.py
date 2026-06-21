import json
from dataclasses import dataclass, field

import numpy as np
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import SystemMessage, HumanMessage


LABELS = ["formal", "informal", "urgent"]

GENERATOR_SYSTEM = (
    "You are a dataset generator creating diverse, realistic customer service messages "
    "for a tone classification training set. "
    "Generate messages that vary in phrasing, length, context, and industry "
    "while clearly belonging to the requested tone class. "
    "Each message should be 1-3 sentences. Be creative and avoid repetition."
)

JUDGE_SYSTEM = (
    "You are a dataset quality judge. "
    "Given a customer service message and its assigned label, decide if the label is correct "
    "and the message is clear. "
    'Reply with JSON only: {"valid": true/false, "reason": "one sentence"}.'
)


@dataclass
class GeneratedExample:
    message: str
    label: str
    is_valid: bool = True
    judge_reason: str = ""
    embedding: list[float] = field(default_factory=list)


def generate_examples_for_label(label: str, n: int, llm: ChatOpenAI) -> list[str]:
    """
    Use GPT-4o to generate N diverse examples for a given label.
    Varies industry and phrasing to maximize diversity.
    """
    prompt = (
        f"Generate {n} diverse customer service messages that have a clearly '{label}' tone.\n"
        "Requirements:\n"
        "- Each message should be on its own line\n"
        "- Vary the industry, product type, and phrasing\n"
        "- Include a mix of short (1 sentence) and medium (2-3 sentence) messages\n"
        "- Make each message distinctly different from the others\n"
        f"- Number each message: 1. ... 2. ...\n\n"
        f"Generate {n} messages now:"
    )
    response = llm.invoke([
        SystemMessage(content=GENERATOR_SYSTEM),
        HumanMessage(content=prompt),
    ])
    raw = response.content.strip()

    examples = []
    for line in raw.split("\n"):
        line = line.strip()
        if not line:
            continue
        for i in range(1, n + 10):
            prefix = f"{i}. "
            if line.startswith(prefix):
                line = line[len(prefix):].strip()
                break
        if len(line) > 10:
            examples.append(line)

    return examples[:n]


def embed_examples(texts: list[str], embeddings: OpenAIEmbeddings) -> list[list[float]]:
    """Embed a list of texts using OpenAI text-embedding-3-small."""
    return embeddings.embed_documents(texts)


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Compute cosine similarity between two embedding vectors."""
    a_arr = np.array(a, dtype=float)
    b_arr = np.array(b, dtype=float)
    denom = np.linalg.norm(a_arr) * np.linalg.norm(b_arr)
    if denom == 0:
        return 0.0
    return float(np.dot(a_arr, b_arr) / denom)


def deduplicate_by_embedding(
    examples: list[GeneratedExample],
    threshold: float = 0.95,
) -> tuple[list[GeneratedExample], int]:
    """
    Remove near-duplicate examples using cosine similarity.
    Any pair with similarity > threshold → drop the later one.
    Returns (deduplicated_examples, n_dropped).
    """
    kept: list[GeneratedExample] = []
    dropped = 0
    for candidate in examples:
        if not candidate.embedding:
            kept.append(candidate)
            continue
        too_similar = any(
            cosine_similarity(candidate.embedding, existing.embedding) > threshold
            for existing in kept
            if existing.embedding
        )
        if too_similar:
            dropped += 1
        else:
            kept.append(candidate)
    return kept, dropped


def judge_example(example: GeneratedExample, llm: ChatOpenAI) -> GeneratedExample:
    """
    Second LLM call to validate label correctness and message clarity.
    Updates example.is_valid and example.judge_reason in place.
    """
    prompt = (
        f"Message: {example.message}\n"
        f"Label: {example.label}\n\n"
        "Is this label correct and is the message unambiguous? "
        'Reply with JSON only: {"valid": true/false, "reason": "one sentence"}'
    )
    response = llm.invoke([
        SystemMessage(content=JUDGE_SYSTEM),
        HumanMessage(content=prompt),
    ])
    try:
        data = json.loads(response.content.strip())
        example.is_valid = bool(data.get("valid", True))
        example.judge_reason = data.get("reason", "")
    except (json.JSONDecodeError, KeyError):
        example.is_valid = True
        example.judge_reason = "judge parse error — kept"
    return example


def export_to_jsonl(examples: list[GeneratedExample], path: str) -> int:
    """
    Export valid examples as JSONL in OpenAI fine-tuning format.
    Returns count of exported examples.
    """
    system_msg = (
        "You are a tone classifier for customer service messages. "
        "Classify each message as exactly one of: formal, informal, urgent. "
        "Reply with only the label — no explanation."
    )
    count = 0
    with open(path, "w") as f:
        for ex in examples:
            if not ex.is_valid:
                continue
            row = {
                "messages": [
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": ex.message},
                    {"role": "assistant", "content": ex.label},
                ]
            }
            f.write(json.dumps(row) + "\n")
            count += 1
    return count
