import time
import streamlit as st
import matplotlib.pyplot as plt
import jieba
import re
import pandas as pd
from collections import Counter
from transformers.pipelines import pipeline
from langdetect import detect
from wordcloud import WordCloud

from utils import make_key, text_area_with_controls, model_loading_notice
from ls_ui.grid import dashboard, full
from ls_ui.cards import card
from ls_ui.motion import fade_block, end

# -------------------------------------------------
# Resource loading (cloud-safe, cached)
# -------------------------------------------------

@st.cache_resource(show_spinner="Loading multilingual sentiment model…")
def load_sentiment_pipeline():
    return pipeline(
        "sentiment-analysis",
        #model="tabularisai/multilingual-sentiment-analysis" #returns Positive/Negative/Neutral; heavier
        model="nlptown/bert-base-multilingual-uncased-sentiment" #returns 1-5 star ratings; lightweight
        #model="cardiffnlp/twitter-xlm-roberta-base-sentiment" #Twitter-specific model; requires extra preprocessing; faster loading but less stable and slightly weaker Chinese support
    )


# -------------------------------------------------
# Utilities
# -------------------------------------------------

def rate_limit(key: str, seconds: int = 5):
    now = time.time()
    last = st.session_state.get(key, 0)
    if now - last < seconds:
        st.warning("Please wait before running this action again.")
        st.stop()
    st.session_state[key] = now


def detect_language(text: str) -> str:
    try:
        lang = detect(text.strip())
        return "zh" if lang.startswith("zh") else lang
    except Exception:
        return "unknown"

def analyze_sentiment(text: str):
    pipeline = load_sentiment_pipeline()  # lazy load
    result = pipeline(text)[0]
    return result["label"], result["score"]

def sentiment_badge(label: str) -> str:
    label = label.lower()
    if "positive" in label:
        return "🙂 **Positive**"
    if "negative" in label:
        return "🙁 **Negative**"
    if "neutral" in label:
        return "🤔 **Neutral**"
    return "❓ **Unknown**"

def normalize_sentiment(label: str):
    stars = int(label.split()[0])
    if stars <= 2:
        return "🙁 **Negative**"
    if stars == 3:
        return "🤔 **Neutral**"
    return "🙂 **Positive**"

# --- Word Cloud Generation ---
def generate_wordcloud(text: str, lang: str):
    if lang == "zh":
        text = " ".join(jieba.cut(text))

    wc = WordCloud(
        width=900,
        height=450,
        background_color="white",
        max_words=120,
        collocations=False
    ).generate(text)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    return fig

# --- Keyword Extraction ---
def extract_keywords(text, top_n=5):
    words = re.findall(r"\b\w+\b", text.lower())
    stopwords = {"the","and","is","in","of","to","a","was","as"}
    filtered = [w for w in words if w not in stopwords and len(w) > 2]
    counts = Counter(filtered)
    return counts.most_common(top_n)

# --- Simple NER helper ---
def simple_ner(text: str):
    entities = []

    # Proper nouns (capitalized words)
    for match in re.findall(r"\b[A-Z][a-z]+\b", text):
        entities.append((match, "Proper Noun"))

    # Numbers
    for match in re.findall(r"\b\d+\b", text):
        entities.append((match, "Number"))

    # Years (YYYY)
    for match in re.findall(r"\b\d{4}\b", text):
        entities.append((match, "Year"))

    return entities

def highlight_entities(text: str, entities):
    """Wrap detected entities with colored spans."""
    highlighted = text
    for ent, label in entities:
        color = {
            "Proper Noun": "#FFD700",  # gold
            "Number": "#87CEEB",       # light blue
            "Year": "#90EE90"          # light green
        }.get(label, "#FFB6C1")        # default pink

        highlighted = re.sub(
            fr"\b{ent}\b",
            f"<span style='background-color:{color}; padding:2px; border-radius:3px;'>{ent}</span>",
            highlighted
        )
    return highlighted

# -------------------------------------------------
# TAB CONTENTS
# -------------------------------------------------

st.title("🧠 NLP Content Intelligence")

tabs = st.tabs([
    "Sentiment Analysis",
    "Keyword Extraction",
    "Entity Recognition (NER)"
])

# =================================================
# TAB 1 — SENTIMENT + WORD CLOUD
# =================================================

with tabs[0]:    
    left, right = dashboard()
    with left:
        with card("😍😞 Sentiment Analysis Tool", refreshable=False):
            #default_text = "I love using Streamlit for building web apps. It's so easy and fun!"
            samples = {
                "Positive Review": "This product exceeded my expectations. Highly recommend to everyone!",
                "Negative Review": "I am very disappointed with the quality. It broke after one use.",
                "Neutral Review": "The item is okay, nothing special but does the job."
            }
            raw_text = text_area_with_controls(
                tab=0,
                state_key="sentiment_text",
                #default_text=default_text,
                samples=samples,
                show_default=False,    # hide default button
                show_samples=True,     # show sample selector
                show_reset=True
            )
        run = st.button("Sentiment Analysis", key=make_key(0, "btn", "sentiment"))
    # Results 
    with right:
        with card("Sentiment Analysis Demo", muted=True):
            if not st.session_state.get("sentiment_model_loaded"):
                model_loading_notice("Multilingual Sentiment Model")

            if run and raw_text.strip():
                rate_limit("sentiment_run", 5)

                lang = detect_language(raw_text)
                label, score = analyze_sentiment(raw_text)
                st.session_state["sentiment_model_loaded"] = True
                st.metric("Confidence Score", round(score, 3))
                # st.markdown(sentiment_badge(label)) # with tabularisai/multilingual-sentiment-analysis
                st.markdown(normalize_sentiment(label)) # with nlptown/bert-base-multilingual-uncased-sentiment
                st.caption(f"Detected language: `{lang}`")
            else:
                st.info("Run 'Sentiment Analysis' to see results.")
                with st.expander("ℹ️ About this tool"):
                    st.caption("This tool analyzes text sentiment using a lightweight multilingual AI model. Click *Analyze* to run sentiment detection and see see if it's positive 🙂 or negative 🙁.  A visual wordcloud display where frequently used words appear larger, helping you see which terms are driving the sentiment.")
                
    # Word Cloud
    if run and raw_text.strip():
        if st.checkbox("Show word cloud", value=True):
            fade_block()
            st.subheader("☁️ Word Cloud")
            fig = generate_wordcloud(raw_text, lang)
            st.pyplot(fig)
            end()

# =================================================
# TAB 2 — KEYWORD EXTRACTION
# =================================================

with tabs[1]:
    left, right = dashboard()
    with left:
        with card("🔑 Keyword Extraction", refreshable=False):
            # default_text = "Barack Obama was born in Hawaii. He served as President of the United States."
            samples = {
                "Tech News": "Apple released a new iPhone model in 2025 with advanced AI features.",
                "Sports": "Lionel Messi scored two goals in the Champions League final.",
                "History": "The French Revolution began in 1789 and changed the course of European history."
            }
            raw_text = text_area_with_controls(
                tab=1,
                state_key="kw_text",
                #default_text=default_text,
                samples=samples,
                show_default=False,  # hide default button
                show_samples=True,   # show sample selector
                show_reset=True
            )

        if st.button("Extract Keywords", key=make_key(1, "btn", "extract")):
            kws = extract_keywords(raw_text)
            if kws:
                st.success("✅ Extracted keywords")
                for word, freq in kws:
                    st.write(f"- **{word}** ({freq})")
            else:
                st.warning("No keywords found. Try another text!")
    with right:
        with card("Keyword Extraction Demo", muted=True):
            st.info("Run 'Keyword Extraction' to see results.")
            with st.expander("ℹ️ About this tool"):
                st.caption("This demo extracts keywords by counting word frequencies, excluding common stopwords. The top keywords are displayed with their occurrence counts. This tool finds the most frequent, meaningful words in text. Useful for summarizing content themes and indexing documents.")

# =================================================
# TAB 3 — ENTITY RECOGNITION (PLACEHOLDER)
# =================================================

with tabs[2]:
    left, right = dashboard()
    with left:
        with card("🔎 Entity Recognition (NER)", refreshable=False):
            # default_text = "Barack Obama was born in 1961 and served as President of the United States."
            samples = {
                "Tech News": "Apple released a new iPhone model in 2025 with advanced AI features.",
                "Sports": "Lionel Messi scored two goals in the Champions League final.",
                "History": "The French Revolution began in 1789 and changed the course of European history."
            }
            raw_text = text_area_with_controls(
                tab=2,
                state_key="ner_text",
                #default_text=default_text,
                samples=samples,
                show_default=False,  # hide default button
                show_samples=True,   # show sample selector
                show_reset=True
            )

        if st.button("Recognize Entities", key=make_key(2, "btn", "recognize")):
            entities = simple_ner(raw_text)
            if entities:
                st.success(f"✅ Found {len(entities)} entities")

                # Legend
                st.markdown("""
                **Legend:**
                - <span style='background-color:#FFD700; padding:2px; border-radius:3px;'>Gold</span> → Proper Noun  
                - <span style='background-color:#87CEEB; padding:2px; border-radius:3px;'>Blue</span> → Number  
                - <span style='background-color:#90EE90; padding:2px; border-radius:3px;'>Green</span> → Year  
                """, unsafe_allow_html=True)

                # Highlighted text
                highlighted = highlight_entities(raw_text, entities)
                st.markdown("### Highlighted Text")
                st.markdown(highlighted, unsafe_allow_html=True)

                # Table view
                st.markdown("### Entity Table")
                df = pd.DataFrame(entities, columns=["Entity", "Type"])
                st.table(df)

                # Download option
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="📥 Download Entities as CSV",
                    data=csv,
                    file_name="entities.csv",
                    mime="text/csv"
                )
            else:
                st.warning("No entities found. Try another text!")

    with right:
        with card("Entity Recognition Demo", muted=True):
            st.info("Run 'Recognize Entities' to see results.")
            with st.expander("ℹ️ About this tool"):
                st.caption("""
                    This demo performs simple Named Entity Recognition (NER) using regex patterns to identify basic entity types like Proper Nouns, Numbers, and Years.
                    The tool uses regular expressions (regex) to detect patterns:
                    - Proper Nouns: Finds capitalized words (e.g., "London", "Alice")
                    - Numbers: Identifies standalone digits (e.g., "42", "1000")
                    - Years: Recognizes 4-digit year formats (e.g., "2025", "1998")
            
                    How to Use:
                    Simply enter any text into the input field and click "Recognize Entities." The tool will highlight all found entities with their categories, showing you what information can be automatically extracted from unstructured text.

                    Note: Entities are shown in **two ways**:
                    - Highlighted directly in the text (with a color legend)
                    - Listed in a structured table

                    You can also **download the entity table as CSV** to use in dataset creation.
                    The NER here is a simple demo using regex patterns for basic entity types.
                    For production use, consider advanced NER models that handle more complex cases and context.
                    """)