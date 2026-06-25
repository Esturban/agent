import base64
import io


def pdf_page_to_b64(pdf_bytes: bytes, page_index: int = 0) -> str:
    """Render one PDF page to PNG and return base64."""
    import pypdfium2 as pdfium
    doc = pdfium.PdfDocument(pdf_bytes)
    page = doc[page_index]
    bitmap = page.render(scale=2)
    img = bitmap.to_pil()
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()


def extract_page(b64_png: str, schema_prompt: str, client, model: str = "gpt-4o-mini") -> dict:
    """Send one page image to vision model and return extracted JSON."""
    import json
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": [
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64_png}"}},
            {"type": "text", "text": schema_prompt + "\n\nRespond with valid JSON only."},
        ]}],
        max_tokens=1024,
    )
    text = resp.choices[0].message.content.strip().strip("```json").strip("```")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"raw": text}


def load_pdf_bytes(source: str) -> bytes:
    """Load PDF from file path or URL."""
    if source.startswith("http"):
        import httpx
        return httpx.get(source, timeout=15).content
    with open(source, "rb") as f:
        return f.read()
