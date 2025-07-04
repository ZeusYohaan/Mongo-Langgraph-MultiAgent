import streamlit as st
import uuid
from agents.supervisor import supervisor
from config import redis_checkpoint

if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = f"session_{uuid.uuid4().hex[:8]}"
if "supervisor_agent" not in st.session_state:
    with redis_checkpoint as redis_checkpointer:
        redis_checkpointer.setup()
        st.session_state.supervisor_agent = supervisor.compile(checkpointer=redis_checkpointer)

st.title("🤖Agent Chat")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.supervisor_agent.invoke(
                    {"messages": [{"role": "user", "content": prompt}]},
                    config={"configurable": {"thread_id": st.session_state.thread_id}}
                )

                assistant_response = response['messages'][-1].content

                st.markdown(assistant_response)

                st.session_state.messages.append({"role": "assistant", "content": assistant_response})

            except Exception as e:
                error_message = f"Sorry, I encountered an error: {str(e)}"
                st.error(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})

with st.sidebar:
    st.header("Session Info")
    st.write(f"**Thread ID:** {st.session_state.thread_id}")
    st.write(f"**Messages:** {len(st.session_state.messages)}")

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.thread_id = f"session_{uuid.uuid4().hex[:8]}"
        st.rerun()
