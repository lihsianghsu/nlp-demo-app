import streamlit as st
from i18n.strings import STRINGS

def t(key: str) -> str:
    lang = st.session_state.get("lang_code", "en")
    return STRINGS.get(lang, STRINGS["en"]).get(key, key)
