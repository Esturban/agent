from typing import List, Dict, Set
from qdrant_client import QdrantClient
from qdrant_client.http import models as rest


def batch_existing_checksums(client: QdrantClient, collection_name: str, checksums: List[str], batch_size: int = 256) -> Set[str]:
    """Return a set of checksums that already exist in the collection's payload.

    This implementation uses Qdrant `scroll` with a payload filter that matches any
    of the provided checksums in batches. If the Qdrant version does not support
    list matching, this function may return an empty set and the caller should
    fall back to alternative strategies.
    """
    existing = set()
    for i in range(0, len(checksums), batch_size):
        batch = checksums[i : i + batch_size]
        try:
            condition = rest.Filter(must=[rest.FieldCondition(key="content_checksum", match=rest.MatchValue(value=batch))])
            hits = client.scroll(collection_name=collection_name, filter=condition, limit=1000)
            for hit in hits:
                payload = hit.payload or {}
                if "content_checksum" in payload:
                    existing.add(payload["content_checksum"])
        except Exception:
            # best effort: continue, returning whatever we've found so far
            continue
    return existing


def missing_documents_by_checksum(client: QdrantClient, collection_name: str, docs: List[Dict], checksum_fn) -> List[Dict]:
    """Return subset of docs that are not present (by checksum) in the collection.

    `docs` may be LangChain Document objects or dicts with a `content` field. The
    `checksum_fn` should accept a string and return a checksum string.
    """
    # map checksum -> original doc list
    checksum_to_docs = {}
    checksums = []
    for d in docs:
        content = getattr(d, "page_content", None) or d.get("content") if isinstance(d, dict) else str(d)
        cs = checksum_fn(content or "")
        checksums.append(cs)
        checksum_to_docs.setdefault(cs, []).append(d)

    existing = batch_existing_checksums(client, collection_name, checksums)
    missing = []
    for cs, original_docs in checksum_to_docs.items():
        if cs not in existing:
            missing.extend(original_docs)
    return missing


