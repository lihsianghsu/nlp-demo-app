import streamlit as st
from contextlib import contextmanager
import uuid

@contextmanager
def card(
    title: str | None = None,
    muted: bool = False,
    collapsible: bool = False,
    refreshable: bool = False,
):
    card_id = str(uuid.uuid4())
    open_key = f"ls_card_open_{card_id}"

    if open_key not in st.session_state:
        st.session_state[open_key] = True

    classes = "ls-card ls-card-muted" if muted else "ls-card"

    st.markdown(f'<div class="{classes}">', unsafe_allow_html=True)
    st.markdown('<div class="ls-card-header">', unsafe_allow_html=True)

    st.markdown(
        f'<div class="ls-card-title">{title or ""}</div>',
        unsafe_allow_html=True
    )

    actions = []
    if collapsible:
        actions.append("▾" if st.session_state[open_key] else "▸")
    if refreshable:
        actions.append("⟳")

    if actions:
        st.markdown('<div class="ls-card-actions">', unsafe_allow_html=True)
        for a in actions:
            if st.button(a, key=f"{card_id}_{a}", help="Card action"):
                if a in ["▾", "▸"]:
                    st.session_state[open_key] = not st.session_state[open_key]
                if a == "⟳":
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    if not collapsible or st.session_state[open_key]:
        try:
            yield
        finally:
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("</div>", unsafe_allow_html=True)
