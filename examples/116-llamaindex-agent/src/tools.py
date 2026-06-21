"""
Tool helpers for example 116 — LlamaIndex ReAct Agent.

Provides sample document sets (science, history, technology) and
utilities to build QueryEngineTool objects from them.
"""

from llama_index.core import Document, VectorStoreIndex
from llama_index.core.tools import QueryEngineTool, ToolMetadata


SCIENCE_DOCS = [
    Document(
        text=(
            "Photosynthesis is the process by which plants convert sunlight, water, and "
            "CO2 into glucose and oxygen. The reaction occurs in chloroplasts using "
            "chlorophyll as the primary pigment. The light-dependent reactions occur in "
            "the thylakoid membrane; the Calvin cycle occurs in the stroma. Plants produce "
            "approximately 120 billion tonnes of dry biomass per year via photosynthesis."
        )
    ),
    Document(
        text=(
            "DNA (deoxyribonucleic acid) is the hereditary material in humans and almost "
            "all other organisms. DNA stores genetic information as sequences of four bases: "
            "adenine (A), thymine (T), guanine (G), and cytosine (C). The human genome "
            "contains approximately 3 billion base pairs encoding around 20,000 protein-coding "
            "genes. DNA replication is semiconservative: each strand serves as a template."
        )
    ),
    Document(
        text=(
            "Quantum mechanics describes the behavior of matter and energy at the atomic "
            "and subatomic scale. Key principles: wave-particle duality, superposition, "
            "and the uncertainty principle (Heisenberg, 1927). Quantum entanglement allows "
            "particles to share quantum states regardless of distance. Applications include "
            "transistors, MRI machines, lasers, and quantum computing."
        )
    ),
]

HISTORY_DOCS = [
    Document(
        text=(
            "The Roman Empire at its peak (117 AD under Trajan) controlled 5 million km2 "
            "and 70 million people — 21% of the world's population. Rome transitioned from "
            "a republic to an empire in 27 BC when Octavian became Augustus. The Western "
            "Roman Empire fell in 476 AD; the Eastern (Byzantine) Empire survived until 1453."
        )
    ),
    Document(
        text=(
            "The Industrial Revolution began in Britain around 1760 and transformed "
            "manufacturing from hand production to machine-based methods. Key innovations: "
            "the steam engine (Watt, 1769), spinning jenny (Hargreaves, 1764), and "
            "iron smelting with coke (Darby, 1709). Britain's coal output rose 8x between "
            "1700 and 1800. By 1850, half of Britain's population lived in cities."
        )
    ),
    Document(
        text=(
            "World War II (1939-1945) was the deadliest conflict in human history with "
            "70-85 million fatalities. It began with Germany's invasion of Poland on "
            "September 1, 1939. The Allied powers (US, UK, USSR, France) defeated the "
            "Axis (Germany, Italy, Japan). The war ended in Europe on May 8, 1945 (V-E Day) "
            "and in the Pacific on September 2, 1945 (V-J Day) after atomic bombs on "
            "Hiroshima and Nagasaki."
        )
    ),
]

TECHNOLOGY_DOCS = [
    Document(
        text=(
            "The Internet is a global network of interconnected computers using the "
            "TCP/IP protocol suite. It originated from ARPANET (1969), funded by the US "
            "Department of Defense. Tim Berners-Lee invented the World Wide Web in 1989, "
            "separating the web (HTTP/HTML layer) from the underlying internet. As of 2024, "
            "5.4 billion people (67% of the global population) use the internet."
        )
    ),
    Document(
        text=(
            "Machine learning (ML) is a subset of artificial intelligence where systems "
            "learn patterns from data without being explicitly programmed. Three main "
            "paradigms: supervised learning (labeled examples), unsupervised learning "
            "(clustering, dimensionality reduction), and reinforcement learning (reward "
            "signals). Deep learning uses neural networks with many layers; transformers "
            "(introduced 2017) power modern LLMs."
        )
    ),
    Document(
        text=(
            "Blockchain is a distributed ledger technology where records (blocks) are "
            "linked using cryptographic hashes and stored across a peer-to-peer network. "
            "Bitcoin (Nakamoto, 2008) was the first blockchain application. Ethereum (2015) "
            "introduced smart contracts — self-executing code on the blockchain. Proof-of-work "
            "consensus is energy-intensive; proof-of-stake reduces energy use by 99.9%."
        )
    ),
]


def build_query_engine_tools(
    science_docs: list[Document] | None = None,
    history_docs: list[Document] | None = None,
    tech_docs: list[Document] | None = None,
) -> list[QueryEngineTool]:
    """
    Index each document list and wrap as a QueryEngineTool.
    Returns list of 3 tools: science, history, technology.
    """
    science_docs = science_docs or SCIENCE_DOCS
    history_docs = history_docs or HISTORY_DOCS
    tech_docs = tech_docs or TECHNOLOGY_DOCS

    science_index = VectorStoreIndex.from_documents(science_docs)
    history_index = VectorStoreIndex.from_documents(history_docs)
    tech_index = VectorStoreIndex.from_documents(tech_docs)

    return [
        QueryEngineTool(
            query_engine=science_index.as_query_engine(),
            metadata=ToolMetadata(
                name="science_tool",
                description=(
                    "Answers questions about science topics including biology "
                    "(photosynthesis, DNA), physics (quantum mechanics), and chemistry."
                ),
            ),
        ),
        QueryEngineTool(
            query_engine=history_index.as_query_engine(),
            metadata=ToolMetadata(
                name="history_tool",
                description=(
                    "Answers questions about historical events including the Roman Empire, "
                    "the Industrial Revolution, and World War II."
                ),
            ),
        ),
        QueryEngineTool(
            query_engine=tech_index.as_query_engine(),
            metadata=ToolMetadata(
                name="technology_tool",
                description=(
                    "Answers questions about technology topics including the Internet, "
                    "machine learning, blockchain, and AI."
                ),
            ),
        ),
    ]


def ask_agent(agent, question: str) -> str:
    """Send a question to the agent and return the string response."""
    response = agent.chat(question)
    return str(response)
