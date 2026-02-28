"""
Vector Store Manager using FAISS (Facebook AI Similarity Search)
Handles building, persisting, and loading the warehouse knowledge vector store.
"""

import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

FAISS_INDEX_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "faiss_index")
FAISS_INDEX_NAME = "warehouse_knowledge"


def get_embeddings(api_key: str) -> GoogleGenerativeAIEmbeddings:
    """Initialize Google Generative AI embeddings."""
    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=api_key
    )


def build_store(chunks: list[Document], api_key: str) -> FAISS:
    """
    Build and persist a new FAISS vector store from document chunks.
    Saves index to ./faiss_index/ directory.
    """
    print(f"[Vector Store] Building FAISS index at: {FAISS_INDEX_DIR}")
    embeddings = get_embeddings(api_key)

    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings,
    )

    os.makedirs(FAISS_INDEX_DIR, exist_ok=True)
    vectorstore.save_local(FAISS_INDEX_DIR, index_name=FAISS_INDEX_NAME)
    print(f"[Vector Store] FAISS index saved with {len(chunks)} chunks.")
    return vectorstore


def load_store(api_key: str) -> FAISS:
    """
    Load an existing FAISS vector store from disk.
    Raises FileNotFoundError if the index hasn't been built yet.
    """
    if not is_store_ready():
        raise FileNotFoundError(
            f"FAISS index not found at '{FAISS_INDEX_DIR}'. "
            "Please run init_vectordb.py first."
        )

    embeddings = get_embeddings(api_key)
    vectorstore = FAISS.load_local(
        FAISS_INDEX_DIR,
        embeddings=embeddings,
        index_name=FAISS_INDEX_NAME,
        allow_dangerous_deserialization=True,
    )
    print(f"[Vector Store] FAISS index loaded from: {FAISS_INDEX_DIR}")
    return vectorstore


def is_store_ready() -> bool:
    """Check if the FAISS index files exist on disk."""
    faiss_file = os.path.join(FAISS_INDEX_DIR, f"{FAISS_INDEX_NAME}.faiss")
    pkl_file   = os.path.join(FAISS_INDEX_DIR, f"{FAISS_INDEX_NAME}.pkl")
    return os.path.exists(faiss_file) and os.path.exists(pkl_file)
