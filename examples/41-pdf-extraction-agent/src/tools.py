from typing import TypedDict

import requests
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

PDF_URL = "https://arxiv.org/pdf/1706.03762"
MAX_RETRIES = 3
CHARS_LIMIT = 3000


class PaperSchema(BaseModel):
    title: str
    year: int
    key_contribution: str
    architecture_name: str


class ExtractionState(TypedDict):
    pdf_text: str
    extracted: dict
    retries: int
    success: bool


def download_pdf_text(url: str) -> str:
    try:
        import io

        import pdfplumber

        resp = requests.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
        with pdfplumber.open(io.BytesIO(resp.content)) as pdf:
            return " ".join(p.extract_text() or "" for p in pdf.pages[:4])
    except Exception as e:
        return f"[PDF download failed: {e}]"


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
extractor = llm.with_structured_output(PaperSchema)
