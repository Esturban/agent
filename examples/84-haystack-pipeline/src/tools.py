from haystack import Document

# These documents are the knowledge base — stored in InMemoryDocumentStore.
# In production: replace with PineconeDocumentStore, WeaviateDocumentStore, etc.
DOCUMENTS = [
    Document(content="LangGraph is a library for building stateful, multi-actor LLM applications using graph-based workflows with TypedDict state."),
    Document(content="Haystack is an open-source NLP framework where components connect via named input/output ports in a stateless Pipeline DAG."),
    Document(content="The key difference: LangGraph uses a shared mutable state dict; Haystack passes data explicitly between component ports."),
    Document(content="LangChain provides chains and tool abstractions that can be embedded inside LangGraph nodes or used standalone."),
    Document(content="InMemoryDocumentStore is Haystack's simplest store — no external service needed, great for prototypes and teaching."),
    Document(content="BM25 retrieval scores documents by term frequency and inverse document frequency — fast keyword matching, no embeddings needed."),
    Document(content="OpenAIGenerator calls the OpenAI Chat Completions API and returns a list of reply strings under the key 'replies'."),
    Document(content="PromptBuilder renders a Jinja2 template with runtime variables like '{{ documents }}' and '{{ query }}' injected at run time."),
]

SAMPLE_QUESTIONS = [
    "What is the difference between LangGraph and Haystack?",
    "How does BM25 retrieval work?",
    "What does PromptBuilder do in a Haystack pipeline?",
    "When should I use InMemoryDocumentStore?",
]
