import time
from typing import Any, TypedDict

from langchain.callbacks.base import BaseCallbackHandler
from langchain_openai import ChatOpenAI

DEMO_TASKS = [
    "Explain what an LLM callback handler does in one sentence.",
    "What are three benefits of agent observability?",
]


class ObservabilityCallback(BaseCallbackHandler):
    def __init__(self):
        self.calls: list[dict] = []
        self._starts: dict[str, float] = {}

    def on_llm_start(self, serialized: dict, prompts: list, run_id: Any, **kwargs):
        self._starts[str(run_id)] = time.time()

    def on_llm_end(self, response: Any, run_id: Any, **kwargs):
        elapsed = round((time.time() - self._starts.pop(str(run_id), time.time())) * 1000)
        usage = {}
        if response.llm_output:
            usage = response.llm_output.get("token_usage", {})
        self.calls.append(
            {
                "latency_ms": elapsed,
                "prompt_tokens": usage.get("prompt_tokens", 0),
                "completion_tokens": usage.get("completion_tokens", 0),
            }
        )

    def on_llm_error(self, error: Any, run_id: Any, **kwargs):
        self.calls.append({"error": str(error)})

    def report(self) -> dict:
        ok = [c for c in self.calls if "error" not in c]
        return {
            "total_calls": len(self.calls),
            "errors": len(self.calls) - len(ok),
            "avg_latency_ms": round(sum(c["latency_ms"] for c in ok) / max(len(ok), 1)),
            "total_tokens": sum(
                c.get("prompt_tokens", 0) + c.get("completion_tokens", 0) for c in ok
            ),
        }


class ObservabilityState(TypedDict):
    task: str
    response: str


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
