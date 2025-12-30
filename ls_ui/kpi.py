# kpi.py
import streamlit as st
from ls_ui.cards import card

def kpi(title: str, value, delta=None, help=None):
    with card(title, muted=True):
        st.metric(title, value, delta=delta, help=help)
