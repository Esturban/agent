import re


def split_sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def score_sentences(sentences: list[str], query: str, client, model: str = "gpt-4o-mini") -> list[tuple[float, str]]:
    """Score each sentence 0–1 for relevance to query using LLM."""
    prompt = (
        f"Query: {query}\n\n"
        "Rate each sentence's relevance to the query from 0.0 (irrelevant) to 1.0 (highly relevant).\n"
        "Reply with one float per line, one per sentence, in order.\n\n"
        + "\n".join(f"{i+1}. {s}" for i, s in enumerate(sentences))
    )
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=len(sentences) * 8,
    )
    scores = []
    for line in resp.choices[0].message.content.strip().splitlines():
        try:
            scores.append(float(line.strip().split()[-1]))
        except (ValueError, IndexError):
            scores.append(0.5)
    return list(zip(scores, sentences))


def compress(chunks: list[str], query: str, client, ratio: float = 0.4) -> str:
    """Keep the top `ratio` fraction of sentences by relevance score."""
    all_sentences = []
    for chunk in chunks:
        all_sentences.extend(split_sentences(chunk))
    scored = score_sentences(all_sentences, query, client)
    scored.sort(key=lambda x: x[0], reverse=True)
    keep_n = max(1, int(len(scored) * ratio))
    kept = [s for _, s in scored[:keep_n]]
    return " ".join(kept)


def count_tokens(text: str) -> int:
    """Rough token estimate: ~4 chars per token."""
    return len(text) // 4
