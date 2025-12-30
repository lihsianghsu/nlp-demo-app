import streamlit as st

def fade_block():
    """Use before a section that should animate in"""
    st.markdown(
        '<div style="animation: ls-fade-in var(--ls-medium) var(--ls-ease);">',
        unsafe_allow_html=True
    )

def end():
    st.markdown("</div>", unsafe_allow_html=True)
