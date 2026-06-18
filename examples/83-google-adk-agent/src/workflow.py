import asyncio

from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types as genai_types

from src.tools import list_topics, search_knowledge

# ADK contrast with LangGraph:
#   LangGraph: you define the graph (nodes + edges + state) explicitly.
#   ADK:       you declare the agent (name, model, tools, instruction) and ADK
#              manages the tool-call loop internally.
_session_service = InMemorySessionService()
APP_NAME = "adk_knowledge_demo"


def create_agent() -> LlmAgent:
    """Create an ADK LlmAgent with two knowledge-base tools."""
    return LlmAgent(
        name="knowledge_agent",
        model="gemini-2.0-flash",
        description="Answers questions using a technology knowledge base.",
        instruction=(
            "You are a helpful assistant. Use search_knowledge to look up topics "
            "and list_topics to show available entries. Be concise."
        ),
        # ADK builds the JSON tool schema from the function docstrings automatically.
        tools=[search_knowledge, list_topics],
    )


async def run_query_async(query: str, agent: LlmAgent) -> str:
    """Run one query through the ADK runner and return the final text response."""
    runner = Runner(
        agent=agent,
        app_name=APP_NAME,
        session_service=_session_service,
    )
    # Each call gets a fresh session — stateless per query for this demo.
    session = await _session_service.create_session(
        app_name=APP_NAME,
        user_id="demo_user",
    )
    message = genai_types.Content(
        role="user",
        parts=[genai_types.Part(text=query)],
    )
    response_text = ""
    async for event in runner.run_async(
        user_id="demo_user",
        session_id=session.id,
        new_message=message,
    ):
        # ADK emits multiple events; is_final_response() marks the last one.
        if event.is_final_response() and event.response.parts:
            response_text = event.response.parts[0].text
    return response_text


def run_query(query: str, agent: LlmAgent) -> str:
    """Synchronous wrapper around the async ADK runner."""
    return asyncio.run(run_query_async(query, agent))
