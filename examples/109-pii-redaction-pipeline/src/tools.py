from presidio_analyzer import AnalyzerEngine, Pattern, PatternRecognizer
from presidio_anonymizer import AnonymizerEngine

SAMPLE_DOCUMENTS = [
    """Customer complaint from John Smith (john.smith@gmail.com, 555-867-5309).
    His SSN is 123-45-6789 and credit card 4532-1234-5678-9012.
    He lives at 742 Evergreen Terrace, Springfield, IL 62701.""",

    """Meeting notes: Sarah Connor (sarah.c@skynet.ai) called from +1-800-555-0199.
    Her employee ID is EMP-9841 and IP address 192.168.1.42 flagged suspicious.""",
]

SAMPLE_LLM_RESPONSE = """Based on our records, the customer John Doe (DOB: 1985-03-15) with
account number ACC-789456 and phone 555-234-5678 has been escalated.
Their email john.doe@example.com should receive the refund confirmation."""


def build_engines() -> tuple[AnalyzerEngine, AnonymizerEngine]:
    analyzer = AnalyzerEngine()
    analyzer.registry.add_recognizer(
        PatternRecognizer(
            supported_entity="US_SSN",
            patterns=[Pattern("us_ssn", r"\b\d{3}-\d{2}-\d{4}\b", 0.95)],
        )
    )
    analyzer.registry.add_recognizer(
        PatternRecognizer(
            supported_entity="EMPLOYEE_ID",
            patterns=[Pattern("employee_id", r"\bEMP-\d{4}\b", 0.9)],
        )
    )
    anonymizer = AnonymizerEngine()
    return analyzer, anonymizer


def redact(text: str, analyzer: AnalyzerEngine, anonymizer: AnonymizerEngine) -> tuple[str, list]:
    results = analyzer.analyze(text=text, language="en")
    redacted = anonymizer.anonymize(text=text, analyzer_results=results)
    entities_found = [
        {"type": r.entity_type, "score": round(r.score, 2), "text": text[r.start:r.end]}
        for r in results
    ]
    return redacted.text, entities_found
