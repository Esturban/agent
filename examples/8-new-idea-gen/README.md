# 8-new-idea-gen - AI-Powered Idea Generation Agent

## Prerequisites
**Keys:** `OPENAI_API_KEY` · `BRAVE_API_KEY`
**Files:** none — fetches the free-for-dev list from GitHub at runtime
**Colab:** ✅ fully self-contained; set both keys in your Colab secrets

```bash
python examples/8-new-idea-gen/main.py
```

This agent automatically parses the [free-for-dev](https://github.com/ripienaar/free-for-dev) list and generates high-value, low-effort agentic solution ideas using free tools.

## Overview

The agent consists of two main components:

1. **Parser Agent**: Parses the free-for-dev list from GitHub and creates embeddings for all available free tools
2. **Idea Generation Agent**: Researches market trends and generates concrete, actionable ideas that combine multiple free tools into cohesive solutions

## Features

- 🆓 **Free Tool Analysis**: Automatically parses and categorizes hundreds of free developer tools
- 🤖 **AI-Powered Ideas**: Uses OpenAI embeddings and LLMs to generate creative, valuable solution ideas
- 🌐 **Market Research**: Incorporates web search to identify current trends and market gaps
- 📊 **Structured Output**: Generates detailed ideas with confidence scores, implementation complexity, and next steps

## Prerequisites

- Python 3.8+
- OpenAI API key
- Brave Search API key (for web research)
- OpenRouter API key (optional, for alternative models)

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
export OPENAI_API_KEY="your-openai-api-key"
export BRAVE_API_KEY="your-brave-search-api-key"
export OPENROUTER_API_KEY="your-openrouter-api-key"  # Optional
```

## Usage

Run the idea generation agent:

```bash
python main.py
```

Or with custom output location:

```bash
python main.py --output "data/ideas/my_ideas"
```

## Output

The agent generates:
- JSON file with structured idea data
- Console output showing idea summaries
- Confidence scores and implementation guidance

The agent includes a concise 1–2 sentence `reasoning` field explaining why the chosen tools were selected for each idea.

Example output structure:
```json
{
  "timestamp": "20241205_143022",
  "total_ideas": 3,
  "ideas": [
    {
      "title": "AI-Powered Development Assistant",
      "description": "An intelligent agent that combines multiple free tools to automate development workflows",
      "target_tools": ["GitHub", "OpenAI", "Vercel"],
      "value_proposition": "Reduces development time and improves code quality through intelligent automation",
      "effort_level": "medium",
      "implementation_complexity": "moderate",
      "confidence": 0.85,
      "reasoning": "Combines GitHub Actions for automation and Vercel for fast hosting to streamline CI-to-deploy for hobby projects.",
      "next_steps": [
        "Research specific APIs and integration points",
        "Create a minimal prototype with free tools",
        "Validate market demand through user testing"
      ]
    }
  ]
}
```

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│  Free-for-Dev   │───▶│   Parser Agent   │───▶│ Idea Generation  │
│  List (URL)     │    │                  │    │     Agent        │
└─────────────────┘    └──────────────────┘    └──────────────────┘
                                                        │
                                                        ▼
                                                ┌──────────────────┐   
                                                │  Idea Content.   │───▶ Output (ideas.json)
                                                │ (tools, summary) │
                                                └──────────────────┘
```

Note: the current implementation uses a simple two-stage pipeline (parser → idea generator). Embeddings and web-research referenced elsewhere are optional/planned extensions and are not active in the present code.

## Key Components

### Models (`src/models.py`)
- `FreeTool`: Represents individual free tools with metadata
- `ParsedContent`: Structured representation of parsed tool data
- `ToolEmbedding`: Embeddings for semantic search and analysis
- `IdeaConcept`: Core idea structure with implementation details
- `AgentState`: State management for the workflow

### Tools (`src/tools.py`)
- `parse_free_dev_list()`: Extracts tool information from markdown
- `web_search_tool()`: Searches for market trends and opportunities
- `create_embeddings()`: Generates OpenAI embeddings for tools

### Workflow (`src/workflow.py`)
- Two-stage pipeline: parsing → idea generation
- LangGraph-based state management
- Error handling and recovery

## Customization

The agent can be extended by:
- Adding new tool categories or sources
- Modifying the idea generation prompts
- Integrating additional research sources
- Customizing the output format

## Related Examples

- [3-prospect-agent](../3-prospect-agent/): Similar architecture for LinkedIn prospect research
- [7-redis-rag](../7-redis-rag/): RAG implementation with Redis vector storage

## Contributing

When adding features:
1. Update the models to support new data structures
2. Add corresponding tools for data processing
3. Modify the agent logic for new capabilities
4. Update this README with usage examples
