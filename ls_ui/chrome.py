import streamlit as st
from importlib.resources import files
from pathlib import Path
import base64
from i18n.translator import t

def render_svg(svg_code):
    b64 = base64.b64encode(svg_code.encode('utf-8')).decode()
    html = f'<img src="data:image/svg+xml;base64,{b64}" style="width:120px;height:120px;"/>'
    st.markdown(html, unsafe_allow_html=True)

# SVG code as string for the logo
svg_code = '''<svg width="120" height="120" viewBox="0 0 120 120"
     xmlns="http://www.w3.org/2000/svg" role="img">
  <title>Lingua Synapse</title>
  <defs>
    <pattern id="logoPattern" x="6" y="6" width="108" height="108" patternUnits="userSpaceOnUse">
      <rect x="0" y="0" width="108" height="108" fill="#000000"/>
      <image href="logo_dark.png" x="0" y="0" width="108" height="108" preserveAspectRatio="xMidYMid meet"/>
    </pattern>
  </defs>
  <circle cx="60" cy="60" r="54" fill="url(#logoPattern)" stroke="#0073aa" stroke-width="2"/>
</svg>'''



def render_header():
    # ------------------------------------------------------------------
    # Scoped CSS (header-only)
    # ------------------------------------------------------------------
    st.markdown(
        """
        <style>
            .ls-header {
                display: flex;
                flex-direction: column;
                justify-content: flex-end;
                align-items: flex-end;
                text-align: flex-end;
                width: 100%;
                padding-bottom: 0.25rem;
            }

            .ls-header h2 {
                margin: 0;
                line-height: 1.15;
            }

            .ls-header p {
                margin: 0;
                line-height: 1.2;
                opacity: 0.7;
            }

            /* Language selector layout */
            .ls-lang-row {
                display: flex;
                font-size: 1.5rem;
                align-items: flex-end;
                justify-content: flex-end;
                gap: 0.01rem;
                margin: 0;
                padding-top: 0.25rem;
                height: 100%;
            }

            .ls-lang {
                display: flex;
                align-items: flex-start;
                justify-content: flex-start;

                height: 100%;
            }

            .ls-lang-label {
                font-size: 0.85rem;
                opacity: 0.8;
            }            
    
            .ls-lang span {
                font-size: 1.5rem;
                line-height: 1;
                margin: 0;
                padding-top: 1rem;
            }

            .gradient-divider {
                height: 2px;
                border: none;
                background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%);
                border-radius: 2px;
                margin: 0.25rem 0 0.75rem 0;
            }

            /* Visually hide label on desktop, keep it accessible */
            .ls-sr-only {
                position: absolute;
                width: 1px;
                height: 1px;
                padding: 0;
                margin: -1px;
                overflow: hidden;
                clip: rect(0, 0, 0, 0);
                white-space: nowrap;
                border: 0;
            }

            .gradient-divider {
                height: 2px;
                border: none;
                background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%);
                border-radius: 2px;
                margin: 0.25rem 0 0.75rem 0;
            }

            /* ------------------ Mobile layout ------------------ */
            @media (max-width: 768px) {
                .ls-lang-row {
                    justify-content: flex-start;
                    margin-top: 0.5rem;
                }

                .ls-header h2 {
                    font-size: 1.4rem;
                }

                .ls-header p {
                    font-size: 0.9rem;
                }

                /* Reveal label on mobile */
                .ls-sr-only {
                    position: static;
                    width: auto;
                    height: auto;
                    margin: 0;
                    overflow: visible;
                    clip: auto;
                    white-space: normal;
                }
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    # ------------------------------------------------------------------
    # State
    # ------------------------------------------------------------------
    if "lang_code" not in st.session_state:
        st.session_state.lang_code = "en"

    LANGUAGES = {"en": "🇬🇧", "fr": "🇫🇷", "zhs": "🇨🇳", "zht": "🇹🇼"}

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------
    left, right = st.columns([2, 4], vertical_alignment="center")

    with left:
        st.session_state.lang_code = st.selectbox(
            "",
            options=list(LANGUAGES.keys()),
            format_func=lambda x: LANGUAGES[x],
            index=list(LANGUAGES.keys()).index(st.session_state.lang_code),
            key="language_selector",
            label_visibility="collapsed",
            help="Select interface language",
            width=100,
        )
    with right:
        #st.markdown("")
        #st.markdown("")
        st.markdown(
            f"""
            <div class="ls-header">
                <h2>{t("app_title")}</h2>
                <p>{t("app_tagline")}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ------------------------------------------------------------------
    # Divider
    # ------------------------------------------------------------------
    st.markdown('<hr class="gradient-divider"/>', unsafe_allow_html=True)

def render_footer():
    st.markdown("")
    st.markdown("")
    st.markdown(
        """
        <style>
        .footer {
            text-align: center;
            margin-top: 2rem;
            font-size: 0.9rem;
            color: #666;
        }
        .footer-icons {
            margin-top: 0.5rem;
            margin-bottom: 12px
        }
        .footer-icons a {
            display: inline-block;
            margin: 0 8px;
            opacity: 0.7;
            transition: opacity 0.3s ease, transform 0.2s ease;
        }
        .footer-icons a:hover {
            opacity: 1;
            transform: scale(1.1);
        }
        .footer-icons svg {
            width: 20px;
            height: 20px;
        }
        </style>

        <footer class="footer">
            <div class="footer-icons">
                <a href="https://github.com/yourusername" target="_blank" rel="noopener noreferrer">
                    <!-- GitHub SVG -->
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.025 0 2.051.138 3.006.419 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.236 1.911 1.236 3.221 0 4.606-2.807 5.629-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.796 24 17.3 24 12c0-6.627-5.373-12-12-12z"/>
                    </svg>
                </a>
                <a href="https://linkedin.com/in/yourprofile" target="_blank" rel="noopener noreferrer">
                    <!-- LinkedIn SVG -->
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
                    </svg>
                </a>
                <a href="https://linguasynapse.wordpress.com/" target="_blank" rel="noopener noreferrer">
                    <!-- WordPress SVG -->
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M21.469 6.825c.84 1.537 1.318 3.3 1.318 5.175 0 3.979-2.156 7.456-5.363 9.325l3.295-9.527c.615-1.54.82-2.771.82-3.864 0-.405-.026-.78-.07-1.11m-7.981.105c.647-.03 1.232-.105 1.232-.105.582-.075.514-.93-.067-.899 0 0-1.755.135-2.88.135-1.064 0-2.85-.15-2.85-.15-.585-.03-.661.855-.075.885 0 0 .54.061 1.125.09l1.68 4.605-2.37 7.08L5.354 6.9c.649-.03 1.234-.1 1.234-.1.585-.075.516-.93-.065-.896 0 0-1.746.138-2.874.138-.2 0-.438-.008-.69-.015C4.911 3.15 8.235 1.215 12 1.215c2.809 0 5.365 1.072 7.286 2.833-.046-.003-.091-.009-.141-.009-1.06 0-1.812.923-1.812 1.914 0 .89.513 1.643 1.06 2.531.411.72.89 1.643.89 2.977 0 .915-.354 1.994-.821 3.479l-1.075 3.585-3.9-11.61.001.014zM12 22.784c-1.059 0-2.081-.153-3.048-.437l3.237-9.406 3.315 9.087c.024.053.05.101.078.149-1.12.393-2.325.609-3.582.609M1.211 12c0-1.564.336-3.05.935-4.39L7.29 21.709C3.694 19.96 1.212 16.271 1.211 12M12 0C5.385 0 0 5.385 0 12s5.385 12 12 12 12-5.385 12-12S18.615 0 12 0"/>
                    </svg>
                </a>
                <a href="https://www.malt.fr/profile/lihsianghsu" target="_blank" rel="noopener noreferrer">
                    <!-- Malt SVG -->
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M20.195 8.581c-.069 0-.285.026-.484.113-.432.181-.597.311-.597.58v5.023c0 .277.26.355.735.355.467 0 .649-.087.649-.355V8.858c0-.173-.113-.277-.303-.277zm3.502 4.903c-.345.087-.45.113-.57.113-.147 0-.2-.044-.2-.2v-2.161h.788c.207 0 .285-.078.285-.285 0-.173-.078-.26-.285-.26h-.787v-.839c0-.259-.087-.363-.268-.363-.173 0-.415.156-.934.597-.528.45-.83.744-.83.951 0 .121.086.199.224.199h.424v2.335c0 .683.337 1.08.925 1.08.39 0 .675-.146 1.012-.406.311-.242.51-.432.51-.596 0-.139-.103-.217-.294-.165zm-15.21-3.078c-.13 0-.285.026-.484.112-.433.19-.597.312-.597.58v3.2c0 .276.26.354.735.354.467 0 .649-.087.649-.355v-3.614c0-.173-.113-.277-.303-.277Zm1.816 0c-.355 0-.675.121-.986.363-.173.138-.32.294-.32.424 0 .112.078.173.19.173.19 0 .251-.078.416-.078.164 0 .25.173.25.476v2.533c0 .277.26.355.735.355.467 0 .649-.087.649-.355v-2.776c0-.657-.39-1.115-.934-1.115zm2.43 0c-.337 0-.692.121-1.003.363-.173.138-.32.294-.32.424 0 .112.078.173.19.173.19 0 .25-.078.432-.078s.268.173.268.476v2.533c0 .277.26.355.735.355.467 0 .649-.087.649-.355v-2.776c0-.657-.39-1.115-.951-1.115zm5.335 0a1.29 1.29 0 0 0-.484.112c-.26.113-.398.2-.467.312-.26-.303-.597-.398-.977-.398-1.116 0-1.911.942-1.911 2.283 0 1.124.605 1.954 1.461 1.954.26 0 .493-.104.77-.363.216-.2.32-.329.32-.45a.14.14 0 0 0-.147-.147c-.121 0-.251.104-.416.104-.354 0-.596-.545-.596-1.35 0-.803.32-1.348.804-1.348.32 0 .562.242.562.657v2.525c0 .277.26.355.735.355.467 0 .649-.087.649-.355v-3.614c0-.173-.113-.277-.303-.277ZM3.499 13.563l-.21.21.619.618c.304.304.79.598 1.244.144.339-.34.26-.695.073-.98-.06.004-1.726.008-1.726.008zm-.963-2.325.21-.21-.608-.607c-.304-.303-.765-.621-1.243-.143-.351.35-.273.692-.087.97Zm2.86.416c-.037.043-1.511 1.524-1.511 1.524h1.154c.43 0 .981-.101.981-.777 0-.496-.296-.683-.624-.747zm-3.244-.031H.981c-.43 0-.981.135-.981.778 0 .479.307.676.641.745.04-.046 1.511-1.523 1.511-1.523zm1.484 3.04-.618-.618-.608.607a2.613 2.613 0 0 1-.137.128c.07.333.266.639.745.639s.676-.307.745-.641c-.043-.037-.085-.073-.127-.115zM2.41 10.15l.608.607.618-.618a2.25 2.25 0 0 1 .128-.118c-.065-.327-.251-.623-.747-.623s-.682.297-.746.625c.046.04.092.08.14.127zm2.742.117c-.455-.454-.94-.16-1.244.144l-2.87 2.87c-.303.303-.621.765-.143 1.243.478.478.94.16 1.243-.143l2.87-2.87c.304-.304.598-.79.144-1.244Z"/>
                    </svg>                                    
                </a>
                <a href="mailto:lihsianghsu@yahoo.fr" target="_blank" rel="noopener noreferrer">
                    <!-- Email SVG -->
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>
                    </svg>
                </a>
            </div>
            <div>© 2025 Lingua Synapse. All rights reserved.</div>
        </footer>
        """,
        unsafe_allow_html=True
    )
def render_footer_simple():
    st.markdown("")
    st.markdown("")
    st.markdown(
        """
        <footer>
            © 2025 Lingua Synapse · Internal Platform
        </footer>
        """,
        unsafe_allow_html=True,
        width = "stretch", 
        text_alignment = "center"
    )
