import time


def call_no_cache(system: str, question: str, client) -> dict:
    start = time.time()
    resp = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=256,
        system=system,
        messages=[{"role": "user", "content": question}],
    )
    return {
        "answer": resp.content[0].text,
        "input_tokens": resp.usage.input_tokens,
        "cache_read": 0,
        "latency_ms": round((time.time() - start) * 1000),
    }


def call_with_cache(system: str, question: str, client) -> dict:
    start = time.time()
    resp = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=256,
        system=[{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": question}],
    )
    cache_read = getattr(resp.usage, "cache_read_input_tokens", 0) or 0
    return {
        "answer": resp.content[0].text,
        "input_tokens": resp.usage.input_tokens,
        "cache_read": cache_read,
        "latency_ms": round((time.time() - start) * 1000),
    }


def compute_savings(uncached: list[dict], cached: list[dict]) -> dict:
    cost_per_mtok = 0.25  # Haiku input price $/MTok
    uncached_tok = sum(r["input_tokens"] for r in uncached)
    cached_tok = sum(r["input_tokens"] - r["cache_read"] for r in cached)
    saved_tok = uncached_tok - cached_tok
    return {
        "uncached_total_input_tokens": uncached_tok,
        "cached_total_billed_tokens": cached_tok,
        "tokens_saved": saved_tok,
        "estimated_savings_usd": round(saved_tok / 1_000_000 * cost_per_mtok, 6),
        "avg_latency_uncached_ms": round(sum(r["latency_ms"] for r in uncached) / len(uncached)),
        "avg_latency_cached_ms": round(sum(r["latency_ms"] for r in cached) / len(cached)),
    }
