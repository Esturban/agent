from src.workflow import create_simple_graph

DEMO_QUESTION = "Explain how photosynthesis works in 2 sentences."


def create_langchain_app():
    return create_simple_graph()
