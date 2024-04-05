import streamlit as st
from app import process_url

from constants import *
from manager import get_response
from upload import ingest_pdf


with st.sidebar:
    st.subheader("🖥️💬 Tutor Agent")
    st.success("App is ready", icon="✅")
    with st.expander("Query URL/Docs", expanded=False):
        uploaded_files = st.file_uploader(
            "Choose a docx file", accept_multiple_files=True, type="docx"
        )
        if uploaded_files:
            ingest_pdf(uploaded_files)
        fromDoc = st.toggle("Answer from Doc only", value=False)
        url = st.text_input("The URL link")
        if url:
            process_url(url)
        fromURL = st.toggle("Answer from URL only", value=False)
    subject = st.selectbox(
        "Choose any of the subjects below?",
        (
            DL,
            ME,
            PR,
            VC,
        ),
    )

    st.write("You selected:", subject)
    # st.subheader("Choose one of the following mode")
    mode = st.radio(
        "Choose one of the following mode",
        [learn, practice, chat],
        index=None,
    )
    st.write("You selected:", mode)

filters = {
    "fromURL": fromURL,
    "fromDoc": fromDoc,
    "mode": mode,
    "subject": subject,
}

# title
st.title("💬 AI Tutor Agent")

if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "How can I help you?"}
    ]

# Display chat messages from history on app rerun
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Accept user input
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)


def generate_response(response):
    placeholder = st.empty()
    full_response = ""
    for item in response:
        full_response += item
        placeholder.markdown(full_response)
    placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)


# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_response(filters, prompt)
            placeholder = st.empty()
            full_response = ""
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)
