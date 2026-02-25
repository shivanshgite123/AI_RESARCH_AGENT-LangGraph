from langgraph.graph import StateGraph, END
from app.state import AgentState
from app.nodes.router import route_question
from app.nodes.rag import retrieve_documents
from app.nodes.websearch import web_search
from app.nodes.generate import generate_answer


def build_graph():
    """Builds and compiles the LangGraph workflow."""
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("rag", retrieve_documents)
    workflow.add_node("websearch", web_search)
    workflow.add_node("generate", generate_answer)

    # Conditional entry point: route_question decides first step
    workflow.set_conditional_entry_point(
        route_question,
        {
            "rag": "rag",
            "websearch": "websearch"
        }
    )

    # Both paths converge at generate
    workflow.add_edge("rag", "generate")
    workflow.add_edge("websearch", "generate")
    workflow.add_edge("generate", END)

    return workflow.compile()


# Compiled graph instance
graph = build_graph()
