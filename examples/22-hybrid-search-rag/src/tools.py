K = 3  # documents retrieved per retriever

# Knowledge base — product catalog with specific model names and codes.
# Demonstrates where BM25 outperforms pure vector search: exact keyword matches
# on model numbers and product names that embeddings would score as semantically similar.
DOCS = [
    "The Apex-X200 is a high-performance SSD with 7,000 MB/s sequential read speed and NVMe Gen4 interface.",
    "The Apex-X100 is an entry-level SSD with 3,500 MB/s sequential read speed and NVMe Gen3 interface.",
    "The Apex-M50 is a mechanical hard drive with 7,200 RPM and 256 MB cache, designed for archival storage.",
    "The Vertex-Pro GPU supports ray tracing, DLSS 3.0, and has 16 GB of GDDR6X memory.",
    "The Vertex-Core GPU is an entry model with 8 GB GDDR6 memory, targeting 1080p gaming.",
    "Our return policy allows returns within 30 days of purchase for all products in original packaging.",
    "Warranty coverage: Apex-X200 and Apex-X100 carry a 5-year limited warranty. Apex-M50 carries 3 years.",
    "The Apex-X200 is compatible with PCIe 4.0 and PCIe 5.0 motherboards via backward compatibility.",
    "Vertex-Pro requires a 750W PSU minimum. Vertex-Core requires 550W minimum.",
    "Technical support for Apex series products is available 24/7 via support.apextech.com.",
]

# Mix of queries that favour BM25 (exact model names), vector search (semantics),
# and hybrid (both signals needed).
SAMPLE_QUESTIONS = [
    "What is the read speed of the Apex-X200?",  # BM25 wins: exact model code
    "Which product is best for budget gaming?",  # Vector wins: semantic intent
    "What warranty does the Apex-M50 come with?",  # BM25 wins: exact model code
    "How much power does the Vertex-Pro need?",  # Hybrid: model name + concept
    "Can I return a product if I change my mind?",  # Vector wins: paraphrase of policy
]
