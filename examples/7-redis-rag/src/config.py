"""
Configuration and setup for the RAG agent.
"""

from .tools import doc_retriever

# Initialize the retriever tool with configuration
retriever_tool = doc_retriever(debug=None, k=10, score_threshold=0.7)

# List of tools available to the agent
tools = [retriever_tool]
