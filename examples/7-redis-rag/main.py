"""
Main entry point for the Redis RAG Agent example.
This module handles environment setup and execution of the agent workflow.
"""
import os
import pprint
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the modular components
from src.workflow import create_workflow


def main():
    """
    Main execution function for the RAG agent example.
    """
    # Create the workflow graph
    graph = create_workflow()

    # Example usage
    inputs = {
        "messages": [
            ("user", "What does Lilian Weng say about the types of agent memory? Please summarize"),
        ]
    }

    print("Running the RAG agent...")
    print("=" * 50)

    for output in graph.stream(inputs):
        for key, value in output.items():
            pprint.pprint(f"Output from node '{key}':")
            pprint.pprint("---")
            pprint.pprint(value, indent=2, width=80, depth=None)
        pprint.pprint("\n---\n")


if __name__ == "__main__":
    main()
