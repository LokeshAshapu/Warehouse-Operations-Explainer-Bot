"""
Retriever module for the Warehouse RAG Pipeline (FAISS backend).
Performs similarity search against FAISS index and returns top-k chunks with sources.
"""

from langchain_community.vectorstores import FAISS
try:
    from langchain_core.documents import Document
except ImportError:
    from langchain.schema import Document


def retrieve(query: str, vectorstore: FAISS, k: int = 4) -> tuple[list[Document], list[str]]:
    """
    Retrieve the most relevant document chunks for a query.

    Args:
        query: User's question
        vectorstore: Loaded FAISS instance
        k: Number of top chunks to retrieve

    Returns:
        (docs, sources) where docs is a list of Document objects
        and sources is a list of unique source filenames
    """
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k}
    )

    docs = retriever.invoke(query)

    # Extract unique source filenames for citation display
    sources = list({doc.metadata.get("source", "Unknown") for doc in docs})
    sources.sort()

    return docs, sources


def format_context(docs: list[Document]) -> str:
    """Combine retrieved chunks into a single context string for the prompt."""
    context_parts = []
    for i, doc in enumerate(docs, 1):
        source = doc.metadata.get("source", "Unknown")
        context_parts.append(f"[Source {i} - {source}]\n{doc.page_content.strip()}")

    return "\n\n---\n\n".join(context_parts)
