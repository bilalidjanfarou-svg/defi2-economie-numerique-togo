"""
Home.py — Point d'entrée de TOGO DIGITAL INSIGHT
Défi 2 Économie Numérique — Togo AI Lab
"""

from pathlib import Path

import streamlit as st

from components.theme import apply_theme
from config import APP_FOOTER, APP_NAME

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)
apply_theme()

BASE = Path(__file__).resolve().parent / "views"

with st.sidebar:
    st.markdown(f"### 🌍 {APP_NAME}")
    st.caption("Défi 2 · Économie Numérique")
    st.divider()

pages = {
    "": [
        st.Page(str(BASE / "accueil.py"), title="Vue d'ensemble", icon="🏠", default=True),
    ],
    "Données": [
        st.Page(str(BASE / "internet.py"), title="Internet", icon="🌐"),
        st.Page(str(BASE / "telecom.py"), title="Télécoms", icon="📡"),
        st.Page(str(BASE / "finance.py"), title="Inclusion financière", icon="💳"),
    ],
    "Explorer": [
        st.Page(str(BASE / "cartographie.py"), title="Cartographie", icon="🗺️"),
        st.Page(str(BASE / "insights.py"), title="Insights", icon="💡"),
    ],
}

pg = st.navigation(pages)

with st.sidebar:
    st.divider()
    st.caption(APP_FOOTER)

pg.run()
