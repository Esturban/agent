from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from .tools import create_tools

_SYSTEM = (
    "You are a research assistant with three tools: "
    "vectorstore_search (internal knowledge base about LangGraph and RAG), "
    "web_search (live web results via DuckDuckGo), and "
    "calculator (Python math expressions). "
    "Choose the right tool for each question — use the vectorstore for internal topics, "
    "the web for current events, and the calculator for arithmetic. "
    "You may call multiple tools in sequence when needed."
)


def create_workflow():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    return create_react_agent(llm, tools=create_tools(), prompt=_SYSTEM)
