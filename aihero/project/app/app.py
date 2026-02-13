import streamlit as st
import asyncio
import ingest
import search_agent
import logs
from dotenv import load_dotenv
load_dotenv('../.env', override=True)

REPOS = [
    ('ing-bank', 'skorecard', 'main'),
    ('guillermo-navas-palencia', 'optbinning', 'master'),
    ('levist7', 'Credit_Risk_Modelling', 'main'),
]


@st.cache_resource
def init_agent():
    st.write("Indexing repos...")
    index = ingest.index_data(REPOS, chunk=True)
    agent = search_agent.init_agent(index)
    return agent


agent = init_agent()

st.set_page_config(page_title="Credit Risk Scorecard Assistant", layout="centered")
st.title("Credit Risk Scorecard Assistant")
st.caption("Ask me anything about credit scorecards, WoE, IV, PSI, and risk modeling")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


def stream_response(prompt: str):
    async def agen():
        async with agent.run_stream(user_prompt=prompt) as result:
            last_len = 0
            full_text = ""
            async for chunk in result.stream_output(debounce_by=0.01):
                new_text = chunk[last_len:]
                last_len = len(chunk)
                full_text = chunk
                if new_text:
                    yield new_text
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


if prompt := st.chat_input("Ask your question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response_text = st.write_stream(stream_response(prompt))
    
    final_text = getattr(st.session_state, "_last_response", response_text)
    st.session_state.messages.append({"role": "assistant", "content": final_text})
