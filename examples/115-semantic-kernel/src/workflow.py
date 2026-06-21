"""
Kernel setup and workflow for example 115 — Semantic Kernel.

Creates a Kernel with OpenAI chat service, registers plugins,
then uses the kernel to complete a multi-step research task via
FunctionChoiceBehavior (SK's built-in tool-use orchestration).
"""

import asyncio

import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.open_ai import OpenAIChatPromptExecutionSettings
from semantic_kernel.contents.chat_history import ChatHistory

from src.tools import WebSearchPlugin, SummarizerPlugin


def create_workflow() -> sk.Kernel:
    """
    Build and return a configured Semantic Kernel with plugins registered.

    Graph pattern:
        Kernel
          ├── WebSearchPlugin.search()
          ├── SummarizerPlugin.summarize()
          └── SummarizerPlugin.extract_key_points()
    """
    kernel = sk.Kernel()

    # Register the OpenAI chat service
    kernel.add_service(
        OpenAIChatCompletion(
            service_id="default",
            ai_model_id="gpt-4o-mini",
        )
    )

    # Register plugins — the Kernel discovers @kernel_function methods automatically
    kernel.add_plugin(WebSearchPlugin(), plugin_name="WebSearch")
    kernel.add_plugin(SummarizerPlugin(), plugin_name="Summarizer")

    return kernel


async def run_research_task(kernel: sk.Kernel, goal: str) -> dict:
    """
    Invoke the kernel on a research goal with auto function calling.

    The kernel sees available plugins and decides which to call based on the goal.
    Returns a dict with the final response and which functions were invoked.
    """
    settings = OpenAIChatPromptExecutionSettings(
        function_choice_behavior=FunctionChoiceBehavior.Auto(
            filters={"included_plugins": ["WebSearch", "Summarizer"]}
        )
    )

    history = ChatHistory()
    history.add_system_message(
        "You are a research assistant. To answer questions, first search for relevant "
        "information using WebSearch, then summarize the findings concisely."
    )
    history.add_user_message(goal)

    chat_service = kernel.get_service("default")
    result = await chat_service.get_chat_message_content(
        chat_history=history,
        settings=settings,
        kernel=kernel,
    )

    return {
        "goal": goal,
        "response": str(result),
        "finish_reason": result.finish_reason if hasattr(result, "finish_reason") else "stop",
    }


def run_task_sync(kernel: sk.Kernel, goal: str) -> dict:
    """Synchronous wrapper around run_research_task for use in main.py."""
    return asyncio.run(run_research_task(kernel, goal))
