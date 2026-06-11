from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, StateGraph

from .tools import NAMESPACE, SYSTEM_PROMPT, MemoryState, llm, store


def retrieve_memories(state: MemoryState) -> dict:
    query = state["messages"][-1] if state["messages"] else ""
    results = store.search(NAMESPACE, query=query, limit=5)
    memories = [r.value["fact"] for r in results]
    return {"memories": memories}


def respond(state: MemoryState) -> dict:
    memory_text = "\n".join(f"- {m}" for m in state["memories"]) or "None yet"
    system = SYSTEM_PROMPT.format(memories=memory_text)
    history = [HumanMessage(content=msg) for msg in state["messages"]]
    response = llm.invoke([SystemMessage(content=system)] + history)
    return {"response": response.content}


def store_memories(state: MemoryState) -> dict:
    # Extract facts from the conversation and persist them
    extract_prompt = (
        f"From this conversation, extract 1-3 factual statements about the user as a JSON list. "
        f"Conversation: {state['messages']}\nResponse: {state['response']}\n"
        f'Return only a JSON array of strings, e.g. ["User is a Python developer"]'
    )
    result = llm.invoke([HumanMessage(content=extract_prompt)])
    import json

    try:
        facts = json.loads(result.content)
        for i, fact in enumerate(facts[:3]):
            key = f"{state['thread_id']}-fact-{i}"
            store.put(NAMESPACE, key, {"fact": fact})
    except (json.JSONDecodeError, TypeError):
        pass
    return {}


def create_workflow():
    graph = StateGraph(MemoryState)
    graph.add_node("retrieve", retrieve_memories)
    graph.add_node("respond", respond)
    graph.add_node("store", store_memories)
    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "respond")
    graph.add_edge("respond", "store")
    graph.add_edge("store", END)
    return graph.compile()
