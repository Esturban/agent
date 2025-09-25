## RAG Agent - Basic

The following file is the implementation of a very basic RAG model made with LangGraph and LangChain.

The way it works:

- `src` contains the definition of the retrieval tool and builds embeddings for the documents after loading and splitting them.  
- `main.py` contains the workflow definition and the execution of the model.  

![](./assets/stategraph.png)

### Purpose

The purpose of this model is to demonstrate, a simple RAG model and how it can rely on documents pulled from the internet. Consider how you could vary this to be a RAG agent from a different site or locally loaded PDFs to create the embeddings.

### Drawbacks

- Each time this runtime is initialized, it will load all the documents and split them into chunks instead of keeping them persistent in the DB.
- The model will not be able to recall previous responses so it will mostly repeat the answer without much variation.

### References

- [Building Agentic RAG with LangGraph: A Step-by-Step Guide](https://medium.com/@wendell_89912/building-an-agentic-rag-with-langgraph-a-step-by-step-guide-009c5f0cce0a)
