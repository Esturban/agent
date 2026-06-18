from dotenv import load_dotenv

from src.tools import PAGES
from src.workflow import create_workflow

load_dotenv()

URLS = list(PAGES.keys())


def run(defended: bool) -> list[str]:
    app = create_workflow()
    result = app.invoke({"urls": URLS, "defended": defended, "summaries": []})
    return result["summaries"]


def main() -> None:
    print("=" * 60)
    print("UNDEFENDED AGENT (no instruction hierarchy, no spotlighting)")
    print("=" * 60)
    for s in run(defended=False):
        print(s)
        print()

    print("=" * 60)
    print("DEFENDED AGENT (instruction hierarchy + spotlighting)")
    print("=" * 60)
    for s in run(defended=True):
        print(s)
        print()

    print("Compare the responses on the three malicious pages to see")
    print("how the defended agent rejects injected instructions.")


if __name__ == "__main__":
    main()
