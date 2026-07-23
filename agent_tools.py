from langchain_community.tools.tavily_search import TavilySearchResults


def get_search_tool():
    return TavilySearchResults(max_results=5, search_depth="advanced")
