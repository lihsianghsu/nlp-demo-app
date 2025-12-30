# Contact.py
import streamlit as st
from ls_ui.cards import card
from ls_ui.grid import two_col
from ls_ui.env import PUBLIC_MODE
from ls_ui.tooling import guarded_action
from ls_ui.telemetry import record_event, record_error

st.title("📬 Contact Lingua Synapse")

st.caption(
    "For inquiries about NLP solutions, integrations, or partnerships. "
    "This form is for professional contact only."
)
# -------------------------
# Privacy notice
# -------------------------
with card("🔏 Privacy notice", muted=True):
    with st.expander("Click to view privacy details"):
        st.markdown(
            """
            - Messages are **not stored** in this application
            - Inputs are processed **in memory only**
            - No tracking or profiling is performed
            - Do not submit sensitive or personal data
            """
        )

# -------------------------
# Contact form
# -------------------------
with card("Contact form"):
    with st.form("contact_form", clear_on_submit=True):
        col1, col2 = two_col()

        with col1:
            name = st.text_input("Name (optional)", max_chars=80)
            email = st.text_input("Email *", max_chars=120)

        with col2:
            company = st.text_input("Company / Organization (optional)", max_chars=120)
            topic = st.selectbox(
                "Topic",
                [
                    "General inquiry",
                    "NLP integration",
                    "Localization / linguistic services",
                    "Demo or pilot project",
                    "Other",
                ],
            )

        message = st.text_area(
            "Message *",
            height=160,
            max_chars=1000,
            placeholder="Describe your use case or question.",
        )

        submitted = st.form_submit_button("Send message")

    if submitted:
        # -------------------------
        # Guardrails
        # -------------------------
        guarded_action(
            key="contact_submit",
            cooldown=20,
            max_chars=1_000,
            text=message,
        )

        if not email or "@" not in email:
            st.error("Please provide a valid email address.")
            st.stop()

        if not message.strip():
            st.error("Message cannot be empty.")
            st.stop()

        # -------------------------
        # Telemetry (no content logged)
        # -------------------------
        try:
            record_event("contact_form_submit")
            # Placeholder for future integration:
            # send_email(...)
            st.success(
                "Thank you for your message. "
                "We will respond if follow-up is appropriate."
            )
        except Exception:
            record_error("contact_form_error")
            st.error("Unable to submit the form at this time.")

# -------------------------
# Public mode notice
if PUBLIC_MODE:
    st.info(
        "You are using the public demo of Lingua Synapse. "
        "For enterprise solutions, please contact us via the form above."
    )

