# 2_Data_Engineering.py
import string
import streamlit as st
import pandas as pd
import re
import json

from utils import make_key, text_area_with_controls, bilingual_sample_controls, render_deduplication_results
from ls_ui.grid import dashboard, full
from ls_ui.cards import card
from ls_ui.motion import fade_block, end


# -------------------------------------------------
# Helper Functions
# -------------------------------------------------

# --- Align helper function ---
def simple_align(src_text: str, tgt_text: str):
    """Align sentences by index from source and target texts, with mismatch check."""
    delimiters = [".", "。", "！", "？"]
    def split_sentences(text):
        for d in delimiters:
            text = text.replace(d, ".")  # normalize to "."
        return [s.strip() for s in text.split(".") if s.strip()]

    src_sentences = split_sentences(src_text)
    tgt_sentences = split_sentences(tgt_text)

    # Check mismatch
    if len(src_sentences) != len(tgt_sentences):
        return None, src_sentences, tgt_sentences

    # Align by index
    pairs = [(src, tgt) for src, tgt in zip(src_sentences, tgt_sentences)]
    return pairs, src_sentences, tgt_sentences

def render_alignment_results(pairs):
    for i, (src, tgt) in enumerate(pairs, start=1):
        cols = st.columns([0.06, 0.47, 0.47])
        cols[0].markdown(f"**{i}.**")
        cols[1].write(src)
        cols[2].write(tgt)

# --- Sample data for alignment ---
ALIGN_SAMPLES = {
    "FR → EN (Greeting)": {
        "src": "Bonjour. Comment ça va?",
        "tgt": "Hello. How are you?"
    },
    "ZH → EN (Product)": {
        "src": "这是一个测试。我们正在对齐句子。",
        "tgt": "This is a test. We are aligning sentences."
    },
    "FR → EN (Business)": {
        "src": "Le contrat a été signé hier. La livraison est prévue demain.",
        "tgt": "The contract was signed yesterday. Delivery is scheduled for tomorrow."
    }
}

# --- TMX Builder ---
def build_tmx_lite(pairs, src_lang="src", tgt_lang="tgt"):
    tus = []
    for i, (src, tgt) in enumerate(pairs, start=1):
        tus.append(
            f"""
            <tu tuid="{i}">
              <tuv xml:lang="{src_lang}"><seg>{src}</seg></tuv>
              <tuv xml:lang="{tgt_lang}"><seg>{tgt}</seg></tuv>
            </tu>
            """.strip()
        )

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<tmx version="1.4">
  <body>
    {"".join(tus)}
  </body>
</tmx>
"""

# --- JSONL Builder ---

def build_jsonl(pairs, src_lang="src", tgt_lang="tgt"):
    lines = []
    for src, tgt in pairs:
        lines.append(json.dumps({
            "source": src,
            "target": tgt,
            "src_lang": src_lang,
            "tgt_lang": tgt_lang
        }, ensure_ascii=False))
    return "\n".join(lines)

# --- Cleaning helpers ---
def clean_tags(text: str) -> str:
    """Remove HTML/XML tags but keep inner content."""
    return re.sub(r"</?[^>]+>", "", text)   # removes <tag> and </tag>, keeps content

def to_lower(text: str) -> str:
    return text.lower()

def strip_punct(text: str) -> str:
    return text.translate(str.maketrans("", "", string.punctuation))

def render_cleaning_steps(steps):
    """
    steps: list of (step_name, before, after)
    """
    for i, (name, before, after) in enumerate(steps, start=1):
        st.markdown(f"**{i}. {name}**")
        cols = st.columns(2)
        cols[0].text_area("Before", before, height=120, disabled=True)
        cols[1].text_area("After", after, height=120, disabled=True)

# --- Deduplication helpers ---
def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s]", "", text)
    return text.strip()


def token_overlap(a: str, b: str) -> float:
    a_tokens = set(a.split())
    b_tokens = set(b.split())
    if not a_tokens or not b_tokens:
        return 0.0
    return len(a_tokens & b_tokens) / len(a_tokens | b_tokens)


def deduplicate_segments(segments, similarity_threshold=0.8):
    kept = []
    removed = []

    for seg in segments:
        norm = normalize_text(seg)
        is_duplicate = False

        for kept_seg in kept:
            kept_norm = normalize_text(kept_seg)

            # Exact match
            if norm == kept_norm:
                removed.append((seg, kept_seg, 1.0))
                is_duplicate = True
                break

            # Similarity match
            sim = token_overlap(norm, kept_norm)
            if sim >= similarity_threshold:
                removed.append((seg, kept_seg, sim))
                is_duplicate = True
                break

        if not is_duplicate:
            kept.append(seg)

    return kept, removed


# -------------------------------------------------
# UI Layout
# -------------------------------------------------

st.title("🔧 Data Engineering for AI")

tabs = st.tabs([
    "Parallel Text Alignment",
    "NLP Dataset Cleaning",
    "Dataset Deduplication"
])

# =================================================
# TAB 1 — PARALLEL TEXT ALIGNMENT
# =================================================
with tabs[0]:
    left, right = dashboard()

    with left:
        with card("↔️ Parallel Text Alignment", refreshable=False):

            bilingual_sample_controls(
                tab=0,
                samples=ALIGN_SAMPLES,
                src_key="align_src",
                tgt_key="align_tgt"
            )

            src_text = st.text_area(
                "Source Text",
                height=180,
                key="align_src"
            )

            tgt_text = st.text_area(
                "Target Text",
                height=180,
                key="align_tgt"
            )

        if st.button("Align Sentences", key=make_key(0, "btn", "align")):
            aligned_pairs, src_sents, tgt_sents = simple_align(src_text, tgt_text)

            if aligned_pairs is None:
                st.error(
                    f"❌ Sentence count mismatch — "
                    f"Source: {len(src_sents)}, Target: {len(tgt_sents)}"
                )
                st.info(
                    "💡 Ensure both texts contain the same number of sentences "
                    "before alignment."
                )
            else:
                st.success(f"✅ Aligned {len(aligned_pairs)} sentence pairs")
                render_alignment_results(aligned_pairs)

                # ---- Export section (lightweight, optional)
                st.markdown("### 📦 Use these aligned pairs as")

                tmx_content = build_tmx_lite(aligned_pairs, src_lang="fr", tgt_lang="en")
                jsonl_content = build_jsonl(aligned_pairs, src_lang="fr", tgt_lang="en")

                cols = st.columns(2)

                with cols[0]:
                    st.download_button(
                        "📥 Translation Memory (TMX)",
                        tmx_content,
                        file_name="aligned.tmx",
                        mime="application/xml"
                    )
                with cols[1]:
                    st.download_button(
                        "📥 Training Data (JSONL)",
                        jsonl_content,
                        file_name="aligned.jsonl",
                        mime="application/json"
                    )   
    with right:
        with card("Parallel Text Alignment", muted=True):
            st.info("Run 'Align Sentences' to see results.")
            with st.expander("ℹ️ About this tool"):
                st.caption(
                    """                    
                    This demo shows how raw content can be transformed into structured parallel data, a foundational step in data engineering for AI and localization workflows.
                    It also shows how bilingual text can be aligned at sentence level and reused across workflows:

                        • As a Translation Memory (TMX) for localization tools
                        • As structured data for training or evaluating NLP models

                    The focus here is on illustration, not production-scale processing.

                    """
                )

# =================================================
# TAB 2 — DATASET CLEANING & NORMALIZATION
# =================================================
with tabs[1]:
    left, right = dashboard()

    with left:
        with card("🧹 Dataset Cleaning & Normalization", refreshable=False):

            default_text = "<p>Hello <b>World</b>! This is <i>sample</i> text.</p>"

            if "clean_raw_text" not in st.session_state:
                st.session_state.clean_raw_text = ""

            cols = st.columns(2)
            with cols[0]:
                if st.button("Use Default Text", key=make_key(1, "btn", "default_clean")):
                    st.session_state.clean_raw_text = default_text
            with cols[1]:
                if st.button("Reset Text", key=make_key(1, "btn", "reset_clean")):
                    st.session_state.clean_raw_text = ""

            raw_text = st.text_area(
                "Raw Text",
                height=200,
                key="clean_raw_text"
            )

            st.markdown("**Cleaning Options**")
            apply_tags = st.checkbox("Remove HTML / XML tags", value=True)
            apply_lower = st.checkbox("Convert to lowercase", value=True)
            apply_punct = st.checkbox("Strip punctuation", value=False)

        if st.button("Run Cleaning", key=make_key(1, "btn", "run_clean")):
            steps = []
            current = raw_text

            if apply_tags:
                cleaned = clean_tags(current)
                steps.append(("Remove tags", current, cleaned))
                current = cleaned

            if apply_lower:
                cleaned = to_lower(current)
                steps.append(("Lowercase", current, cleaned))
                current = cleaned

            if apply_punct:
                cleaned = strip_punct(current)
                steps.append(("Strip punctuation", current, cleaned))
                current = cleaned

            if steps:
                st.success("✅ Cleaning pipeline applied")
                render_cleaning_steps(steps)
            else:
                st.warning("No cleaning options selected.")

    with right:
        with card("Dataset Cleaning & Normalization", muted=True):
            st.info("Run 'Run Cleaning' to see step-by-step transformations.")
            with st.expander("ℹ️ About this tool"):
                st.caption(
                    """
                    This demo illustrates a lightweight text preparation pipeline.
                    Each transformation is applied step by step and rendered explicitly,
                    showing how raw content is normalized before being used in NLP workflows
                    such as training, indexing, or quality checks.
                    """
                )


# =================================================
# TAB 3 — DATASET DEDUPLICATION
# =================================================
with tabs[2]:
    left, right = dashboard()

    with left:
        with card("🧪 Dataset Deduplication & Similarity Filtering", refreshable=False):

            default_text = """
                Hello world
                Hello world!
                This is a sample sentence
                This is a sample sentence with extra words
                Another sentence
                completely different line
                Another sentence."""

            if "dedup_text" not in st.session_state:
                st.session_state.dedup_text = ""

            cols = st.columns(2)
            with cols[0]:
                if st.button("Use Sample Text", key=make_key(2, "btn", "default_dedup")):
                    st.session_state.dedup_text = default_text
            with cols[1]:
                if st.button("Reset Text", key=make_key(2, "btn", "reset_dedup")):
                    st.session_state.dedup_text = ""

            raw_text = st.text_area(
                "One segment per line",
                height=220,
                key="dedup_text"
            )

            similarity_threshold = st.slider(
                "Similarity threshold",
                min_value=0.5,
                max_value=1.0,
                value=0.8,
                step=0.05
            )

        if st.button("Run Deduplication", key=make_key(2, "btn", "run_dedup")):
            segments = [s.strip() for s in raw_text.splitlines() if s.strip()]

            if len(segments) < 2:
                st.warning("Please provide at least two segments.")
            else:
                kept, removed = deduplicate_segments(
                    segments,
                    similarity_threshold=similarity_threshold
                )

                st.success("✅ Deduplication completed")
                render_deduplication_results(kept, removed)

    with right:
        with card("Dataset Deduplication", muted=True):
            st.info("Run 'Recognize Entities' to see results.")
            with st.expander("ℹ️ About this tool"):
                st.caption(
                    """
                    This demo illustrates how redundant or highly similar text segments
                    can be identified and filtered before being used for NLP or AI tasks.
                    Deduplication helps reduce dataset size, training cost, and bias
                    while improving overall data quality.
                    """
                )


# -------------------------------------------------
# END OF PAGE