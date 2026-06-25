import base64
from pathlib import Path


def load_image_b64(source: str) -> tuple[str, str]:
    """Return (b64_string, mime_type) from a file path or URL."""
    if source.startswith("http"):
        import httpx
        resp = httpx.get(source, timeout=10)
        mime = resp.headers.get("content-type", "image/jpeg").split(";")[0]
        return base64.b64encode(resp.content).decode(), mime
    path = Path(source)
    mime_map = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png", "webp": "image/webp"}
    mime = mime_map.get(path.suffix.lstrip(".").lower(), "image/jpeg")
    return base64.b64encode(path.read_bytes()).decode(), mime


def vision_content(source: str, text: str) -> list:
    b64, mime = load_image_b64(source)
    return [
        {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
        {"type": "text", "text": text},
    ]


def ask_vision(source: str, question: str, client, model: str = "gpt-4o-mini") -> str:
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": vision_content(source, question)}],
        max_tokens=512,
    )
    return resp.choices[0].message.content
