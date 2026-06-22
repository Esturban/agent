TASK_PROMPT = (
    "I have uploaded calculator.py and test_calculator.py. "
    "test_add() currently fails because add() subtracts instead of adding. "
    "Fix calculator.py so all tests pass. "
    "Return the corrected calculator.py content only."
)

EXPECTED_FIX = "return a + b"


def format_result(events: list[tuple[str, dict]]) -> str:
    """Concatenate message_chunk content from the event stream."""
    return "".join(
        data.get("content", "")
        for et, data in events
        if et == "message_chunk"
    )
