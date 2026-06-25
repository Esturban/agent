import math
import time
from dataclasses import dataclass, field


def embed(text: str, client) -> list[float]:
    resp = client.embeddings.create(model="text-embedding-3-small", input=text)
    return resp.data[0].embedding


def cosine_sim(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    return dot / (norm_a * norm_b + 1e-10)


@dataclass
class SemanticCache:
    threshold: float = 0.92
    _entries: list = field(default_factory=list)
    hits: int = 0
    misses: int = 0

    def get(self, query_vec: list[float]) -> str | None:
        for vec, response in self._entries:
            if cosine_sim(query_vec, vec) >= self.threshold:
                self.hits += 1
                return response
        self.misses += 1
        return None

    def set(self, query_vec: list[float], response: str) -> None:
        self._entries.append((query_vec, response))

    def stats(self) -> dict:
        total = self.hits + self.misses
        return {
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": round(self.hits / total, 3) if total else 0,
        }


def ask_llm(question: str, client, model: str = "gpt-4o-mini") -> tuple[str, float]:
    start = time.time()
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": question}],
        max_tokens=256,
    )
    return resp.choices[0].message.content, round((time.time() - start) * 1000)
