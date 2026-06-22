from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Iterator

import httpx


@dataclass
class ResearchRun:
    """Drive a DeerFlow runtime configured with a custom skill.

    The runtime owns: skill activation, subagent delegation, artifact writing.
    This client owns: uploading source files and collecting resulting events.
    """

    base_url: str
    thread_id: str
    _http: httpx.Client = field(
        default_factory=lambda: httpx.Client(
            timeout=httpx.Timeout(60.0, read=300.0)
        )
    )

    def upload(self, filename: str, content: str) -> str:
        """Upload a text file into the thread workspace; returns artifact_id."""
        resp = self._http.post(
            f"{self.base_url}/api/files/upload",
            files={"file": (filename, content.encode(), "text/markdown")},
            data={"thread_id": self.thread_id},
        )
        resp.raise_for_status()
        return resp.json().get("artifact_id", "unknown")

    def stream(
        self,
        prompt: str,
        *,
        plan_mode: bool = True,
        subagent_enabled: bool = True,
    ) -> Iterator[tuple[str, dict]]:
        """Yield (event_type, data) tuples from the SSE endpoint."""
        with self._http.stream(
            "POST",
            f"{self.base_url}/api/chat/stream",
            json={
                "message": prompt,
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

    def artifact_path(self, events: list[tuple[str, dict]]) -> str | None:
        """Extract artifact path from tool_result events, if present."""
        for et, data in events:
            if et == "tool_result":
                content = str(data.get("content", ""))
                if ".md" in content or "artifact" in content.lower():
                    return content[:120]
        return None
