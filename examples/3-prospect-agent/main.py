import os
import json
from dotenv import load_dotenv
from time import time
import pandas as pd
from langchain_openai import ChatOpenAI

# Import from new modules
from src.models import State, OutputSchema
from src.tools import create_tools
from src.workflow import create_workflow
from src.agent import run_agent


load_dotenv()
brave_key = os.getenv("BRAVE_API_KEY")

def prospect_agent(prospect_path: str, output_suffix: str):
    # minimal CSV handling: read and ensure not empty
    prospects = pd.read_csv(prospect_path)[:2]
    if prospects.empty:
        raise ValueError(f"Prospects CSV is empty or unreadable: {prospect_path}")

    # Set up LLM
    llm = ChatOpenAI(model="gpt-5-nano", temperature=0)

    # Create tools and workflow
    tools, tool_node = create_tools(brave_key)
    graph = create_workflow(llm, tools, tool_node)

    # run_agent now returns (generated_message, confidence, source_summary)
    cols = prospects.apply(lambda row: pd.Series(run_agent(row, llm, tools[0])), axis=1)
    cols.columns = ["generated_message", "confidence", "source_summary"]
    prospects = pd.concat([prospects, cols], axis=1)

    out_dir = os.path.dirname(output_suffix)  # Fixed: was output_path, should be output_suffix
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    prospects.to_csv(f"{output_suffix}_{time()}.csv", index=False)
    

if __name__ == "__main__":
    prospect_agent(prospect_path="data/sample_connections.csv", output_suffix="data/aug/connections_aug")
