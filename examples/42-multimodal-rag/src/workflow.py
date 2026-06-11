from langchain_community.vectorstores import Chroma
from langchain_core.messages import HumanMessage
from langgraph.graph import END, StateGraph

from .tools import IMAGE_DOCS, MultimodalState, embeddings, fetch_image_b64, qa_llm, vision_llm

_vectorstore: Chroma | None = None


def describe_images(state: MultimodalState) -> dict:
    descriptions = []
    for doc in IMAGE_DOCS:
        try:
            b64 = fetch_image_b64(doc["url"])
            msg = HumanMessage(content=[
                {"type": "text", "text": f"Describe this image in 2 sentences. Label: {doc['label']}"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
            ])
            result = vision_llm.invoke([msg])
            desc = f"[{doc['id']}] {result.content}"
        except Exception as e:
            desc = f"[{doc['id']}] {doc['label']} (description unavailable: {e})"
        descriptions.append(desc)
        print(f"  Described: {doc['id']}")
    return {"descriptions": descriptions}


def store_descriptions(state: MultimodalState) -> dict:
    global _vectorstore
    _vectorstore = Chroma.from_texts(
        state["descriptions"],
        embedding=embeddings,
        collection_name="image_descriptions",
    )
    print(f"  Stored {len(state['descriptions'])} descriptions")
    return {}


def answer_query(state: MultimodalState) -> dict:
    if _vectorstore is None:
        return {"answer": "No descriptions indexed yet."}
    docs = _vectorstore.similarity_search(state["query"], k=3)
    context = "\n".join(d.page_content for d in docs)
    prompt = f"Context:\n{context}\n\nQuestion: {state['query']}\nAnswer:"
    result = qa_llm.invoke([HumanMessage(content=prompt)])
    return {"answer": result.content}


def create_workflow():
    graph = StateGraph(MultimodalState)
    graph.add_node("describe", describe_images)
    graph.add_node("store", store_descriptions)
    graph.add_node("answer", answer_query)
    graph.set_entry_point("describe")
    graph.add_edge("describe", "store")
    graph.add_edge("store", "answer")
    graph.add_edge("answer", END)
    return graph.compile()
