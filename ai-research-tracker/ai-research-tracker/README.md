#  AI Research Tracker

A **LangGraph + Gemini RAG System** that intelligently answers AI research questions by routing between a local vector database and real-time web search.



##  Architecture

```
User → FastAPI → LangGraph Workflow
                      ↓
                Router Node
               /            \
        RAG Node         WebSearch Node
         (ChromaDB)        (Tavily)
               \            /
            Generate Node (Gemini LLM)
                      ↓
                  Response
```

**Routing Logic:**
- Questions with keywords like `latest`, `2024`, `2025`, `2026`, `current`, `news` → **Web Search**
- All other questions → **RAG (Vector Store)**



##  Folder Structure

```
ai-research-tracker/
├── app/
│   ├── main.py              # FastAPI app
│   ├── graph.py             # LangGraph workflow
│   ├── state.py             # AgentState TypedDict
│   ├── nodes/
│   │     ├── router.py      # Route: rag or websearch
│   │     ├── rag.py         # Retrieve from ChromaDB
│   │     ├── websearch.py   # Tavily web search
│   │     └── generate.py    # Gemini LLM response
│   ├── services/
│   │     ├── gemini.py      # Gemini LLM client
│   │     └── vectorstore.py # ChromaDB + embeddings
├── requirements.txt
├── .env.example
└── README.md
```
File                                           Description
app/main.py                 FastAPI with CORS, Pydantic models, proper error handling
app/graph.py                LangGraph workflow with build_graph() factory function
app/state.py                AgentState with Optional types
app/nodes/router.py         Smart routing with 10+ keyword triggers
app/nodes/rag.py            ChromaDB retrieval with error handling
app/nodes/websearch.py      Tavily search with structured result formatting
app/nodes/generate.py       Gemini prompt with clear instructions & source labeling
app/services/gemini.py      LLM client with lazy init
app/services/vectorstore.py ChromaDB + Gemini embeddings + 5 seed research docs

##  Setup

### 1. Clone & Install

```bash
cd ai-research-tracker
pip install -r requirements.txt
```

### 2. Configure API Keys

```bash
cp .env.example .env
```

Edit `.env`:
```
GOOGLE_API_KEY=your_gemini_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

Get your keys:
- **Google Gemini**: https://aistudio.google.com/app/apikey
- **Tavily**: https://app.tavily.com

### 3. Run the App

```bash
uvicorn app.main:app --reload
```

API available at: `http://localhost:8000`

Interactive docs: `http://localhost:8000/docs`



##  API Usage

### POST `/chat`

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the Transformer architecture?"}'
```

**Response:**
```json
{
  "question": "What is the Transformer architecture?",
  "response": "The Transformer architecture was introduced in...",
  "route": "rag"
}
```

### Web Search Example

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the latest advancements in AI research 2026?"}'
```

This will route to **web search** (due to "latest" and "2026" keywords).



##  Pre-loaded Research Documents

The vector store comes pre-seeded with summaries on:
- Transformer architecture (Vaswani et al., 2017)
- RAG – Retrieval Augmented Generation (Lewis et al., 2020)
- LangGraph framework
- GPT-4 (OpenAI, 2023)
- BERT (Devlin et al., 2018)



| `GOOGLE_API_KEY` | Google Gemini API key |
| `TAVILY_API_KEY` | Tavily Search API key |
