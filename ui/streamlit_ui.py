"""
Streamlit UI for the AI Ethics & Fairness Review Assistant.
"""
import streamlit as st
import os
import sys
import time
from typing import List, Tuple, Optional
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.ethics_bot import run_ethics_bot
from app.config.logging_config import setup_logging

# Initialize logging
logger = setup_logging()

# Constants
THROTTLE_SECONDS = 5
MIN_INPUT_LENGTH = 10

def initialize_session_state() -> None:
    """Initialize Streamlit session state variables."""
    if "review_log" not in st.session_state:
        st.session_state.review_log: List[Tuple[str, str]] = []
    if "last_query_time" not in st.session_state:
        st.session_state.last_query_time: float = 0

def can_submit() -> bool:
    """
    Check if enough time has passed since the last submission.
    
    Returns:
        bool: True if submission is allowed, False otherwise
    """
    now = time.time()
    if now - st.session_state.last_query_time < THROTTLE_SECONDS:
        return False
    st.session_state.last_query_time = now
    return True

def clear_chat() -> None:
    """Clear the chat history."""
    st.session_state.review_log = []
    logger.info("Chat history cleared")

def main() -> None:
    """Main Streamlit application entry point."""
    st.set_page_config(page_title="Ethics Assistant", page_icon="⚖️")
    st.title("⚖️ AI Ethics & Fairness Review Assistant")
    
    initialize_session_state()
    
    # Clear chat option
    if st.button("🧹 Clear Chat"):
        clear_chat()
        st.rerun()
    
    # User input form
    with st.form("ethics_form"):
        project_desc = st.text_area(
            "Enter your project description:",
            height=180,
            placeholder="e.g., We are building a predictive model to flag high-risk loan applicants..."
        )
        submit = st.form_submit_button("Analyze")
    
    # Handle form submission
    if submit:
        if not can_submit():
            st.warning(f"⏳ Please wait {THROTTLE_SECONDS} seconds between requests to avoid overloading the assistant.")
            logger.warning("Request throttled")
        elif project_desc.strip():
            logger.info("Processing new project description")
            st.session_state.review_log.append(("🧑‍💻 You", project_desc))
            
            with st.spinner("Analyzing ethical implications..."):
                reply = run_ethics_bot(project_desc)
            
            st.session_state.review_log.append(("🤖 Ethics Bot", reply))
            logger.info("Analysis completed")
        else:
            st.warning("⚠️ Please enter a project description before clicking Analyze.")
            logger.warning("Empty project description submitted")
    
    # Display chat history
    for speaker, message in st.session_state.review_log:
        with st.chat_message(speaker):
            st.markdown(message, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.caption("Built by Sachin Bhandary · Streamlit + Modular Ethics Bot")

if __name__ == "__main__":
    main()
