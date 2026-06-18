from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from .tools import SYSTEM_PROMPT


def create_workflow():
    try:
        from langchain_community.agent_toolkits import PlaywrightBrowserToolkit
        from langchain_community.tools.playwright.utils import create_sync_playwright_browser
    except ImportError:
        raise SystemExit(
            "Playwright not installed. Run:\n"
            "  pip install playwright && playwright install chromium"
        )

    browser = create_sync_playwright_browser()
    toolkit = PlaywrightBrowserToolkit.from_browser(sync_browser=browser)
    tools = toolkit.get_tools()

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    return create_react_agent(llm, tools, state_modifier=SYSTEM_PROMPT)
