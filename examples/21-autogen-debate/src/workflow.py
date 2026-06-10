from autogen import ConversableAgent

from src.tools import MAX_TURNS, get_llm_config


def run_debate(topic: str) -> list[dict]:
    """
    Run a two-agent AutoGen debate on the given topic.

    Unlike LangGraph (explicit StateGraph + nodes), AutoGen agents communicate
    directly via initiate_chat -- the framework manages the turn loop internally.
    Returns the full chat history as a list of message dicts.
    """
    llm_config = get_llm_config()

    proponent = ConversableAgent(
        name="Proponent",
        system_message=(
            f"You are a skilled debater arguing FOR: '{topic}'. "
            "Make strong, well-reasoned arguments. Be concise -- 2-3 sentences per turn."
        ),
        llm_config=llm_config,
        human_input_mode="NEVER",
    )
    opponent = ConversableAgent(
        name="Opponent",
        system_message=(
            f"You are a skilled debater arguing AGAINST: '{topic}'. "
            "Counter each argument directly. Be concise -- 2-3 sentences per turn."
        ),
        llm_config=llm_config,
        human_input_mode="NEVER",
    )

    result = proponent.initiate_chat(
        opponent,
        message=f"Proposition: '{topic}'. I argue FOR it -- let's debate.",
        max_turns=MAX_TURNS,
        silent=True,
    )
    return result.chat_history
