# Quickstart: Run the 2-external-vdb RAG example with dedup protection

Prerequisites:
- Python 3.11+
- Qdrant instance (local or cloud) and credentials in `.env` as `QDRANT_URL` and `QDRANT_KEY`
- OpenAI or compatible embeddings API credentials if using OpenAI embeddings

Steps:

1. Install dependencies: `pip install -r requirements.txt`
2. Set `.env` with `QDRANT_URL`, `QDRANT_KEY`, and `BRAVE_API_KEY` if running web search.
3. Run the example: `python examples/2-external-vdb/main.py`
4. Observe logs: ingest counts, skipped documents, and retriever readiness.

To reset the collection: use Qdrant UI or client to delete the `hugging_face_documentation`
collection and re-run ingestion to see all documents indexed.


