import streamlit as st
from ls_ui.cards import card

st.title("🔐 Privacy & Data Handling")

with card("Summary", muted=True):
    st.markdown(
        """
        This application is designed to demonstrate NLP capabilities
        while **minimizing data collection by default**.
        """
    )

with card("What we do NOT collect"):
    st.markdown(
        """
        - No user accounts  
        - No cookies  
        - No IP addresses  
        - No browser fingerprinting  
        - No persistent identifiers  
        - No storage of user-submitted text  
        """
    )

with card("What we do collect (aggregated only)"):
    st.markdown(
        """
        To maintain service quality, we collect **anonymous, aggregated telemetry**:
        
        - Feature usage counts (e.g. sentiment analysis run)
        - Error counts
        - Average execution time
        
        This data:
        - Contains **no personal information**
        - Is **not linked to users or sessions**
        - Is **not shared with third parties**
        - Is **not persisted across deployments**
        """
    )

with card("Contact form data"):
    st.markdown(
        """
        - Contact form submissions are **not stored** in this application
        - Messages are processed **in memory only**
        - Do not submit sensitive or personal data
        """
    )

with card("Disclaimer", muted=True):
    st.caption(
        "This application is a demonstration system and should not be used "
        "for production decision-making."
    )
