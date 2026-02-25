from typing import TypedDict, List, Optional


class AgentState(TypedDict):
    question: str
    documents: Optional[List[str]]
    web_results: Optional[str]
    generation: Optional[str]
