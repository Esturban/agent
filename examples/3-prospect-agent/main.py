import os
import json
import argparse
from datetime import datetime
from dotenv import load_dotenv
from time import time
import pandas as pd
from langchain_openai import ChatOpenAI

# Import from new modules
from src.models import ProspectMetadata
from src.tools import create_tools
from src.workflow import create_workflow


load_dotenv()
brave_key = os.getenv("BRAVE_API_KEY")

def prospect_agent(prospect_path: str, output_suffix: str, since_date: str = None, to_date: str = None):
    # minimal CSV handling: read and ensure not empty
    # Skip the first 3 lines which contain LinkedIn export notes
    prospects = pd.read_csv(prospect_path, skiprows=3)
    print(f"Raw prospects: {prospects.shape[0]}")
    if prospects.empty:
        raise ValueError(f"Prospects CSV is empty or unreadable: {prospect_path}")

    # Simple filtering if since_date is provided
    if since_date:
        try:
            since_date_dt = datetime.strptime(since_date, "%Y-%m-%d")  # CLI input in YYYY-MM-DD
            prospects['Connected On'] = pd.to_datetime(prospects['Connected On'], format="%d %b %Y", errors='coerce')  # CSV format: DD MMM YYYY
            prospects = prospects[prospects['Connected On'] >= since_date_dt].dropna(subset=['Connected On'])
            print(f"Filtered prospects: {prospects.shape[0]}")
            if prospects.empty:
                print("No prospects found after the specified since_date.")
        except ValueError:
            raise ValueError("Invalid since_date format. Use YYYY-MM-DD.")
    if to_date:
        try:
            to_date_dt = datetime.strptime(to_date, "%Y-%m-%d")
            prospects = prospects[prospects['Connected On'] <= to_date_dt].dropna(subset=['Connected On'])
            print(f"Filtered prospects: {prospects.shape[0]}")
        except ValueError:
            raise ValueError("Invalid to_date format. Use YYYY-MM-DD.")

    # Set up LLMs - researcher uses gpt-5-nano for efficiency, copywriter uses gpt-5 for quality
    researcher_llm = ChatOpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPENROUTER_API_KEY"), model="alibaba/tongyi-deepresearch-30b-a3b:free", temperature=0)
    copywriter_llm = ChatOpenAI(model="gpt-5-mini", temperature=0)

    # Create tools and workflow
    tools, tool_node = create_tools(brave_key)
    graph = create_workflow(researcher_llm, copywriter_llm, tools[0])

    # Process each prospect through the graph
    def process_prospect(row):
        initial_state = {
            "prospect": ProspectMetadata(
                first_name=row.get("First Name", ""),
                last_name=row.get("Last Name", ""),
                company=row.get("Company", ""),
                position=row.get("Position", "")
            ),
            "research": None,
            "output": None
        }
        result = graph.invoke(initial_state)
        output = result["output"]
        return output.generated_message, output.confidence, output.source_summary
    
    cols = prospects.apply(lambda row: pd.Series(process_prospect(row)), axis=1)
    cols.columns = ["generated_message", "confidence", "source_summary"]
    prospects = pd.concat([prospects, cols], axis=1)

    out_dir = os.path.dirname(output_suffix)  # Fixed: was output_path, should be output_suffix
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    prospects.to_csv(f"{output_suffix}_{datetime.now().strftime("%Y%m%d%H")}.csv", index=False)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prospect Agent CLI")
    parser.add_argument("--input", "-i", default="data/Connections.csv", help="Path to input CSV")
    parser.add_argument("--output_suffix", "-o", default="data/aug/Connections_aug", help="Output CSV suffix")
    parser.add_argument("--since_date", "-s", default="2025-10-04", help="Filter by Connected On >= this date (YYYY-MM-DD)")
    parser.add_argument("--to_date", "-t", default="2025-10-10", help="Filter by Connected On <= this date (YYYY-MM-DD)")
    args = parser.parse_args()

    prospect_agent(args.input, args.output_suffix, args.since_date, args.to_date)
