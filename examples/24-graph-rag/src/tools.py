TOP_K = 3  # neighbours to collect per matched entity

# Knowledge base with overlapping entities and explicit relationships.
# Designed so multi-hop graph traversal surfaces answers that single-doc
# retrieval would miss (e.g. "who founded the company behind LangGraph?").
DOCS = [
    "LangChain was founded by Harrison Chase in 2022 as an open-source Python framework for LLM applications.",
    "LangGraph is a library built on top of LangChain by Harrison Chase, adding stateful graph-based agent workflows.",
    "LangSmith is an observability platform created by LangChain Inc. for tracing and evaluating LLM pipelines.",
    "Anthropic was founded by Dario Amodei and Daniela Amodei in 2021 after they left OpenAI.",
    "Claude is the AI assistant developed by Anthropic, designed with a focus on safety and helpfulness.",
    "OpenAI was co-founded by Sam Altman, Elon Musk, Greg Brockman, and Ilya Sutskever in 2015.",
    "GPT-4 is a large language model developed by OpenAI, released in March 2023.",
    "Ilya Sutskever co-founded OpenAI and later founded Safe Superintelligence Inc. (SSI) in 2024.",
    "Dario Amodei previously served as VP of Research at OpenAI before co-founding Anthropic.",
    "LangChain Inc. raised a $25M Series A in 2023 and later a $35M round led by Sequoia Capital.",
]

SAMPLE_QUESTIONS = [
    "Who founded the company that makes LangGraph?",        # multi-hop: LangGraph -> LangChain -> Harrison Chase
    "What did Ilya Sutskever do after leaving OpenAI?",     # direct: Sutskever -> SSI
    "What observability tool does LangChain make?",         # direct: LangChain -> LangSmith
    "What company did Dario Amodei leave to found Anthropic?",  # multi-hop: Amodei -> OpenAI -> Anthropic
]
