# utils.py
# Utility functions for Streamlit NLP app demos.
# Provides text area with controls, deduplication results rendering.
import streamlit as st
import time

# Generate unique keys for Streamlit widgets
def make_key(tab: int, widget: str, purpose: str) -> str:
    """
    Generate a consistent Streamlit widget key.
    Example: make_key(2, "btn", "default") -> "tab2_btn_default"
    """
    return f"tab{tab}_{widget}_{purpose}"

# Text area
def text_area_with_controls(
    tab: int,
    state_key: str,
    label: str = "Input Text",
    height: int = 200,
    default_text: str = None,
    show_default: bool = True,
    samples: dict = None,
    show_samples: bool = True,
    show_reset: bool = True,
):
    """
    Text area with optional Default, Reset, and Sample controls.
    Default/Reset buttons are placed side by side below the selectbox.
    Parameters:
    - tab: tab index for unique button keys
    - state_key: session_state key to bind the text area
    - default_text: text to paste when clicking 'Use Default Text'
    - samples: optional dict of {name: text} for multiple examples
    - label: label for the text area
    - height: height of the text area
    - show_default: if True, show 'Use Default Text' button
    - show_samples: if True and samples provided, show sample selector
    - show_reset: if True, show 'Reset Text Area' button

    """
    # Selectbox for samples
    choice = st.selectbox(
        "📚 Try an Example",
        options=list(samples.keys()),
        key=make_key(tab, "sel", f"{state_key}_samples")
    )

    # Side-by-side buttons below selectbox: Default and Reset
    cols = st.columns(2)
    with cols[0]:
        if show_default and default_text:
            if st.button("Use Default Text", key=make_key(tab, "btn", f"default_{state_key}")):
                st.session_state[state_key] = default_text
        elif show_samples and samples:
            if st.button("Load Example", key=make_key(tab, "btn", f"example_{state_key}")):
                st.session_state[state_key] = samples[choice]

    with cols[1]:
        if show_reset:
            if st.button("Reset Text Area", key=make_key(tab, "btn", f"reset_{state_key}")):
                st.session_state[state_key] = ""
    
    # Bound text area
    text_val = st.text_area(label, height=height, key=state_key)

    return text_val

# Bilingual sample controls
def bilingual_sample_controls(tab: int, samples: dict, src_key: str, tgt_key: str):
    choice = st.selectbox(
        "📚 Try an Example",
        options=list(samples.keys()),
        key=make_key(tab, "sel", "align_samples")
    )

    cols = st.columns(2)
    with cols[0]:
        if st.button("Load Example", key=make_key(tab, "btn", "load_align_sample")):
            st.session_state[src_key] = samples[choice]["src"]
            st.session_state[tgt_key] = samples[choice]["tgt"]

    with cols[1]:
        if st.button("Reset Text Areas", key=make_key(tab, "btn", "reset_align")):
            st.session_state[src_key] = ""
            st.session_state[tgt_key] = ""

# Deduplication results display
def render_deduplication_results(kept, removed):
    st.metric("Kept segments", len(kept))
    st.metric("Removed segments", len(removed))

    if kept:
        st.markdown("### ✅ Kept segments")
        for i, seg in enumerate(kept, start=1):
            st.write(f"{i}. {seg}")

    if removed:
        st.markdown("### 🗑️ Removed (duplicate / similar)")
        for seg, ref, score in removed:
            st.warning(f"Similarity {score:.2f}")
            st.write(f"Removed: {seg}")
            st.write(f"Matched with: {ref}")

# Jaccard similarity
def compute_jaccard_similarity(str1: str, str2: str) -> float:
    """
    Compute Jaccard similarity between two strings based on word sets.
    Jaccard similarity = (size of intersection) / (size of union)
    """
    set1 = set(str1.lower().split())
    set2 = set(str2.lower().split())
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    if not union:
        return 0.0
    return len(intersection) / len(union)

# Guardrail for actions
def guarded_action(key: str, cooldown: int, max_chars: int, text: str):
    now = time.time()
    last = st.session_state.get(key, 0) # last action timestamp
    if now - last < cooldown:
        st.warning(f"Please wait {int(cooldown - (now - last))} seconds before submitting again.")
        return False
    if len(text) > max_chars:
        st.error(f"Input exceeds maximum length of {max_chars} characters.")
        return False
    st.session_state[key] = now
    return True

# Model loading notice
def model_loading_notice(label: str):
    st.info(
        f"🔄**{label}**: This model is loaded on first use. Subsequent runs are instant.",
        icon="⚡"
    )
# Tighten block container spacing
def tighten_bloc_container():
    st.markdown(
    """
    <style>
        header + section .block-container {
            padding-top: 2rem;
            padding-bottom: 5rem;
        }

        .block-container > div:first-child {
            margin-top: -0.5rem;
        }

        .gradient-divider {
            margin: 0.5rem 0 0.75rem 0;
        }
    </style>
    """,
    unsafe_allow_html=True
)