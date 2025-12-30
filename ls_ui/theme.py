import streamlit as st
from importlib.resources import files

def apply_theme():
    css = files("ls_ui.assets").joinpath("brand.css").read_text(encoding="utf-8")

    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True
    )
    st.session_state["line_spacing"] = "Relaxed"

def load_css(css_file_path: str):
    """Apply custom CSS styling to the Streamlit app."""
    with open(css_file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def apply_theme_with_tabs():
    if "theme" not in st.session_state:
        st.session_state["theme"] = "Brand"  # Default theme

    # Tab system with icons + tooltips
    st.markdown('<div class="theme-tabs">', unsafe_allow_html=True)

    tabs = [
        ("☀️ Light", "Light", "Switch to Light Mode"),
        ("🌙 Dark", "Dark", "Switch to Dark Mode"),
        ("🎨 Brand", "Brand", "Apply Brand Theme"),
        ("⚡ Auto", "Auto", "Detect system preference automatically"),
    ]

    for label, theme_name, tooltip in tabs:
        active_class = "active" if st.session_state["theme"] == theme_name else ""
        if st.button(label, key=f"{theme_name}_tab"):
            st.session_state["theme"] = theme_name
        st.markdown(
            f"<div class='theme-tab {active_class}' title='{tooltip}'>{label}</div>",
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # Apply CSS + spacing based on theme
    if st.session_state["theme"] == "Light":
        load_css("ls_ui/assets/brand.css")
        st.session_state["line_spacing"] = "Normal"
        #st.sidebar.image("ls_ui/assets/logo_light.jpg", width=True)
    elif st.session_state["theme"] == "Dark":
        load_css("ls_ui/assets/custom_dark.css")
        st.session_state["line_spacing"] = "Relaxed"
        #st.sidebar.image("ls_ui/assets/logo_dark.png", width=True)
    elif st.session_state["theme"] == "Brand":
        load_css("ls_ui/assets/brand.css")
        st.session_state["line_spacing"] = "Relaxed"
        #st.sidebar.image("ls_ui/assets/logo_dark.png", width=True)
    else:  # Auto
        auto_css = """
        <style>
        @media (prefers-color-scheme: dark) {
            body { background-color: #121212; color: #e0e0e0; }
        }
        @media (prefers-color-scheme: light) {
            body { background-color: #ffffff; color: #333333; }
        }
        </style>
        """
        st.markdown(auto_css, unsafe_allow_html=True)
        st.session_state["line_spacing"] = "Normal"
        # st.sidebar.image("assets/logo_light.jpg", width=True)

