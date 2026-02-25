import os
from typing import List
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from dotenv import load_dotenv

load_dotenv()

CHROMA_PERSIST_DIR = "./chroma_db"

# Sample seed documents for demo purposes
SEED_DOCUMENTS = [
    Document(
        page_content="Transformer architecture introduced in 'Attention is All You Need' (2017) by Vaswani et al. "
                     "Uses self-attention mechanisms to process sequential data. Key components: multi-head attention, "
                     "positional encoding, feed-forward layers. Revolutionized NLP tasks.",
        metadata={"source": "Vaswani et al., 2017", "topic": "transformers"}
    ),
    Document(
        page_content="Retrieval-Augmented Generation (RAG) combines retrieval systems with language models. "
                     "Introduced by Lewis et al. in 2020. Retrieves relevant documents from a knowledge base "
                     "before generating answers. Reduces hallucination and improves factual accuracy.",
        metadata={"source": "Lewis et al., 2020", "topic": "RAG"}
    ),
    Document(
        page_content="LangGraph is a library for building stateful, multi-actor applications with LLMs. "
                     "It extends LangChain with graph-based workflows. Supports cycles, conditional edges, "
                     "and human-in-the-loop patterns. Ideal for complex agent orchestration.",
        metadata={"source": "LangChain Docs", "topic": "langgraph"}
    ),
    Document(
        page_content="GPT-4 is a large multimodal model from OpenAI. Accepts text and image inputs. "
                     "Significantly outperforms GPT-3.5 on academic benchmarks. Uses RLHF for alignment. "
                     "Context window up to 128k tokens in GPT-4 Turbo.",
        metadata={"source": "OpenAI, 2023", "topic": "LLM"}
    ),
    Document(
        page_content="BERT (Bidirectional Encoder Representations from Transformers) by Devlin et al. 2018. "
                     "Pre-trained on masked language modeling and next sentence prediction. "
                     "Fine-tuned for downstream NLP tasks. Replaced unidirectional models for understanding tasks.",
        metadata={"source": "Devlin et al., 2018", "topic": "BERT"}
    ),
]


def get_embeddings():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables.")
    return GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=api_key
    )


def get_vectorstore() -> Chroma:
    embeddings = get_embeddings()
    vectorstore = Chroma(
        persist_directory=CHROMA_PERSIST_DIR,
        embedding_function=embeddings
    )
    # Seed if empty
    if vectorstore._collection.count() == 0:
        vectorstore.add_documents(SEED_DOCUMENTS)
        print(f"[VectorStore] Seeded {len(SEED_DOCUMENTS)} documents.")
    return vectorstore


def retrieve(query: str, k: int = 3) -> List[str]:
    vectorstore = get_vectorstore()
    docs = vectorstore.similarity_search(query, k=k)
    return [doc.page_content for doc in docs]
