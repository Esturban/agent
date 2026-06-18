import requests

K = 3  # documents retrieved per retriever


def load_catalog() -> list[str]:
    """Fetch the Fake Store product catalog — free, zero auth, 20 real products.

    Each product becomes one document string: title + price + category + description.
    Titles contain specific words (BM25 wins on exact match) while descriptions are
    natural-language prose (vector search wins on semantic intent) — the same contrast
    the hybrid retriever is designed to demonstrate, now on real data.
    """
    resp = requests.get("https://fakestoreapi.com/products", timeout=10)
    return [
        f"{p['title']} (${p['price']:.2f}, {p['category']}): {p['description'][:120]}"
        for p in resp.json()
    ]


# Populated at import time — acceptable for a demo; in production, lazy-load instead.
DOCS = load_catalog()

# Queries chosen to demonstrate the three retrieval modes on the Fake Store catalog.
SAMPLE_QUESTIONS = [
    "Tell me about the Fjallraven Foldsack backpack.",  # BM25 wins: exact title words
    "I need something warm for the outdoors.",          # Vector wins: semantic intent
    "What jewelry is available?",                       # BM25 wins: exact category keyword
    "Find me something to carry a laptop in.",          # Vector wins: semantic paraphrase
    "What electronics do you sell?",                    # Hybrid: category + product type
]
