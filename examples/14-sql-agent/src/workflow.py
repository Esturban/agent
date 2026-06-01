from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from src.tools import describe_table, list_tables, run_sql


def create_workflow():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    return create_react_agent(llm, tools=[list_tables, describe_table, run_sql])
