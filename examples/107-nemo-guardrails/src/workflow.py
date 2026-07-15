import asyncio
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from nemoguardrails import RailsConfig, LLMRails
from .tools import get_config_path


class NoStopChatOpenAI(ChatOpenAI):
    """Adapt NeMo's legacy stop-token binding for GPT-5 chat models."""

    def bind(self, **kwargs):
        kwargs.pop("stop", None)
        return super().bind(**kwargs)


def load_rails() -> LLMRails:
    config = RailsConfig.from_path(get_config_path())
    llm = NoStopChatOpenAI(model="gpt-5.4-nano", temperature=0)
    return LLMRails(config, llm=llm)


async def run_with_rails(rails: LLMRails, user_message: str) -> str:
    messages = [{"role": "user", "content": user_message}]
    response = await rails.generate_async(messages=messages)
    if isinstance(response, dict):
        content = response.get("content", "")
    else:
        content = str(response)
    if content.strip():
        return content

    # Colang's input rail has accepted the message. Hand the benign request to
    # the application model rather than treating NeMo's empty continuation as a
    # successful response.
    app_llm = ChatOpenAI(model="gpt-5.4-nano", temperature=0)
    reply = await app_llm.ainvoke([
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage(content=user_message),
    ])
    return reply.content


def query(rails: LLMRails, user_message: str) -> str:
    return asyncio.run(run_with_rails(rails, user_message))
