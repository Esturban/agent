"""Tool definitions for the LiteLLM multi-provider example.

Provides:
- PROVIDERS: list of (env_var, model_string) tuples for every supported provider
- call_provider: call one provider and return a result dict with cost + latency
- compare_providers: run a prompt across all available providers
- smart_completion: cost-threshold fallback between preferred and cheap model
"""

import os
import time

import litellm
from litellm import completion, completion_cost

litellm.set_verbose = False

PROVIDERS = [
    ("OPENAI_API_KEY", "openai/gpt-4o-mini"),
    ("ANTHROPIC_API_KEY", "anthropic/claude-haiku-4-5"),
    ("GEMINI_API_KEY", "gemini/gemini-1.5-flash"),
    ("COHERE_API_KEY", "cohere/command-r"),
]


def call_provider(model_str: str, prompt: str, max_tokens: int = 80) -> dict:
    """Call a single LiteLLM-supported model and return a structured result."""
    t0 = time.perf_counter()
    resp = completion(
        model=model_str,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
    )
    latency_ms = (time.perf_counter() - t0) * 1000
    cost = completion_cost(completion_response=resp)
    return {
        "model": model_str,
        "answer": resp.choices[0].message.content,
        "cost_usd": cost,
        "latency_ms": latency_ms,
        "total_tokens": resp.usage.total_tokens,
    }


def compare_providers(prompt: str, providers: list | None = None) -> list[dict]:
    """Run prompt across all available providers; return results sorted by cost."""
    providers = providers or PROVIDERS
    results = []
    for env_var, model_str in providers:
        if not os.environ.get(env_var):
            continue
        results.append(call_provider(model_str, prompt))
    results.sort(key=lambda r: r["cost_usd"])
    return results


def smart_completion(prompt: str, budget_usd: float = 0.001) -> str:
    """Return an answer using the best model within budget_usd.

    Prefers openai/gpt-4o; falls back to openai/gpt-4o-mini when the
    estimated cost exceeds budget_usd.
    """
    preferred = "openai/gpt-4o"
    fallback = "openai/gpt-4o-mini"
    assumed_output = 80
    estimated_input = int(len(prompt.split()) * 1.3)
    input_cost, output_cost = litellm.cost_per_token(
        model=preferred,
        prompt_tokens=estimated_input,
        completion_tokens=assumed_output,
    )
    model = preferred if (input_cost + output_cost) <= budget_usd else fallback
    resp = completion(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=assumed_output,
    )
    return resp.choices[0].message.content
