from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.graph import graph

app = FastAPI(
    title="AI Research Tracker",
    description="A LangGraph + Gemini RAG system for answering AI research questions.",
    version="1.0.0"
)

# Allow CORS for local development / front-end testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    question: str
    response: str
    route: str = ""


@app.get("/")
async def root():
    return {
        "message": "AI Research Tracker API is running.",
        "docs": "/docs",
        "endpoints": {
            "POST /chat": "Ask an AI research question",
            "GET /health": "Health check"
        }
    }


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    try:
        # Initialize state
        initial_state = {
            "question": question,
            "documents": None,
            "web_results": None,
            "generation": None
        }

        # Run the LangGraph workflow
        result = graph.invoke(initial_state)

        # Determine which route was used
        route = "websearch" if result.get("web_results") else "rag"

        return ChatResponse(
            question=question,
            response=result.get("generation", "No response generated."),
            route=route
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
