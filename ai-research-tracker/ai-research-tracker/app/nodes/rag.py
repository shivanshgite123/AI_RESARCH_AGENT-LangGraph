from app.state import AgentState
from app.services.vectorstore import retrieve


def retrieve_documents(state: AgentState) -> dict:
    """
    Retrieves relevant documents from the vector store based on the question.
    """
    question = state["question"]
    print(f"[RAG Node] Retrieving documents for: {question}")

    try:
        docs = retrieve(question, k=3)
        print(f"[RAG Node] Retrieved {len(docs)} documents.")
    except Exception as e:
        print(f"[RAG Node] Error during retrieval: {e}")
        docs = ["No documents found. Please check your vector store configuration."]

    return {"documents": docs}
