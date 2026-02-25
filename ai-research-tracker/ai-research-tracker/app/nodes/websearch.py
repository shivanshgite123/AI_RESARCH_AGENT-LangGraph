import os
from app.state import AgentState
from dotenv import load_dotenv

load_dotenv()


def web_search(state: AgentState) -> dict:
    """
    Performs a web search using Tavily API and returns results as context.
    """
    query = state["question"]
    print(f"[WebSearch Node] Searching for: {query}")

    try:
        from tavily import TavilyClient

        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            raise ValueError("TAVILY_API_KEY not found in environment variables.")

        client = TavilyClient(api_key=api_key)
        response = client.search(query=query, max_results=3)

        # Extract and format results
        results = []
        for item in response.get("results", []):
            title = item.get("title", "")
            content = item.get("content", "")
            url = item.get("url", "")
            results.append(f"Title: {title}\nContent: {content}\nSource: {url}")

        web_results = "\n\n---\n\n".join(results) if results else "No results found."
        print(f"[WebSearch Node] Found {len(results)} results.")

    except ImportError:
        web_results = "Tavily package not installed. Run: pip install tavily-python"
        print(f"[WebSearch Node] Import error: {web_results}")
    except Exception as e:
        web_results = f"Web search failed: {str(e)}"
        print(f"[WebSearch Node] Error: {e}")

    return {"web_results": web_results}
