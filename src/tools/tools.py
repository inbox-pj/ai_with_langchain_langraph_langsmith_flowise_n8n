from langchain_tavily import TavilySearch


def get_profile_url_tavily(name: str):
    search = TavilySearch()
    res = search.run(f"{name}")
    return res
