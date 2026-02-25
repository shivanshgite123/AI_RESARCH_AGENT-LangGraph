from app.state import AgentState
from app.services.gemini import generate_response


def generate_answer(state: AgentState) -> dict:
    """
    Generates a final answer using Gemini LLM based on retrieved context.
    """
    question = state["question"]
    documents = state.get("documents") or []
    web_results = state.get("web_results") or ""

    # Determine context source
    if web_results:
        context = web_results
        source_label = "Web Search Results"
    elif documents:
        context = "\n\n".join(documents)
        source_label = "Research Database"
    else:
        context = "No context available."
        source_label = "No Source"

    print(f"[Generate Node] Generating answer using: {source_label}")

    prompt = f"""You are an expert AI research assistant. Answer the user's question based on the context provided below.

Context Source: {source_label}

Context:
{context}

Question: {question}

Instructions:
- Provide a clear, accurate, and detailed answer based on the context.
- If the context is insufficient, say so honestly and provide what you know.
- Use a professional and informative tone.
- Cite the source if available.

Answer:"""

    try:
        response = generate_response(prompt)
        generation = response.content
        print("[Generate Node] Answer generated successfully.")
    except Exception as e:
        generation = f"Error generating response: {str(e)}"
        print(f"[Generate Node] Error: {e}")

    return {"generation": generation}
