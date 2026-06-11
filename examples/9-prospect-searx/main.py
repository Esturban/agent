import argparse
import json
import os
from datetime import datetime
from time import time

import pandas as pd
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Import from new modules
from src.models import ProspectMetadata
from src.tools import create_tools
from src.workflow import create_workflow

load_dotenv()


def prospect_agent(
    prospect_path: str, output_suffix: str, since_date: str = None, to_date: str = None
):
    # minimal CSV handling: read and ensure not empty
    # Skip the first 3 lines which contain LinkedIn export notes
    start_time = time()
    prospects = pd.read_csv(prospect_path, skiprows=3)
    prospects = prospects.dropna(subset=["First Name", "Last Name", "Company", "Position"])
    print(f"Raw prospects: {prospects.shape[0]}")
    if prospects.empty:
        raise ValueError(f"Prospects CSV is empty or unreadable: {prospect_path}")

    # Simple filtering if since_date is provided
    if since_date:
        try:
            since_date_dt = datetime.strptime(since_date, "%Y-%m-%d")  # CLI input in YYYY-MM-DD
            prospects["Connected On"] = pd.to_datetime(
                prospects["Connected On"], format="%d %b %Y", errors="coerce"
            )  # CSV format: DD MMM YYYY
            prospects = prospects[prospects["Connected On"] >= since_date_dt].dropna(
                subset=["Connected On"]
            )
            # print(f"Filtered prospects: {prospects.shape[0]}")
            if prospects.empty:
                print("No prospects found after the specified since_date.")
        except ValueError:
            raise ValueError("Invalid since_date format. Use YYYY-MM-DD.")
    if to_date:
        try:
            to_date_dt = datetime.strptime(to_date, "%Y-%m-%d")
            prospects = prospects[prospects["Connected On"] <= to_date_dt].dropna(
                subset=["Connected On"]
            )
            print(f"Filtered prospects: {prospects.shape[0]}")
        except ValueError:
            raise ValueError("Invalid to_date format. Use YYYY-MM-DD.")

    # Set up LLMs - researcher uses gpt-5-nano for efficiency, copywriter uses gpt-5 for quality
    researcher_llm = ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        model="alibaba/tongyi-deepresearch-30b-a3b:free",
        temperature=0,
    )
    copywriter_llm = ChatOpenAI(model="gpt-5-mini")

    # Wait spacing for rate limiting
    wait_seconds = float(os.getenv("SEARCH_WAIT_SECONDS", "1.0"))

    # Create tools and workflow (SearXNG)
    tools, tool_node = create_tools(wait_seconds=wait_seconds)
    graph = create_workflow(researcher_llm, copywriter_llm, tools[0])

    # Process each prospect through the graph sequentially so we can capture
    # progress and exit gracefully on the first error, reporting the last
    # successfully processed prospect and timing information.
    def process_prospect(row, max_retries: int = 2, backoff_seconds: float = 1.0):
        print(
            f"Processing prospect: {row.get('First Name', '')} {row.get('Last Name', '')} {row.get('Company', '')} {row.get('Position', '')}"
        )
        initial_state = {
            "prospect": ProspectMetadata(
                first_name=row.get("First Name", ""),
                last_name=row.get("Last Name", ""),
                company=row.get("Company", ""),
                position=row.get("Position", ""),
            ),
            "research": None,
            "output": None,
        }

        last_exc = None
        for attempt in range(1, max_retries + 2):
            try:
                result = graph.invoke(initial_state)
                output = result["output"]
                return (
                    output.generated_message,
                    output.confidence,
                    output.source_summary,
                )
            except Exception as e:
                last_exc = e
                print(
                    f"Attempt {attempt} failed for prospect {row.get('First Name', '')} {row.get('Last Name', '')}: {e}"
                )
                if attempt <= max_retries:
                    print(f"Retrying after {backoff_seconds} seconds...")
                    from time import sleep

                    sleep(backoff_seconds)
                    backoff_seconds *= 2
                    continue
                # Exhausted retries, re-raise the last exception
                raise last_exc

    processed_rows = []
    last_completed = None
    completed_count = 0

    for idx, row in prospects.iterrows():
        try:
            generated_message, confidence, source_summary = process_prospect(row)
            try:
                row_dict = row.to_dict()
            except Exception as to_dict_exc:
                # Debug only on failure: include row representation and exception
                print(f"Failed to convert row at index {idx} to dict: {to_dict_exc}")
                try:
                    # Print the raw row values for inspection
                    print("Row values:", list(row.values))
                except Exception:
                    print("Could not read row.values()")
                # Re-raise to be handled by outer exception handler
                raise

            row_dict.update(
                {
                    "generated_message": generated_message,
                    "confidence": confidence,
                    "source_summary": source_summary,
                }
            )
            processed_rows.append(row_dict)
            last_completed = row_dict
            completed_count += 1
        except Exception as e:
            elapsed = time() - start_time
            print(f"Error processing prospect at index {idx}: {e}")
            # Debug: print the full row content when an error occurs
            try:
                print("Full row (as dict) on failure:", row.to_dict())
            except Exception as row_dict_exc:
                print(f"Could not convert failing row to dict: {row_dict_exc}")
                try:
                    print("Raw row values on failure:", list(row.values))
                except Exception:
                    print("Could not read raw row values on failure")

            if last_completed:
                print("Last completed prospect:")
                try:
                    # Show a concise view including Connected On if present
                    print(
                        json.dumps(
                            {
                                "First Name": last_completed.get("First Name", ""),
                                "Last Name": last_completed.get("Last Name", ""),
                                "Company": last_completed.get("Company", ""),
                                "Position": last_completed.get("Position", ""),
                                "Connected On": str(last_completed.get("Connected On", "")),
                            },
                            indent=2,
                        )
                    )
                except Exception:
                    print(last_completed)
            else:
                print("No prospects completed successfully.")
            print(f"Total completed: {completed_count}")
            print(f"Elapsed time (s): {elapsed:.2f}")

            # Save partial results if any were produced
            if processed_rows:
                partial_path = (
                    f"{output_suffix}_partial_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
                )
                pd.DataFrame(processed_rows).to_csv(partial_path, index=False)
                print(f"Partial results saved to {partial_path}")

            # Re-raise so the caller sees the original failure (we've logged state)
            raise

    # After successful run, persist full results and log summary
    out_dir = os.path.dirname(output_suffix)  # Fixed: was output_path, should be output_suffix
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    result_df = pd.DataFrame(processed_rows)
    final_path = f"{output_suffix}_{datetime.now().strftime('%Y%m%d%H')}.csv"
    result_df.to_csv(final_path, index=False)
    total_elapsed = time() - start_time
    print(f"Completed processing {completed_count} prospects")
    if last_completed:
        print("Last completed prospect:")
        print(
            json.dumps(
                {
                    "First Name": last_completed.get("First Name", ""),
                    "Last Name": last_completed.get("Last Name", ""),
                    "Company": last_completed.get("Company", ""),
                    "Position": last_completed.get("Position", ""),
                    "Connected On": str(last_completed.get("Connected On", "")),
                },
                indent=2,
            )
        )
    print(f"Elapsed time (s): {total_elapsed:.2f}")
    print(f"Results saved to {final_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prospect Agent CLI")
    parser.add_argument("--input", "-i", default="data/Connections.csv", help="Path to input CSV")
    parser.add_argument(
        "--output_suffix",
        "-o",
        default="data/aug/Connections_aug",
        help="Output CSV suffix",
    )
    parser.add_argument(
        "--since_date",
        "-s",
        default="2025-08-01",
        help="Filter by Connected On >= this date (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--to_date",
        "-t",
        default="2025-08-28",
        help="Filter by Connected On <= this date (YYYY-MM-DD)",
    )
    args = parser.parse_args()

    prospect_agent(args.input, args.output_suffix, args.since_date, args.to_date)
