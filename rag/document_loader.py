"""
Document Loader for Warehouse RAG Pipeline
Loads and chunks all .txt files from the data/ directory.
"""

import os
try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
try:
    from langchain_core.documents import Document
except ImportError:
    from langchain.schema import Document


DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def load_documents() -> list[Document]:
    """Load all .txt files from the data directory as LangChain Documents."""
    documents = []
    
    if not os.path.exists(DATA_DIR):
        raise FileNotFoundError(f"Data directory not found: {DATA_DIR}")
    
    txt_files = [f for f in os.listdir(DATA_DIR) if f.endswith(".txt")]
    
    if not txt_files:
        raise ValueError(f"No .txt files found in {DATA_DIR}")
    
    for filename in txt_files:
        filepath = os.path.join(DATA_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        doc = Document(
            page_content=content,
            metadata={"source": filename, "filepath": filepath}
        )
        documents.append(doc)
        print(f"  Loaded: {filename} ({len(content)} characters)")
    
    return documents


def chunk_documents(documents: list[Document], chunk_size: int = 800, chunk_overlap: int = 100) -> list[Document]:
    """Split documents into overlapping chunks for better retrieval."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
        length_function=len,
    )
    
    chunks = splitter.split_documents(documents)
    print(f"  Total chunks created: {len(chunks)}")
    return chunks


def load_and_chunk() -> list[Document]:
    """Full pipeline: load all documents then chunk them."""
    print("[Document Loader] Loading knowledge base documents...")
    docs = load_documents()
    print(f"[Document Loader] Chunking {len(docs)} documents...")
    chunks = chunk_documents(docs)
    return chunks
