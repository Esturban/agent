from typing import TypedDict

from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langgraph.graph import END, START, StateGraph

from src.tools import DEMO_QUERY, SAMPLE_TEXT, semantic_chunks, sentence_window_chunks


class ChunkingState(TypedDict):
    query: str
    results: dict[str, str]


def create_workflow():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    emb = OpenAIEmbeddings(model="text-embedding-3-small")

    # Build all four chunk sets once at workflow creation time
    fixed = CharacterTextSplitter(separator="", chunk_size=200, chunk_overlap=20).split_text(SAMPLE_TEXT)
    recursive = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30).split_text(SAMPLE_TEXT)
    sw_texts = [item["sentence"] for item in sentence_window_chunks(SAMPLE_TEXT, window=1)]
    semantic = semantic_chunks(SAMPLE_TEXT, threshold=0.75, emb_model=emb)

    strategies = [
        ("fixed-size", fixed),
        ("recursive", recursive),
        ("sentence-window", sw_texts),
        ("semantic", semantic),
    ]

    def retrieve_and_answer(state: ChunkingState) -> dict:
        query = state["query"]
        results = {}
        for name, chunks in strategies:
            vs = Chroma.from_texts(chunks, emb, collection_name=f"chunk-{name}")
            docs = vs.similarity_search(query, k=2)
            context = "\n\n".join(d.page_content for d in docs)
            prompt = (
                f"Answer using ONLY the context below. If not found, say 'Not found.'\n\n"
                f"Context:\n{context}\n\nQuestion: {query}"
            )
            answer = llm.invoke(prompt).content
            results[name] = answer
        return {"results": results}

    graph = StateGraph(ChunkingState)
    graph.add_node("retrieve_and_answer", retrieve_and_answer)
    graph.add_edge(START, "retrieve_and_answer")
    graph.add_edge("retrieve_and_answer", END)
    return graph.compile()
