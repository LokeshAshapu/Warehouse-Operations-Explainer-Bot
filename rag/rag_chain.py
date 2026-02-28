"""
RAG Chain - Combines vector retrieval with Gemini Flash generation.
This is the core of the warehouse explainer bot.
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

try:
    from langchain_community.vectorstores import FAISS
except ImportError:
    raise ImportError("Please install faiss-cpu: pip install faiss-cpu")
try:
    from langchain_core.documents import Document
except ImportError:
    from langchain.schema import Document

from rag.retriever import retrieve, format_context
from bot.gemini_client import GeminiClient
from bot.prompt_templates import build_rag_prompt


def run_rag_chain(
    query: str,
    vectorstore,
    gemini_client: GeminiClient,
    chat_history: list[dict] = None,
    k: int = 4
) -> tuple[str, list[str], list]:
    """
    Execute the full RAG pipeline:
    1. Retrieve relevant chunks from vector store
    2. Build a grounded prompt with context
    3. Generate answer with Gemini Flash
    
    Args:
        query: User's question
        vectorstore: Loaded ChromaDB instance
        gemini_client: Initialized Gemini client
        chat_history: Previous conversation turns (optional)
        k: Number of context chunks to retrieve
    
    Returns:
        (answer, sources, docs)
        - answer: Generated response text
        - sources: List of source document filenames
        - docs: Raw Document chunks used as context
    """
    # Step 1: Retrieve relevant context
    docs, sources = retrieve(query, vectorstore, k=k)
    context = format_context(docs)
    
    # Step 2: Build the RAG prompt
    prompt = build_rag_prompt(query=query, context=context)
    
    # Step 3: Generate answer
    answer = gemini_client.generate(prompt)
    
    return answer, sources, docs
