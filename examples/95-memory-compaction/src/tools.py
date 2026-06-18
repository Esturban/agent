HOT_TIER_MAX = 6   # verbatim turns before compaction fires
WARM_TIER_MAX = 4  # summary blocks before oldest archive to cold

DEMO_TURNS = [
    "My name is Alex and I'm building a trading bot.",
    "Remember that I only trade ETH, never BTC.",
    "What's the difference between a limit order and a market order?",
    "I'm using Binance as my exchange.",
    "Remember that my risk tolerance is low — max 2% per trade.",
    "Explain slippage to me.",
    "What timeframes work best for ETH?",
    "Don't forget I'm based in Canada so tax rules matter.",
    "How do I calculate position size?",
    "What is the Kelly criterion?",
    "I prefer 4H and daily charts.",
    "How do stop losses interact with volatility?",
]


def importance_score(turn: dict) -> float:
    """Recency × (1 + boost) — explicit memory cues ('remember', 'never') lift score."""
    recency = turn.get("recency", 0.5)
    content = turn.get("content", "").lower()
    cues = {"remember", "don't forget", "never", "always", "important"}
    boost = 0.4 if any(c in content for c in cues) else 0.0
    return min(1.0, recency + boost)


def build_context(hot: list[dict], warm: list[dict]) -> str:
    """Concatenate warm summaries then recent verbatim turns into a single context block."""
    lines = []
    if warm:
        lines.append("=== Summarized history ===")
        for block in warm:
            lines.append(block["summary"])
    if hot:
        lines.append("=== Recent turns ===")
        for t in hot:
            lines.append(f"{t['role']}: {t['content']}")
    return "\n".join(lines)
