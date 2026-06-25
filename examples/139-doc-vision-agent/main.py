import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from src.workflow import create_workflow

load_dotenv()

SCHEMA_PROMPT = """Extract the following fields from this document page as JSON:
{
  "title": "string or null",
  "date": "string or null",
  "key_numbers": ["list of numeric values mentioned"],
  "summary": "one sentence summary"
}"""

SAMPLE_PDF = "https://www.w3.org/WAI/WCAG21/wcag21.pdf"

if __name__ == "__main__":
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    workflow = create_workflow()
    config = {"configurable": {"client": client, "model": "gpt-4o-mini"}}

    result = workflow.invoke(
        {"pdf_source": SAMPLE_PDF, "schema_prompt": SCHEMA_PROMPT, "page_count": 0, "results": []},
        config=config,
    )
    print(f"Processed {result['page_count']} pages\n")
    for page in result["results"]:
        print(f"Page {page['page']}:")
        print(json.dumps(page, indent=2))
        print()
