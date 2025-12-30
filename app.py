from cProfile import label
import streamlit as st
from ls_ui.theme import apply_theme
from ls_ui.chrome import render_header, render_footer
from ls_ui.env import PUBLIC_MODE
from utils import tighten_bloc_container
from i18n.translator import t


st.set_page_config(
    page_title="AI-Powered Language Solutions",
    page_icon="assets/logo_dark.png",
    layout="wide",
    #initial_sidebar_state=None,
    menu_items={
        'Get Help': 'mailto:lihsianghsu@yahoo.fr',
        'Report a bug': "mailto:lihsianghsu@yahoo.fr",
        'About': "https://linguasynapse.wordpress.com/",
    }
)

# logo
st.logo("ls_ui/assets/logo_dark.png", icon_image="ls_ui/assets/icon_2.png", size="large")

# Apply theme and render header

tighten_bloc_container()
apply_theme()
render_header()

# Define pages

def get_pages():
    return [
        st.Page("pages/Home.py", title=f"🏠 {t('nav_home')}", default=True),
        st.Page("pages/NLP_Content_Intelligence.py", title=f"🧠 {t('nav_nlp')}"),
        st.Page("pages/Data_Engineering.py", title=f"🔧 {t('nav_data_engineering')}"),
        st.Page("pages/Asset_Quality_Mgmt.py", title=f"📚 {t('nav_asset_quality')}"),
        st.Page("pages/Contact.py", title=f"📬 {t('nav_contact')}"),
        st.Page("pages/Privacy.py", title=f"🔐 {t('nav_privacy')}"),
    ]

pages = get_pages()
pg = st.navigation(pages, position="top")
pg.run()

render_footer()
