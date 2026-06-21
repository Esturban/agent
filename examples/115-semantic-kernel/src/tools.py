"""
Plugin definitions for example 115 — Semantic Kernel.

Each plugin is a dict of named functions that the Kernel can call.
These simulate real tools: web search and text summarization.
"""

from semantic_kernel.functions import kernel_function


class WebSearchPlugin:
    """Simulates a web search tool that returns fake but realistic results."""

    SEARCH_RESULTS = {
        "climate change": (
            "Climate change refers to long-term shifts in global temperatures and weather "
            "patterns. Since the 1800s, human activities — mainly burning fossil fuels — "
            "have been the main driver. CO2 levels have risen 50% above pre-industrial "
            "levels. The IPCC reports that limiting warming to 1.5C requires net-zero "
            "emissions by 2050."
        ),
        "large language models": (
            "Large language models (LLMs) are neural networks trained on vast text corpora "
            "using self-supervised learning. GPT-4 (OpenAI), Claude (Anthropic), and Gemini "
            "(Google) are current leaders. Key capabilities: text generation, summarization, "
            "code synthesis, and reasoning. Emergent behaviors appear at scale >100B params."
        ),
        "renewable energy": (
            "Renewable energy sources — solar, wind, hydro, geothermal — account for 30% "
            "of global electricity in 2024. Solar PV costs fell 90% from 2010-2023. Wind "
            "capacity grew 75% in the same period. IEA projects renewables will supply 60% "
            "of electricity by 2030 under net-zero scenarios."
        ),
    }

    @kernel_function(
        name="search",
        description="Search the web for information on a topic",
    )
    def search(self, query: str) -> str:
        """Return simulated search results for a query."""
        query_lower = query.lower()
        for key, result in self.SEARCH_RESULTS.items():
            if key in query_lower:
                return f"[WebSearch results for '{query}']\n{result}"
        return (
            f"[WebSearch results for '{query}']\n"
            "No specific results found. General answer: This topic requires further "
            "research. Key factors to consider include recent publications, expert "
            "consensus, and empirical data from peer-reviewed sources."
        )


class SummarizerPlugin:
    """Summarizes text to a requested number of sentences."""

    @kernel_function(
        name="summarize",
        description="Summarize a long text into a shorter version",
    )
    def summarize(self, text: str, sentences: int = 2) -> str:
        """Truncate text to approximately the requested number of sentences."""
        parts = [s.strip() for s in text.replace("\n", " ").split(".") if s.strip()]
        selected = parts[: max(1, sentences)]
        return ". ".join(selected) + "."

    @kernel_function(
        name="extract_key_points",
        description="Extract the key points from a text as a bullet list",
    )
    def extract_key_points(self, text: str) -> str:
        """Return the first 3 sentences as bullet points."""
        parts = [s.strip() for s in text.replace("\n", " ").split(".") if s.strip()]
        bullets = [f"- {p}" for p in parts[:3]]
        return "\n".join(bullets) if bullets else "- No key points found."
