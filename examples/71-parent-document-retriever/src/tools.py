CHILD_CHUNK_SIZE = 100
PARENT_CHUNK_SIZE = 600

SAMPLE_DOCS = [
    """The transformer architecture revolutionized natural language processing. Introduced in 2017 by Vaswani et al., it replaced recurrent networks with self-attention mechanisms. This allowed parallel computation and better capture of long-range dependencies. The key innovation was multi-head attention, which lets the model focus on different parts of the input simultaneously. Transformers became the foundation for BERT, GPT, and all modern large language models. Their ability to scale with more data and computation made them the dominant architecture in AI today.""",

    """Retrieval-augmented generation (RAG) combines the strengths of retrieval systems and generative models. Instead of relying solely on parametric knowledge stored in model weights, RAG retrieves relevant documents from an external knowledge base at inference time. This approach reduces hallucination and allows models to access up-to-date information. The typical RAG pipeline has three stages: document indexing, retrieval, and generation. Vector embeddings enable semantic search, where queries and documents are matched by meaning rather than exact keywords. RAG has become the standard architecture for building AI applications over private or frequently updated data.""",

    """Neural network training involves adjusting millions of parameters to minimize a loss function. The primary algorithm is stochastic gradient descent (SGD) with backpropagation. In each training iteration, the model makes a forward pass to compute predictions, then a backward pass to compute gradients. The optimizer updates weights based on those gradients. Modern optimizers like Adam adapt the learning rate for each parameter. Regularization techniques like dropout prevent overfitting by randomly disabling neurons during training. Training large models requires distributed computing across multiple GPUs or TPUs.""",
]

SAMPLE_QUESTIONS = [
    "What was the key innovation in the transformer architecture?",
    "How does RAG reduce hallucination?",
    "What is stochastic gradient descent?",
]
