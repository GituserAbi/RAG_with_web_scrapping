from main import *
import streamlit as st
import time
from streamlit_extras.stylable_container import stylable_container

# Function to simulate streaming response
def generator(response):
    words = response.split(" ")
    for word in words:
        yield word + " "
        time.sleep(0.02)

# Initialize session state if not already set
if "messages" not in st.session_state:
    st.session_state.messages = []
if "human_review" not in st.session_state:
    st.session_state.human_review = False
if "pending_response" not in st.session_state:
    st.session_state.pending_response = ""
if "edited_response" not in st.session_state:
    st.session_state.edited_response = ""
if "enable_edit" not in st.session_state:
    st.session_state.enable_edit = False

st.title("Assistant")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # AI generates response
    with st.chat_message("assistant"):
        response = generateResponse(prompt)
        st.session_state.pending_response = response
        st.write_stream(generator(response))
    
    # Activate human review toggle
    st.session_state.human_review = True

# Human-in-the-loop validation
if st.session_state.human_review:
    st.subheader("Human Validation Needed")
    st.markdown("**Generated Response:**")
    st.info(st.session_state.pending_response)
    
    # Feedback buttons next to each other below the generated response
    with stylable_container("feedback-container", css_styles="display: flex; gap: 5px; align-items: center;"):
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("👍", key="thumbs_up"):
                st.session_state.enable_edit = False
                st.session_state.messages.append({"role": "assistant", "content": st.session_state.pending_response})
                st.session_state.human_review = False
        with col2:
            if st.button("👎", key="thumbs_down"):
                st.session_state.enable_edit = True
    
    # Editable text area for human modification (only enabled if thumbs down is clicked)
    if st.session_state.enable_edit:
        edited_response = st.text_area("Modify AI Response:", value=st.session_state.pending_response, key="edited_response_input")
        if st.button("Approve Response"):
            st.session_state.messages.append({"role": "assistant", "content": st.session_state.pending_response})
            st.session_state.messages.append({"role": "assistant", "content": edited_response})
            st.session_state.human_review = False
            st.session_state.pending_response = ""
            st.session_state.enable_edit = False
