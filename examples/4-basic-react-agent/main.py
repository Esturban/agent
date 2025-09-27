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
from src.tools import find_sum, find_product, get_laptop_price
import uuid
import os
import pandas as pd
from pathlib import Path
load_dotenv()

_repo_root = Path(__file__).parent.parent.parent


#Setup the LLM
llm = ChatOpenAI(
    model="gpt-5-nano"
)

#Example 1
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
#inputs = {"messages":[("user","what is the sum of 2 and 3 ?")]}

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
    
## Example 1 End

from src.agent.product_qna import product_qna

import uuid
#To maintain memory, each request should be in the context of a thread.
#Each user conversation will use a separate thread ID
config = {"configurable": {"thread_id": uuid.uuid4()}}

#Test the agent with an input
inputs = {"messages":[
                HumanMessage("What are the features and pricing for GammaAir?")
            ]}
product_QnA_agent = product_qna(llm)
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