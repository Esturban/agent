from langchain_core.tools import tool
from dotenv import load_dotenv
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AIMessage,HumanMessage,SystemMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import sqlite3
from langchain.tools.retriever import create_retriever_tool
from langchain_chroma import Chroma 
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.checkpoint.memory import MemorySaver

import uuid
import os
import pandas as pd
from pathlib import Path
load_dotenv()

_repo_root = Path(__file__).parent.parent.parent


#Tool annotation identifies a function as a tool automatically
@tool
def find_sum(x:int, y:int) -> int :
    #The docstring comment describes the capabilities of the function
    #It is used by the agent to discover the function's inputs, outputs and capabilities
    """
    This function is used to add two numbers and return their sum.
    It takes two integers as inputs and returns an integer as output.
    """
    return x + y

@tool
def find_product(x:int, y:int) -> int :
    """
    This function is used to multiply two numbers and return their product.
    It takes two integers as inputs and returns an integer as ouput.
    """
    return x * y


#Setup the LLM for the agent


#Setup the LLM
llm = ChatOpenAI(
    model="gpt-5-nano"
)

#Test the model
# response = llm.invoke("Hello, how are you?")
# print(response.content)

#Create list of tools available to the agent
agent_tools=[find_sum, find_product]

#System prompt
system_prompt = SystemMessage(
    """You are a Math genius who can solve math problems. Solve the
    problems provided by the user, by using only tools available. 
    Do not solve the problem yourself"""
)

agent_graph=create_react_agent(
    model=llm, 
    prompt=system_prompt,
    tools=agent_tools,
    # debug=True,
    )

#Example 1
inputs = {"messages":[("user","what is the sum of 2 and 3 ?")]}

#result = agent_graph.invoke(inputs)

#Get the final answer
#print(f"Agent returned : {result['messages'][-1].content} \n")

#print("Step by Step execution : ")
#for message in result['messages']:
#    print(message.pretty_repr())
    
#Example 2
#inputs = {"messages":[("user","What is 3 multipled by 2 and 5 + 1 ?")]}

#result = agent_graph.invoke(inputs)

#Get the final answer
#print(f"Agent returned : {result['messages'][-1].content} \n")

#print("Step by Step execution : ")
#for message in result['messages']:
#    print(message.pretty_repr())
    
    
#Create the embedding model
embedding=OpenAIEmbeddings(model="text-embedding-3-small")

#Load the laptop product pricing CSV into a Pandas dataframe.
product_pricing_df = pd.read_csv(f"{_repo_root}/data/product/Laptop pricing.csv")
#print(product_pricing_df)

@tool
def get_laptop_price(laptop_name:str) -> int :
    """
    This function returns the price of a laptop, given its name as input.
    It performs a substring match between the input name and the laptop name.
    If a match is found, it returns the pricxe of the laptop.
    If there is NO match found, it returns -1
    """

    #Filter Dataframe for matching names
    match_records_df = product_pricing_df[
                        product_pricing_df["Name"].str.contains(
                                                "^" + laptop_name, case=False)
                        ]
    #Check if a record was found, if not return -1
    if len(match_records_df) == 0 :
        return -1
    else:
        return match_records_df["Price"].iloc[0]

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

import uuid
#To maintain memory, each request should be in the context of a thread.
#Each user conversation will use a separate thread ID
config = {"configurable": {"thread_id": uuid.uuid4()}}

#Test the agent with an input
inputs = {"messages":[
                HumanMessage("What are the features and pricing for GammaAir?")
            ]}

#Use streaming to print responses as the agent  does the work.
#This is an alternate way to stream agent responses without waiting for the agent to finish
for stream in product_QnA_agent.stream(inputs, config, stream_mode="values"):
    message=stream["messages"][-1]
    if isinstance(message, tuple):
        print(message)
    else:
        message.pretty_print()
        
user_inputs = [
    "Hello",
    "I am looking to buy a laptop",
    "Give me a list of available laptop names",
    "Tell me about the features of  SpectraBook",
    "How much does it cost?",
    "Give me similar information about OmegaPro",
    "What info do you have on AcmeRight ?",
    "Thanks for the help"
]

#Create a new thread
config = {"configurable": {"thread_id": str(uuid.uuid4())}}

for input in user_inputs:
    print(f"----------------------------------------\nUSER : {input}")
    #Format the user message
    user_message = {"messages":[HumanMessage(input)]}
    #Get response from the agent
    ai_response = product_QnA_agent.invoke(user_message,config=config)
    #Print the response
    print(f"AGENT : {ai_response['messages'][-1].content}")

def execute_prompt(user, config, prompt):
    inputs = {"messages":[("user",prompt)]}
    ai_response = product_QnA_agent.invoke(inputs,config=config)
    print(f"\n{user}: {ai_response['messages'][-1].content}")

#Create different session threads for 2 users
config_1 = {"configurable": {"thread_id": str(uuid.uuid4())}}
config_2 = {"configurable": {"thread_id": str(uuid.uuid4())}}

#Test both threads
execute_prompt("USER 1", config_1, "Tell me about the features of  SpectraBook")
execute_prompt("USER 2", config_2, "Tell me about the features of  GammaAir")
execute_prompt("USER 1", config_1, "What is its price ?")
execute_prompt("USER 2", config_2, "What is its price ?")