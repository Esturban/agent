from dotenv import load_dotenv
from src.tools import PDF_URL
from src.workflow import create_workflow


def main():
    load_dotenv()
    app = create_workflow()

    print(f"Extracting from: {PDF_URL}")
    result = app.invoke(
        {
            "url": PDF_URL,
            "pdf_text": "",
            "extracted": {},
            "retries": 0,
            "success": False,
        }
    )

    if result["success"]:
        print("\nExtracted:")
        for k, v in result["extracted"].items():
            print(f"  {k}: {v}")
    else:
        print(f"Extraction failed after {result['retries']} retries")


if __name__ == "__main__":
    main()
