from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

SAMPLE_DOCS = [
    "Albert Einstein was born on March 14, 1879 in Ulm, Germany.",
    "Einstein developed the special theory of relativity in 1905 while working at the Swiss patent office.",
    "The general theory of relativity, published in 1915, describes gravity as spacetime curvature.",
    "Einstein received the Nobel Prize in Physics in 1921 for his discovery of the photoelectric effect.",
    "E=mc2 expresses the equivalence of energy and mass, derived from special relativity.",
    "The photoelectric effect shows that light behaves as quantized packets called photons.",
    "Quantum mechanics describes the behavior of particles at the subatomic scale.",
    "Special relativity shows that the speed of light is constant in all inertial frames.",
    "Einstein's academic career included positions at Zurich, Prague, and Princeton's IAS.",
    "The Manhattan Project, which Einstein indirectly influenced, led to atomic weapons in 1945.",
]

SAMPLE_QUERIES = [
    "What year did Einstein win the Nobel Prize?",
    "Where did Einstein develop special relativity?",
    "What does E=mc2 mean and where does it come from?",
]

STEP_BACK_PROMPT = (
    "You are an expert at widening specific questions into broader background questions. "
    "Given a specific factual question, produce a single broader question that would retrieve "
    "the background knowledge needed to answer the original. "
    "Output only the broader question, nothing else."
)


def build_vectorstore() -> Chroma:
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    return Chroma.from_texts(SAMPLE_DOCS, embeddings, collection_name="stepback-demo")
