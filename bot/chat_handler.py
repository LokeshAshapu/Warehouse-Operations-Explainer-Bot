"""
Chat Handler - Manages Streamlit session state and conversation history.
"""

import streamlit as st
try:
    from langchain_chroma import Chroma
except ImportError:
    from langchain_community.vectorstores import Chroma
from rag.rag_chain import run_rag_chain
from bot.gemini_client import GeminiClient


def initialize_session():
    """Initialize Streamlit session state for chat."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "sources_history" not in st.session_state:
        st.session_state.sources_history = []  # List of source lists per bot message


def add_user_message(content: str):
    """Add a user message to session history."""
    st.session_state.messages.append({"role": "user", "content": content})


def add_bot_message(content: str, sources: list[str]):
    """Add a bot message and its sources to session history."""
    st.session_state.messages.append({"role": "assistant", "content": content})
    st.session_state.sources_history.append(sources)


def handle_query(
    query: str,
    vectorstore: Chroma,
    gemini_client: GeminiClient
) -> tuple[str, list[str]]:
    """
    Process a user query through the RAG chain and update session state.
    
    Returns:
        (answer, sources)
    """
    add_user_message(query)
    
    answer, sources, _ = run_rag_chain(
        query=query,
        vectorstore=vectorstore,
        gemini_client=gemini_client,
    )
    
    add_bot_message(answer, sources)
    return answer, sources


def clear_history():
    """Clear the entire chat history."""
    st.session_state.messages = []
    st.session_state.sources_history = []


def get_bot_message_index(msg_index: int) -> int:
    """
    Given an index in the messages array (which is a bot message),
    return the corresponding index in sources_history.
    """
    bot_count = 0
    for i, msg in enumerate(st.session_state.messages):
        if msg["role"] == "assistant":
            if i == msg_index:
                return bot_count
            bot_count += 1
    return -1
