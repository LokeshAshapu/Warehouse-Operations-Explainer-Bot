"""
init_vectordb.py — One-time FAISS vector store initialization script.

Run this BEFORE launching the Streamlit app:
    python init_vectordb.py

This script:
  1. Loads all .txt knowledge base files from data/
  2. Splits them into overlapping chunks
  3. Embeds each chunk using Google gemini-embedding-001
  4. Persists the FAISS index to ./faiss_index/
"""

import os
import sys
import time
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY", "")
if not API_KEY:
    print("❌ ERROR: GOOGLE_API_KEY not found in environment.")
    print("   Please create a .env file with: GOOGLE_API_KEY=your_key_here")
    sys.exit(1)

print("=" * 60)
print("  WarehouseBot — FAISS Vector DB Initialization")
print("=" * 60)
print()

# ── Step 1: Load and chunk documents ──────────────────────────────────────
print("📂 Step 1: Loading knowledge base documents...")
from rag.document_loader import load_and_chunk
chunks = load_and_chunk()
print(f"   ✅ {len(chunks)} chunks ready for embedding.\n")

# ── Step 2: Build FAISS vector store ──────────────────────────────────────
print("🔢 Step 2: Embedding chunks and building FAISS index...")
print("   (This may take 30–90 seconds for the first run)")
from rag.vector_store import build_store

start = time.time()
vectorstore = build_store(chunks, api_key=API_KEY)
elapsed = time.time() - start
print(f"   ✅ FAISS index built in {elapsed:.1f}s\n")

# ── Step 3: Quick retrieval test ───────────────────────────────────────────
print("🧪 Step 3: Running retrieval smoke test...")
from rag.retriever import retrieve

test_queries = [
    "What is the inbound receiving process?",
    "What safety PPE is required in a warehouse?",
    "How does order picking work?",
]

for q in test_queries:
    docs, sources = retrieve(q, vectorstore, k=2)
    print(f"   Query : '{q}'")
    print(f"   Found : {len(docs)} chunks from → {sources}")
    print()

print("=" * 60)
print("  ✅ FAISS Initialization COMPLETE!")
print()
print("  FAISS index saved to: ./faiss_index/")
print()
print("  Next step: launch the app with:")
print("    python -m streamlit run app.py")
print("=" * 60)
