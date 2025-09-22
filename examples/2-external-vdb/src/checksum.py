import hashlib
from typing import Iterable


def normalize_text(text: str) -> str:
    """Normalize text deterministically for checksum calculation."""
    if text is None:
        return ""
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    return "\n".join(lines)


def compute_checksum(text: str) -> str:
    """Return SHA256 checksum of normalized text."""
    normalized = normalize_text(text)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def compute_checksums_for_docs(docs: Iterable[dict], content_field: str = "content"):
    """Yield (checksum, doc) pairs for documents that contain a content field."""
    for d in docs:
        content = d.get(content_field) if isinstance(d, dict) else None
        if content is None and hasattr(d, "page_content"):
            content = getattr(d, "page_content")
        yield compute_checksum(content or ""), d


