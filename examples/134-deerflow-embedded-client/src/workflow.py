from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Iterator

import httpx


@dataclass
class DeerFlowClient:
    """Thin HTTP client for a running DeerFlow service.

    DeerFlow exposes a FastAPI backend. This client wraps the three
    endpoints needed for the embedded-client pattern:
      POST /api/files/upload  — attach a file to a thread workspace
      POST /api/chat/stream   — SSE streaming run
      POST /api/chat          — blocking run (non-streaming)

    Contrast with direct LangGraph:
      LangGraph  → you own the graph (nodes, edges, state, tool-call loop)
      DeerFlow   → you own the *request*; the runtime owns everything else
    """

    base_url: str
    thread_id: str
    _http: httpx.Client = field(
        default_factory=lambda: httpx.Client(timeout=httpx.Timeout(60.0, read=120.0))
    )

    def upload(self, filename: str, content: str) -> str:
        """Upload text content as a file; returns the artifact_id."""
        resp = self._http.post(
            f"{self.base_url}/api/files/upload",
            files={"file": (filename, content.encode(), "text/markdown")},
            data={"thread_id": self.thread_id},
        )
        resp.raise_for_status()
        return resp.json().get("artifact_id", "unknown")

    def stream(
        self,
        message: str,
        *,
        plan_mode: bool = False,
        subagent_enabled: bool = False,
    ) -> Iterator[tuple[str, dict]]:
        """Yield (event_type, data) tuples from the SSE streaming endpoint.

        DeerFlow emits Server-Sent Events with types:
          message_chunk  — incremental LLM output
          tool_call      — the agent is invoking a tool
          tool_result    — tool returned
          end            — run complete (data: [DONE])
        """
        payload = {
            "message": message,
            "thread_id": self.thread_id,
            "plan_mode": plan_mode,
            "subagent_enabled": subagent_enabled,
        }
        with self._http.stream(
            "POST", f"{self.base_url}/api/chat/stream", json=payload
        ) as resp:
            resp.raise_for_status()
            for line in resp.iter_lines():
                if not line.startswith("data:"):
                    continue
                raw = line.removeprefix("data:").strip()
                if raw == "[DONE]":
                    yield "end", {}
                    return
                try:
                    event = json.loads(raw)
                    yield event.get("type", "unknown"), event
                except json.JSONDecodeError:
                    pass

    def chat(self, message: str, *, plan_mode: bool = False) -> str:
        """Blocking chat; collects streamed chunks and returns the final answer."""
        chunks: list[str] = []
        for event_type, data in self.stream(message, plan_mode=plan_mode):
            if event_type == "message_chunk":
                chunks.append(data.get("content", ""))
        return "".join(chunks)

    def close(self) -> None:
        self._http.close()
