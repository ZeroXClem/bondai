import os
from termcolor import cprint
from .langchain import build_langchain_tools, is_langchain_installed
from bondai.tools import HumanTool
from bondai.tools.agent import AgentTool
from bondai.tools.alpaca import CreateOrderTool, GetAccountTool, ListPositionsTool
from bondai.tools.file import FileQueryTool, FileReadTool, FileWriteTool
from bondai.tools.gmail import ListEmailsTool, QueryEmailsTool
from bondai.tools.search import GoogleSearchTool, DuckDuckGoSearchTool
from bondai.tools.website import (
    DownloadFileTool,
    WebsiteQueryTool,
)

def build_tool_options():
    tool_options = [
        DownloadFileTool(),
        FileQueryTool(),
        FileWriteTool(), 
        WebsiteQueryTool(),
    ]

    if os.environ.get('ALPACA_API_KEY') and os.environ.get('ALPACA_SECRET_KEY'):
        tool_options.append(CreateOrderTool())
        tool_options.append(GetAccountTool())
        tool_options.append(ListPositionsTool())
    else:
        cprint("Skipping Alpaca Markets tools because ALPACA_API_KEY and ALPACA_SECRET_KEY environment variables are not set.", "yellow")

    if os.environ.get('GOOGLE_API_KEY') and os.environ.get('GOOGLE_CSE_ID'):
        tool_options.append(GoogleSearchTool())
    else:
        tool_options.append(DuckDuckGoSearchTool())
        cprint("Skipping Google Search tool because GOOGLE_API_KEY and GOOGLE_CSE_ID environment variables are not set.", "yellow")

    if 'gmail-token.pickle' in os.listdir():
        tool_options.append(ListEmailsTool())
        tool_options.append(QueryEmailsTool())
    else:
        cprint("Skipping Gmail tools because gmail-token.pickle file is not present.", "yellow")
    
    if is_langchain_installed():
        cprint("Loading LangChain tools...", "yellow")
        langchain_tools = build_langchain_tools()
        for t in langchain_tools:
            tool_options.append(t)
        cprint("Done loading LangChain tools", "yellow")

    return tool_options

