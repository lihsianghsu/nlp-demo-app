# containers.py 
# Containers for page and section layouts
import streamlit as st

def page(title: str, subtitle: str | None = None):
    with st.container():
        st.markdown('<div class="page-container">', unsafe_allow_html=True)
        st.title(title)
        if subtitle:
            st.caption(subtitle)

def section(title: str):
    st.markdown(f"### {title}")

