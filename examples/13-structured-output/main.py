import json
import sys

from dotenv import load_dotenv

from src.workflow import create_workflow

load_dotenv()


def main():
    subject = " ".join(sys.argv[1:]) or input("Enter a company or person to profile: ").strip()
    app = create_workflow()
    result = app.invoke({"subject": subject, "raw_results": "", "profile": {}})
    print(json.dumps(result["profile"], indent=2))


if __name__ == "__main__":
    main()
