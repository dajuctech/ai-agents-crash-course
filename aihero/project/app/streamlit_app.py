"""
Streamlit Web Application - Day 6 Concepts
Interactive web interface for the Tech Interview AI Assistant
"""

import os
import sys
from pathlib import Path
import streamlit as st
import asyncio

# Import modules from the same directory
import ingest
import search_agent
import logs

# Load environment variables from .env file
from dotenv import load_dotenv
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


# Configuration
REPO_OWNER = "yangshun"
REPO_NAME = "tech-interview-handbook"


# --- Initialization ---
@st.cache_resource
def init_agent():
    """
    Initialize the agent with cached resources.
    This runs once and caches the result for better performance.
    """
    st.write("🔄 Downloading Tech Interview Handbook...")

    # Index the data (no filtering needed - use all documents)
    index = ingest.index_data(REPO_OWNER, REPO_NAME, chunk=False)

    st.write("✅ Data indexed successfully!")
    st.write("🤖 Initializing AI agent...")

    # Create the agent
    agent = search_agent.init_agent(index, REPO_OWNER, REPO_NAME)

    st.write("✅ Agent ready!")
    return agent


# Initialize agent
agent = init_agent()


# --- Streamlit UI ---
st.set_page_config(
    page_title="Tech Interview AI Assistant",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Tech Interview AI Assistant")
st.caption("Ask me anything about technical interviews using the Tech Interview Handbook")

# Info expander
with st.expander("ℹ️ About this app"):
    st.markdown("""
    This AI assistant helps you prepare for technical interviews by searching through
    the [Tech Interview Handbook](https://github.com/yangshun/tech-interview-handbook).

    **Features:**
    - 💬 Natural language questions
    - 🔍 Automatic search through documentation
    - 📚 Citations with GitHub links
    - 💾 All interactions are logged for quality improvement

    **Example questions:**
    - What are common behavioral interview questions?
    - How should I prepare for system design interviews?
    - What data structures should I know for coding interviews?
    """)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# --- Streaming helper ---
def stream_response(prompt: str):
    """
    Stream the agent's response for better UX.

    Args:
        prompt: User's question

    Yields:
        Chunks of the response text
    """
    async def agen():
        async with agent.run_stream(user_prompt=prompt) as result:
            last_len = 0
            full_text = ""
            async for chunk in result.stream_output(debounce_by=0.01):
                # Stream only the delta
                new_text = chunk[last_len:]
                last_len = len(chunk)
                full_text = chunk
                if new_text:
                    yield new_text

            # Log once complete
            logs.log_interaction_to_file(agent, result.new_messages())
            st.session_state._last_response = full_text

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    agen_obj = agen()

    try:
        while True:
            piece = loop.run_until_complete(agen_obj.__anext__())
            yield piece
    except StopAsyncIteration:
        return


# --- Chat input ---
if prompt := st.chat_input("Ask your question..."):
    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant message (streamed)
    with st.chat_message("assistant"):
        response_text = st.write_stream(stream_response(prompt))

    # Save full response to history
    final_text = getattr(st.session_state, "_last_response", response_text)
    st.session_state.messages.append({"role": "assistant", "content": final_text})


# --- Sidebar ---
with st.sidebar:
    st.header("📊 Statistics")
    st.metric("Total Messages", len(st.session_state.messages))

    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    st.header("🔗 Links")
    st.markdown(f"""
    - [Tech Interview Handbook](https://github.com/{REPO_OWNER}/{REPO_NAME})
    - [AI Hero Course](https://alexeygrigorev.com/aihero/)
    - [DataTalks.Club](https://datatalks.club/)
    """)

    st.markdown("---")

    st.markdown("""
    <div style='text-align: center; color: #666;'>
    <small>Built with Pydantic AI & Streamlit<br>
    Part of AI Hero Course</small>
    </div>
    """, unsafe_allow_html=True)
