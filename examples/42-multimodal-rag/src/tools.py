import base64
from typing import TypedDict

import httpx
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

IMAGE_DOCS = [
    {
        "id": "cat",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Cat_November_2010-1a.jpg/320px-Cat_November_2010-1a.jpg",
        "label": "a cat",
    },
    {
        "id": "dog",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/YellowLabradorLooking_new.jpg/320px-YellowLabradorLooking_new.jpg",
        "label": "a dog",
    },
    {
        "id": "coffee",
        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/A_small_cup_of_coffee.JPG/320px-A_small_cup_of_coffee.JPG",
        "label": "a cup of coffee",
    },
]

QUERIES = [
    "What animal is in the images?",
    "Is there a beverage shown?",
]


class MultimodalState(TypedDict):
    descriptions: list[str]
    query: str
    answer: str


def fetch_image_b64(url: str) -> str:
    resp = httpx.get(url, timeout=15, follow_redirects=True)
    return base64.b64encode(resp.content).decode()


vision_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2, max_tokens=200)
qa_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
