from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from .tools import build_engines, redact

# ── Prompts ──────────────────────────────────────────────────────────────────

# Grounded instruction: the LLM only sees the pre-redacted document, so it
# cannot leak original PII even if it tries to quote the source verbatim.
REDACTION_SYSTEM = "You are a helpful assistant. Answer based only on the provided document."

# Document wrapper keeps data clearly separated from the question,
# reducing prompt-injection risk from malicious document content.
REDACTION_USER = "Document:\n{document}\n\nQuestion: {question}"

# ── Pipeline ──────────────────────────────────────────────────────────────────


def run_pipeline(raw_document: str, question: str) -> dict:
    """
    Two-stage PII pipeline:
    1. Pre-ingestion: redact PII from document before sending to LLM
    2. Post-generation: redact any PII the LLM leaks in its response
    """
    analyzer, anonymizer = build_engines()

    # Stage 1: scrub input before LLM sees it
    clean_doc, pre_entities = redact(raw_document, analyzer, anonymizer)

    llm = ChatOpenAI(model="gpt-5.4-nano", temperature=0)
    messages = [
        SystemMessage(content=REDACTION_SYSTEM),
        HumanMessage(content=REDACTION_USER.format(document=clean_doc, question=question)),
    ]
    raw_response = llm.invoke(messages).content

    # Stage 2: scrub any PII the LLM included in its response
    clean_response, post_entities = redact(raw_response, analyzer, anonymizer)

    return {
        "original_doc": raw_document,
        "pre_redacted_doc": clean_doc,
        "pre_entities": pre_entities,
        "raw_llm_response": raw_response,
        "final_response": clean_response,
        "post_entities": post_entities,
    }
