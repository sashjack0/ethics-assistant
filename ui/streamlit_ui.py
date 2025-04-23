# ui/streamlit_ui.py

import streamlit as st
from app.ethics_bot import run_ethics_bot

st.set_page_config(page_title="Ethics Assistant", page_icon="⚖️")
st.title("⚖️ AI Ethics & Fairness Review Assistant")

# Chat log to keep track of history
if "review_log" not in st.session_state:
    st.session_state.review_log = []

# User input
with st.form("ethics_form"):
    project_desc = st.text_area("Enter your project description:", height=180, placeholder="e.g., We are building a predictive model to flag high-risk loan applicants...")
    submit = st.form_submit_button("Analyze")

# On submit, call bot
if submit and project_desc:
    st.session_state.review_log.append(("🧑‍💻 You", project_desc))
    reply = run_ethics_bot(project_desc)
    st.session_state.review_log.append(("🤖 Ethics Bot", reply))

# Display interaction log
for speaker, message in st.session_state.review_log:
    with st.chat_message(speaker):
        st.markdown(message)

# Footer
st.markdown("---")
st.caption("Built by Sachin Bhandary · Streamlit + Modular Ethics Bot")
