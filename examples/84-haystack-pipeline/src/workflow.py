from haystack import Pipeline
from haystack.components.builders import PromptBuilder
from haystack.components.generators import OpenAIGenerator
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.document_stores.in_memory import InMemoryDocumentStore

from src.tools import DOCUMENTS

# Haystack contrast with LangGraph:
#   LangGraph: shared mutable state dict flows through nodes.
#   Haystack:  stateless DAG — each component exposes named input/output ports;
#              pipeline.connect() wires them explicitly.

_PROMPT_TEMPLATE = """
Answer the question concisely using only the provided context.
If the context doesn't contain the answer, say so.

Context:
{% for doc in documents %}
- {{ doc.content }}
{% endfor %}

Question: {{ query }}
Answer:
"""


def create_pipeline() -> tuple[Pipeline, InMemoryDocumentStore]:
    """Build and return a BM25 RAG pipeline with an in-memory document store."""
    store = InMemoryDocumentStore()
    store.write_documents(DOCUMENTS)

    pipeline = Pipeline()
    # add_component registers a component instance under a name
    pipeline.add_component("retriever",     InMemoryBM25Retriever(document_store=store))
    pipeline.add_component("prompt_builder", PromptBuilder(template=_PROMPT_TEMPLATE))
    pipeline.add_component("generator",      OpenAIGenerator(model="gpt-4o-mini"))

    # connect("source_component.output_port", "target_component.input_port")
    # Haystack validates port names at connect time — typos fail fast.
    pipeline.connect("retriever.documents", "prompt_builder.documents")
    pipeline.connect("prompt_builder.prompt", "generator.prompt")

    return pipeline, store


def run_query(pipeline: Pipeline, question: str) -> str:
    """Run a question through the pipeline and return the answer string."""
    result = pipeline.run({
        "retriever":      {"query": question},
        "prompt_builder": {"query": question},
    })
    # OpenAIGenerator returns a list of replies — take the first.
    replies = result["generator"]["replies"]
    return replies[0] if replies else "(no answer)"
