import streamlit as st
import time

def guarded_action(
    key: str,
    cooldown: int = 5,
    max_chars: int | None = None,
    text: str | None = None,
):
    """Rate-limit + input guard for public tools"""
    now = time.time()
    last = st.session_state.get(key, 0)

    if now - last < cooldown:
        st.warning("Please wait before running this action again.")
        st.stop()

    if max_chars and text and len(text) > max_chars:
        st.error("Input too long.")
        st.stop()

    st.session_state[key] = now
