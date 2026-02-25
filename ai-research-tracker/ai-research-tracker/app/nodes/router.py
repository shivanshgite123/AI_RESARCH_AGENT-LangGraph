from typing import Literal
from app.state import AgentState

# Keywords that suggest a need for real-time web search
WEB_SEARCH_KEYWORDS = [
    "latest", "recent", "new", "2024", "2025", "2026",
    "today", "current", "now", "breaking", "just released",
    "announced", "update", "news"
]


def route_question(state: AgentState) -> Literal["rag", "websearch"]:
    """
    Routes the question to either the RAG node or Web Search node.
    - If question contains time-sensitive keywords → websearch
    - Otherwise → rag (vector database lookup)
    """
    question = state["question"].lower()

    for keyword in WEB_SEARCH_KEYWORDS:
        if keyword in question:
            print(f"[Router] Routing to WEBSEARCH (matched keyword: '{keyword}')")
            return "websearch"

    print("[Router] Routing to RAG")
    return "rag"
