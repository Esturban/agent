USER_ID = "demo-user-001"

SESSION_1_MESSAGES = [
    {"role": "user", "content": "Hi, I'm Alice. I prefer Python over Java."},
    {"role": "assistant", "content": "Got it, Alice! I'll keep Python in mind."},
    {"role": "user", "content": "I also like concise code — no boilerplate."},
    {"role": "assistant", "content": "Noted. Concise and Pythonic it is."},
]

SESSION_2_QUERIES = [
    "What programming language do I prefer?",
    "What is my name?",
    "What coding style do I like?",
]


def format_memories(memories: list) -> str:
    if not memories:
        return "  (no memories found)"
    lines = []
    for i, m in enumerate(memories, 1):
        memory_text = m.get("memory", m.get("text", str(m)))
        score = m.get("score", m.get("similarity", ""))
        score_str = f"  [score={score:.3f}]" if isinstance(score, float) else ""
        lines.append(f"  {i}. {memory_text}{score_str}")
    return "\n".join(lines)
