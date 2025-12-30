# 1_Asset_Quality_Mgmt.py
import streamlit as st

st.title("📚 Asset & Quality Management")

# TM & Glossary Engine
st.header("Translation Memory & Glossary")
st.markdown("""
- **Centralized Engine**: Store and reuse translations
- **Consistency**: Automatic terminology enforcement
- **Efficiency**: Up to 40% cost reduction
""")

# Interactive Glossary Search
search_term = st.text_input("Search terminology", "API")
glossary_db = {
    "API": {"FR": "Interface de programmation", "ZH": "应用程序接口"},
    "Machine Learning": {"FR": "Apprentissage automatique", "ZH": "机器学习"},
}
if search_term:
    st.dataframe(glossary_db.get(search_term, {}), use_container_width=True)

# Human-in-the-Loop Annotation
st.header("🎯 Human-in-the-Loop Annotation")
st.markdown("**Upload data for expert annotation**")
uploaded_file = st.file_uploader("Choose a file (TXT/JSON)", type=['txt', 'json'])
if uploaded_file:
    st.success(f"File received: {uploaded_file.name}")
    st.button("Send for Expert Review", type="primary")