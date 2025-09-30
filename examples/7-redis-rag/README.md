## Redis RAG Agent

The purpose of this workbook is to introduce various conditional tools and logic to assess whether a task is done or not.

The way the graph works:

- Decides whether or not to execute the function for retrieval
- Goes into the VDB to retrieve the documents
- Determines if the content is relevant with a grader
- If it's relevant, then it summarizes
- If it's irrelevant, then it rewrites the question (initiating the retrieval again until the agent is satisfied with the answer)


### Requirements

- Redis - There are several different ways to run a redis server. Your two easiest options:
    - Docker: `docker run -p 6379:6379 -d redis`
    - Cloud: Start a free account and use the link and API key (will need to adjust the server URL a bit)

### Inspiration / References

- [Langgraph - Redis Agentic RAG](https://colab.research.google.com/github/redis-developer/redis-ai-resources/blob/main/python-recipes/agents/00_langgraph_redis_agentic_rag.ipynb)