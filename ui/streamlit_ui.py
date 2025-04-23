# ui/streamlit_ui.py

import streamlit as st
import os, sys
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.ethics_bot import run_ethics_bot

st.set_page_config(page_title="Ethics Assistant", page_icon="⚖️")
st.title("⚖️ AI Ethics & Fairness Review Assistant")

# Chat log to keep track of history
if "review_log" not in st.session_state:
    st.session_state.review_log = []
if "last_query_time" not in st.session_state:
    st.session_state.last_query_time = 0

# Clear chat option
if st.button("🧹 Clear Chat"):
    st.session_state.review_log = []
    st.rerun()

# User input
with st.form("ethics_form"):
    project_desc = st.text_area("Enter your project description:", height=180, placeholder="e.g., We are building a predictive model to flag high-risk loan applicants...")
    submit = st.form_submit_button("Analyze")

# Throttle control (1 request per 5 seconds)
def can_submit():
    now = time.time()
    if now - st.session_state.last_query_time < 5:
        return False
    st.session_state.last_query_time = now
    return True

# On submit, call bot only if non-empty and allowed
if submit:
    if not can_submit():
        st.warning("⏳ Please wait 5 seconds between requests to avoid overloading the assistant.")
    elif project_desc.strip():
        st.session_state.review_log.append(("🧑‍💻 You", project_desc))
        with st.spinner("Analyzing ethical implications..."):
            reply = run_ethics_bot(project_desc)
        st.session_state.review_log.append(("🤖 Ethics Bot", reply))
    else:
        st.warning("⚠️ Please enter a project description before clicking Analyze.")

# Display interaction log with markdown
for speaker, message in st.session_state.review_log:
    with st.chat_message(speaker):
        st.markdown(message, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("Built by Sachin Bhandary · Streamlit + Modular Ethics Bot")
