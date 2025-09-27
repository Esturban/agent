from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain.tools.retriever import create_retriever_tool
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import SystemMessage
from ..tools import get_laptop_price
from langchain_openai import ChatOpenAI
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
_repo_root = Path(__file__).parent.parent.parent.parent.parent


def product_qna(user_input: str):
    llm = ChatOpenAI(model="gpt-5-nano")
    #Create the embedding model
    embedding=OpenAIEmbeddings(model="text-embedding-3-small")

    #print(get_laptop_price("alpha"))
    #print(get_laptop_price("testing"))

    # Load, chunk and index the contents of the product featuers document.
    loader=PyPDFLoader(f"{_repo_root}/data/product/Laptop product descriptions.pdf")
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=256)
    splits = text_splitter.split_documents(docs)

    #Create a vector store with Chroma
    prod_feature_store = Chroma.from_documents(
        documents=splits, 
        embedding=embedding
    )

    get_product_features = create_retriever_tool(
        prod_feature_store.as_retriever(search_kwargs={"k": 1}),
        name="Get_Product_Features",
        description="""
        This store contains details about Laptops. It lists the available laptops
        and their features including CPU, memory, storage, design and advantages
        """
    )


    #Create a System prompt to provide a persona to the chatbot
    system_prompt = SystemMessage("""
        You are professional chatbot that answers questions about laptops sold by your company.
        To answer questions about laptops, you will ONLY use the available tools and NOT your own memory.
        You will handle small talk and greetings by producing professional responses.
        """
    )

    #Create a list of tools available
    tools = [get_laptop_price, get_product_features]

    #Create memory across questions in a conversation (conversation memory)
    checkpointer=MemorySaver()

    #Create a Product QnA Agent. This is actual a graph in langGraph
    product_QnA_agent=create_react_agent(
                                    model=llm, #LLM to use
                                    tools=tools, #List of tools to use
                                    prompt=system_prompt, #The system prompt
                                    debug=False, #Debugging turned on if needed
                                    checkpointer=checkpointer #For conversation memory
    )
    return product_QnA_agent