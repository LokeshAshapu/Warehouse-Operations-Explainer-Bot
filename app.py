"""
Logistics Warehouse Operations Explainer Bot
Project 18 - Hackathon AITAM
Built with: Streamlit | Gemini 1.5 Flash | ChromaDB (RAG)
"""

import os
import sys
import streamlit as st
from dotenv import load_dotenv

# ── Load environment ──────────────────────────────────────────────────────────
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY", "")

# ── Page config (MUST be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="WarehouseBot — Operations Explainer",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS — dark industrial warehouse theme ──────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Global Reset ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Background ── */
.stApp {
    background: linear-gradient(135deg, #0a0e1a 0%, #0d1321 40%, #111827 100%);
    color: #e2e8f0;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    border-right: 1px solid #f59e0b33;
}
section[data-testid="stSidebar"] .stMarkdown h1,
section[data-testid="stSidebar"] .stMarkdown h2,
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: #f59e0b;
}

/* ── Header banner ── */
.wh-header {
    background: linear-gradient(90deg, #1e3a5f 0%, #0f2744 40%, #1a1a2e 100%);
    border: 1px solid #f59e0b44;
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    gap: 20px;
    box-shadow: 0 8px 32px rgba(245, 158, 11, 0.08);
}
.wh-header-icon { font-size: 3.2rem; line-height: 1; }
.wh-header-title { font-size: 2rem; font-weight: 700; color: #f59e0b; margin: 0; letter-spacing: -0.5px; }
.wh-header-sub { font-size: 0.95rem; color: #94a3b8; margin-top: 4px; }

/* ── Chat messages ── */
.wh-msg-user {
    display: flex;
    justify-content: flex-end;
    margin: 12px 0;
}
.wh-msg-user .bubble {
    background: linear-gradient(135deg, #1d4ed8, #2563eb);
    color: #fff;
    padding: 14px 20px;
    border-radius: 20px 20px 4px 20px;
    max-width: 72%;
    font-size: 0.95rem;
    line-height: 1.6;
    box-shadow: 0 4px 16px rgba(37, 99, 235, 0.3);
}
.wh-msg-bot {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    margin: 12px 0;
}
.wh-bot-avatar {
    background: linear-gradient(135deg, #f59e0b, #d97706);
    border-radius: 50%;
    width: 40px; height: 40px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.3rem;
    flex-shrink: 0;
    box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
}
.wh-msg-bot .bubble {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    border: 1px solid #334155;
    color: #e2e8f0;
    padding: 16px 20px;
    border-radius: 4px 20px 20px 20px;
    max-width: 82%;
    font-size: 0.95rem;
    line-height: 1.7;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
}

/* ── Source badge ── */
.src-badge {
    display: inline-block;
    background: #1e293b;
    border: 1px solid #f59e0b55;
    color: #f59e0b;
    font-size: 0.75rem;
    font-family: 'JetBrains Mono', monospace;
    padding: 3px 10px;
    border-radius: 20px;
    margin: 2px 4px 2px 0;
}

/* ── Quick query buttons ── */
.stButton button {
    background: linear-gradient(135deg, #1e293b, #0f172a) !important;
    color: #e2e8f0 !important;
    border: 1px solid #f59e0b55 !important;
    border-radius: 10px !important;
    font-size: 0.82rem !important;
    padding: 8px 12px !important;
    width: 100% !important;
    text-align: left !important;
    transition: all 0.2s ease !important;
}
.stButton button:hover {
    background: linear-gradient(135deg, #f59e0b22, #1e293b) !important;
    border-color: #f59e0b !important;
    color: #f59e0b !important;
    transform: translateX(4px) !important;
}

/* ── Input ── */
.stChatInputContainer, [data-testid="stChatInput"] {
    background: #1e293b !important;
    border: 1px solid #f59e0b55 !important;
    border-radius: 14px !important;
    color: #e2e8f0 !important;
}
textarea, input[type="text"] {
    background: transparent !important;
    color: #e2e8f0 !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
    color: #94a3b8 !important;
    font-size: 0.85rem !important;
}

/* ── Status pill ── */
.status-online {
    display: inline-flex; align-items: center; gap: 6px;
    background: #052e16; border: 1px solid #16a34a55;
    color: #4ade80; font-size: 0.78rem;
    padding: 4px 12px; border-radius: 20px;
}
.status-offline {
    display: inline-flex; align-items: center; gap: 6px;
    background: #450a0a; border: 1px solid #dc262655;
    color: #f87171; font-size: 0.78rem;
    padding: 4px 12px; border-radius: 20px;
}
.dot { width: 7px; height: 7px; border-radius: 50%; display: inline-block; }
.dot-green { background: #4ade80; animation: pulse 2s infinite; }
.dot-red   { background: #f87171; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }

/* ── Divider ── */
hr { border-color: #1e293b !important; }

/* ── Scrollable chat ── */
.chat-container { max-height: 62vh; overflow-y: auto; padding-right: 4px; }
.chat-container::-webkit-scrollbar { width: 4px; }
.chat-container::-webkit-scrollbar-track { background: transparent; }
.chat-container::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)

# ── Lazy imports (after env is loaded) ───────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_resources(api_key: str):
    """
    Load FAISS vector store and Gemini client (cached across rerenders).
    Returns (vectorstore, gemini_client, error_msg)
    """
    try:
        from rag.vector_store import load_store, is_store_ready
        from bot.gemini_client import GeminiClient

        if not is_store_ready():
            return None, None, "FAISS index not found. Please run `python init_vectordb.py` first."

        if not api_key:
            return None, None, "GOOGLE_API_KEY not found in environment. Check your .env file."

        vs  = load_store(api_key)
        gc  = GeminiClient(api_key=api_key)
        return vs, gc, None
    except Exception as e:
        return None, None, str(e)


# ── Session state init ─────────────────────────────────────────────────────
if "messages"       not in st.session_state: st.session_state.messages       = []
if "src_history"    not in st.session_state: st.session_state.src_history    = []
if "pending_query"  not in st.session_state: st.session_state.pending_query  = None

# ── Load resources ─────────────────────────────────────────────────────────
vectorstore, gemini_client, load_error = load_resources(API_KEY)
db_ready = (vectorstore is not None and gemini_client is not None)

# ═══════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🏭 WarehouseBot")
    st.markdown("*AI-Powered Operations Explainer*")
    st.markdown("---")

    # Status pill
    if db_ready:
        st.markdown("""
        <div class="status-online">
            <span class="dot dot-green"></span>
            FAISS Vector DB · Online
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="status-offline">
            <span class="dot dot-red"></span>
            FAISS Vector DB · Offline
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### ⚡ Quick Queries")
    st.markdown("<small style='color:#64748b'>Click to ask instantly</small>", unsafe_allow_html=True)
    st.markdown(" ")

    quick_queries = [
        ("📦", "Explain warehouse inbound process"),
        ("🔍", "What is order picking?"),
        ("📬", "Explain packing and dispatch stages"),
        ("🦺", "What safety rules apply in warehouses?"),
        ("🗄️", "How does warehouse storage and slotting work?"),
        ("↩️", "What is reverse logistics and returns processing?"),
        ("📊", "What KPIs are tracked in a warehouse?"),
        ("🤖", "What is a Warehouse Management System (WMS)?"),
    ]

    for icon, query in quick_queries:
        if st.button(f"{icon}  {query}", key=f"quick_{hash(query)}"):
            st.session_state.pending_query = query

    st.markdown("---")
    st.markdown("### 📚 Knowledge Base")
    st.markdown("""
    <small style='color:#64748b;line-height:1.8'>
    ✅ Warehouse Operations<br>
    ✅ Safety Rules & PPE<br>
    ✅ Standard SOPs (6 docs)<br>
    ✅ KPIs & WMS<br>
    ✅ Returns & HazMat
    </small>
    """, unsafe_allow_html=True)
    st.markdown("---")

    if st.button("🗑️  Clear Chat History", key="clear_chat"):
        st.session_state.messages    = []
        st.session_state.src_history = []
        st.rerun()

    st.markdown("---")
    st.markdown("""
    <small style='color:#475569'>
    <b>Model:</b> Gemini 2.0 Flash<br>
    <b>Vector DB:</b> FAISS (Facebook AI)<br>
    <b>Embeddings:</b> Google gemini-embedding-001<br>
    <b>Framework:</b> LangChain + Streamlit
    </small>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════
# MAIN AREA
# ═══════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="wh-header">
    <div class="wh-header-icon">🏭</div>
    <div>
        <div class="wh-header-title">Warehouse Operations Explainer Bot</div>
        <div class="wh-header-sub">
            Project 18 &nbsp;·&nbsp; RAG-powered &nbsp;·&nbsp; Gemini 1.5 Flash &nbsp;·&nbsp; 
            Explains inbound · storage · picking · packing · dispatch · safety
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Error banner if resources failed to load
if not db_ready:
    st.error(f"⚠️ **System not ready:** {load_error}", icon="🚨")
    st.info("**Steps to fix:**\n1. Ensure `.env` contains your `GOOGLE_API_KEY`\n2. Run `python init_vectordb.py` to build the vector store\n3. Restart this app with `streamlit run app.py`")
    st.stop()

# ── Chat history display ───────────────────────────────────────────────────
bot_msg_counter = 0

with st.container():
    for i, msg in enumerate(st.session_state.messages):
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="wh-msg-user">
                <div class="bubble">💬 {msg['content']}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Get sources for this bot message
            sources = []
            if bot_msg_counter < len(st.session_state.src_history):
                sources = st.session_state.src_history[bot_msg_counter]
            bot_msg_counter += 1

            st.markdown(f"""
            <div class="wh-msg-bot">
                <div class="wh-bot-avatar">🤖</div>
                <div class="bubble">{msg['content']}</div>
            </div>
            """, unsafe_allow_html=True)

            if sources:
                badge_html = "".join(
                    f'<span class="src-badge">📄 {s}</span>' for s in sources
                )
                with st.expander("📚 Retrieved Source Documents", expanded=False):
                    st.markdown(f"<div style='padding:4px 0'>{badge_html}</div>", unsafe_allow_html=True)
                    st.markdown(
                        f"<small style='color:#64748b'>Top {len(sources)} knowledge chunk(s) "
                        f"retrieved via ChromaDB similarity search.</small>",
                        unsafe_allow_html=True
                    )

# Introductory message when chat is empty
if not st.session_state.messages:
    st.markdown("""
    <div style="
        text-align:center; 
        padding: 40px 20px; 
        color: #475569;
        background: linear-gradient(135deg, #0f172a, #1e293b);
        border: 1px dashed #334155;
        border-radius: 16px;
        margin: 20px 0;
    ">
        <div style="font-size:4rem; margin-bottom:16px">🏭</div>
        <div style="font-size:1.3rem; font-weight:600; color:#94a3b8; margin-bottom:8px">
            Welcome to WarehouseBot
        </div>
        <div style="font-size:0.9rem; max-width:500px; margin:0 auto; line-height:1.7">
            I explain logistics and warehouse operational workflows — 
            <b style="color:#f59e0b">inbound receiving, storage, picking, packing, dispatch</b>, 
            safety rules, and SOPs.<br><br>
            Use the <b>Quick Queries</b> in the sidebar, or type your question below! 👇
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Chat input ─────────────────────────────────────────────────────────────
user_input = st.chat_input("Ask about any warehouse operation, process, or safety rule...")

# Handle pending query from sidebar buttons
if st.session_state.pending_query:
    user_input = st.session_state.pending_query
    st.session_state.pending_query = None

# ── Process query ──────────────────────────────────────────────────────────
if user_input and user_input.strip():
    query = user_input.strip()

    # Append user message
    st.session_state.messages.append({"role": "user", "content": query})

    # Generate RAG response
    with st.spinner("🔍 Searching knowledge base and generating answer..."):
        try:
            from rag.rag_chain import run_rag_chain
            answer, sources, _ = run_rag_chain(
                query=query,
                vectorstore=vectorstore,
                gemini_client=gemini_client,
            )
        except Exception as e:
            answer  = f"⚠️ An error occurred: {str(e)}"
            sources = []

    # Append bot message
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.session_state.src_history.append(sources)
    st.rerun()
