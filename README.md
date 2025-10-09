## RAG Agent

> A repo dedicated to building different Retrieval Augmented Generative Agents using LangGraph and LangChain.

This is a separate workspace exploring different agents using LangGraph and different database options to explore how to make RAG agents under different circumstances with different criteria.

The following are the contents of this repository:  

- [`examples/1-basic-local-rag`](./examples/1-basic-local-rag/README.md) - A very basic RAG agent using LangGraph and LangChain.
- [`examples/2-multi-tool-rag`](./examples/2-multi-tool-rag/README.md) - A RAG agent with internet search using a cloud-hosted Vector DB.
- [`examples/3-prospect-agent`](./examples/3-prospect-agent/README.md) - A RAG agent that uses internet search to augment prospects with news articles.
- [`examples/4-basic-react-agent`](./examples/4-basic-react-agent/README.md) - A simple ReAct agent that has the ability to remember conversation history and reference PDFs.
- [`examples/5-react-agent-lg`](./examples/5-react-agent-lg/README.md) - A ReAct agent in langgraph with specific instructions and conversation history.
- [`examples/6-multi-agent-graph`](./examples/6-multi-agent-graph/README.md) - Multiple agents in langgraph that interact to decide and determine the information to query and get.
- [`examples/7-redis-rag`](./examples/7-redis-rag/README.md) - A RAG agent with Vector Database creation and conditional tools to evaluate the confidence of the context requested to answer inputs (Visible graph stream)
- [`examples/8-new-idea-gen`](./examples/8-new-idea-gen/README.md) - A new idea generator agent that uses LangGraph and LangChain.
