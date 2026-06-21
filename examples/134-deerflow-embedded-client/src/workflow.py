from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Iterator

import httpx


@dataclass
class DeerFlowClient:
    """HTTP wrapper for a running DeerFlow FastAPI service.
    DeerFlow owns skills, memory, and the LLM loop — you own only the request.
    """

    base_url: str
    thread_id: str
    _http: httpx.Client = field(
        default_factory=lambda: httpx.Client(timeout=httpx.Timeout(60.0, read=120.0))
    )

    def upload(self, filename: str, content: str) -> str:
        """Attach text to the thread workspace; returns artifact_id."""
        resp = self._http.post(
            f"{self.base_url}/api/files/upload",
            files={"file": (filename, content.encode(), "text/markdown")},
            data={"thread_id": self.thread_id},
        )
        resp.raise_for_status()
        return resp.json().get("artifact_id", "unknown")

    def stream(
        self, message: str, *, plan_mode: bool = False, subagent_enabled: bool = False
    ) -> Iterator[tuple[str, dict]]:
        """Yield (event_type, data) tuples from the SSE endpoint."""
        with self._http.stream(
            "POST",
            f"{self.base_url}/api/chat/stream",
            json={
                "message": message,
                "thread_id": self.thread_id,
                "plan_mode": plan_mode,
                "subagent_enabled": subagent_enabled,
            },
        ) as r:
            r.raise_for_status()
            for line in r.iter_lines():
                if not line.startswith("data:"):
                    continue
                raw = line.removeprefix("data:").strip()
                if raw == "[DONE]":
                    yield "end", {}
                    return
                try:
                    ev = json.loads(raw)
                    yield ev.get("type", "unknown"), ev
                except json.JSONDecodeError:
                    pass

    def chat(self, message: str, *, plan_mode: bool = False) -> str:
        """Blocking chat — joins message_chunk events into the final answer."""
        return "".join(
            d.get("content", "")
            for et, d in self.stream(message, plan_mode=plan_mode)
            if et == "message_chunk"
        )
