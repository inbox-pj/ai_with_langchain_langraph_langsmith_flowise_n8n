from langchain_tavily import TavilySearch


def get_tools():
    tools = [TavilySearch()]
    return tools
