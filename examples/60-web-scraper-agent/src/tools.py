import requests
from bs4 import BeautifulSoup
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K = 4

SAMPLE_TARGET = "https://en.wikipedia.org/wiki/Retrieval-augmented_generation"

SAMPLE_QUESTIONS = [
    "What is retrieval-augmented generation?",
    "Who introduced RAG and when?",
    "What are the main components of a RAG system?",
]


def fetch_page(url: str) -> str:
    response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()
    return response.text


def parse_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["nav", "footer", "script", "style", "header"]):
        tag.decompose()
    main = soup.find("main") or soup.find("article") or soup.find("body")
    return main.get_text(separator=" ", strip=True) if main else soup.get_text(separator=" ", strip=True)


def chunk_text(text: str) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    return splitter.split_text(text)


def build_vectorstore(chunks: list[str]) -> Chroma:
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    return Chroma.from_texts(chunks, embeddings, collection_name="web-scraper")
