import asyncio
from nemoguardrails import RailsConfig, LLMRails
from .tools import get_config_path


def load_rails() -> LLMRails:
    config = RailsConfig.from_path(get_config_path())
    return LLMRails(config)


async def run_with_rails(rails: LLMRails, user_message: str) -> str:
    messages = [{"role": "user", "content": user_message}]
    response = await rails.generate_async(messages=messages)
    if isinstance(response, dict):
        return response.get("content", str(response))
    return str(response)


def query(rails: LLMRails, user_message: str) -> str:
    return asyncio.run(run_with_rails(rails, user_message))
