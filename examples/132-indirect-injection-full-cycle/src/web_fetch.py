"""
Simulated web fetch and email read tools.

In a real agent, these would call actual APIs. Here we read from the
content/ directory so the demo runs offline, letting you inspect exactly
what the agent fetches and what injection it encounters.

The fetch() function also strips HTML and returns clean text, but
crucially does NOT strip embedded instruction-shaped text — that's what
makes indirect injection dangerous.
"""

import os
import re
from pathlib import Path

CONTENT_DIR = Path(__file__).parent.parent / "content"


def _strip_html_tags(html: str) -> str:
    clean = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.DOTALL)
    clean = re.sub(r"<script[^>]*>.*?</script>", "", clean, flags=re.DOTALL)
    clean = re.sub(r"<!--.*?-->", "", clean, flags=re.DOTALL)
    clean = re.sub(r"<[^>]+>", " ", clean)
    clean = re.sub(r"\s+", " ", clean).strip()
    return clean


def _extract_text_preserving_hidden(html: str) -> str:
    """
    Strip only visible HTML tags but KEEP text inside style=display:none
    and position:absolute elements — this is what a naive fetch does and
    why CSS-hidden injections still reach the model.
    """
    # Remove script/style blocks (content, not tags)
    clean = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL)
    # Preserve content from HTML comments (they contain injection in our demo)
    clean = re.sub(r"<!--", "[COMMENT]", clean)
    clean = re.sub(r"-->", "[/COMMENT]", clean)
    # Strip remaining tags but keep text
    clean = re.sub(r"<[^>]+>", " ", clean)
    clean = re.sub(r"\s+", " ", clean).strip()
    return clean


SOURCES = {
    "https://acmecorp.example/q3-update": CONTENT_DIR / "benign_page.html",
    "https://acmecorp.example/q3-update-compromised": CONTENT_DIR / "poisoned_page.html",
}


def fetch_url(url: str) -> str:
    """Fetch a URL and return extracted text (injection-preserving)."""
    if url not in SOURCES:
        return f"[fetch failed: unknown URL {url}]"
    path = SOURCES[url]
    raw = path.read_text()
    return _extract_text_preserving_hidden(raw)


def read_email(email_id: str) -> str:
    """Read an email by ID. Returns raw text including any hidden instructions."""
    email_map = {
        "email_supplier_q4": CONTENT_DIR / "poisoned_email.txt",
    }
    if email_id not in email_map:
        return f"[email not found: {email_id}]"
    return email_map[email_id].read_text()


def send_email(to: str, subject: str, body: str) -> str:
    """Simulate sending an email (logged, not actually sent)."""
    return f"[SIMULATED] Email sent to={to} subject={subject!r} body_length={len(body)}"


def read_calendar() -> str:
    return "Calendar: Meeting Mon 10am, Dentist Wed 2pm, Sprint review Fri 3pm."


def read_contacts() -> str:
    return "Contacts: Alice (CFO), Bob (Engineering), Carol (Legal), Dave (Sales)."
