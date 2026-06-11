from langchain_core.documents import Document

# Private knowledge base for vectorstore path
DOCS = [
    Document(
        page_content="Our refund policy allows returns within 30 days of purchase with original receipt."
    ),
    Document(
        page_content="API rate limits are 1000 requests per minute for Pro plans and 100 for Free plans."
    ),
    Document(
        page_content="The platform supports SSO via SAML 2.0 and OAuth 2.0 providers including Google and GitHub."
    ),
    Document(
        page_content="Data is stored in EU-West-1 by default. US regions available on Enterprise plans."
    ),
    Document(
        page_content="Uptime SLA is 99.9% for Pro plans and 99.99% for Enterprise. Includes status page monitoring."
    ),
]

# Annotated with expected routing strategy — demonstrates classifier decisions
SAMPLE_QUESTIONS = [
    # strategy: "simple"   — no retrieval needed, LLM knows this
    "What is 7 multiplied by 8?",
    # strategy: "vectorstore" — private policy info not in LLM training data
    "What is your refund policy?",
    # strategy: "vectorstore" — private technical spec
    "What are the API rate limits for a Pro plan?",
    # strategy: "web"     — current event, LLM training data is stale
    "What is the current price of Bitcoin?",
    # strategy: "simple"  — general knowledge LLM knows well
    "Who wrote Hamlet?",
]
