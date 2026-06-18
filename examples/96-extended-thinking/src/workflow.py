import os
import anthropic
from .tools import MODEL, THINKING_BUDGET


def ask(prompt: str, thinking: bool) -> dict:
    """Call Claude with or without the extended thinking scratchpad.

    With thinking enabled the response contains two ContentBlocks:
      - ThinkingBlock  (type='thinking')  — private chain-of-thought, not shown to users
      - TextBlock      (type='text')      — the final answer returned to the caller
    max_tokens must cover both thinking and text, so we size it generously.
    """
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    kwargs: dict = {
        "model":    MODEL,
        "messages": [{"role": "user", "content": prompt}],
        # When thinking is on, max_tokens must be >= budget_tokens.
        "max_tokens": THINKING_BUDGET + 2048 if thinking else 1024,
    }
    if thinking:
        kwargs["thinking"] = {"type": "enabled", "budget_tokens": THINKING_BUDGET}

    response = client.messages.create(**kwargs)

    thinking_text = ""
    answer = ""
    for block in response.content:
        if block.type == "thinking":
            thinking_text = block.thinking
        elif block.type == "text":
            answer = block.text

    return {
        "answer":           answer.strip(),
        "thinking_preview": thinking_text[:300] if thinking_text else "",
        "thinking_words":   len(thinking_text.split()) if thinking_text else 0,
        "output_tokens":    response.usage.output_tokens,
    }
