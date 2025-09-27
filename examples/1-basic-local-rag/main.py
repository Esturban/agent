from typing import Literal
from langchain_core.messages import HumanMessage
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode
from dotenv import load_dotenv
from src.utils import retrieve_context, export_stategraph


load_dotenv()

# Creating the tool node
tools = [retrieve_context]
tool_node = ToolNode(tools)

# Binding the RAG tool to the model
model = ChatOpenAI(model="gpt-5-nano", temperature=0).bind_tools(tools)


# Function to decide whether to continue or stop the workflow
def should_continue(state: MessagesState) -> Literal["tools", END]:
    messages = state["messages"]
    last_message = messages[-1]
    # If the LLM makes a tool call, go to the "tools" node
    if last_message.tool_calls:
        return "tools"
    # Otherwise, finish the workflow
    return END


# Function that invokes the model
def call_model(state: MessagesState):
    messages = state["messages"]
    response = model.invoke(messages)
    return {"messages": [response]}  # Returns as a list to add to the state


# Define the workflow with LangGraph
workflow = StateGraph(MessagesState)

# Add nodes to the graph
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

# Connect nodes
workflow.add_edge(START, "agent")  # Initial entry
workflow.add_conditional_edges(
    "agent", should_continue
)  # Decision after the "agent" node
workflow.add_edge("tools", "agent")  # Cycle between tools and agent

# Configure memory to persist the state
checkpointer = MemorySaver()

# Compile the graph into a LangChain Runnable application
app = workflow.compile(checkpointer=checkpointer)

# Try to export the stategraph to an image and print the path for convenience
_exported_path = export_stategraph(workflow, out_path="examples/1-basic-local-rag/assets/stategraph.png")
if _exported_path:
    print(f"StateGraph exported to: {_exported_path}")
else:
    print("StateGraph export failed or produced no file.")


# Execute the workflow
final_state = app.invoke(
    {"messages": [HumanMessage(content="Explain what a list is in Python")]},
    config={"configurable": {"thread_id": 42}},
)

# Show the final response
print(final_state["messages"][-1].content)
