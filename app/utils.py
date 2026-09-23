"""Fonctions utilitaires partagées entre les pages du dashboard."""

from pathlib import Path

import pandas as pd
import streamlit as st

DATA = Path(__file__).resolve().parent.parent / "data" / "processed"

PALETTE = {
    "primary": "#3B82F6",
    "secondary": "#22D3EE",
    "accent": "#F59E0B",
    "muted": "#8B949E",
    "bg": "#0e1117",
    "card": "#161b22",
}


@st.cache_data
def load_csv(path):
    return pd.read_csv(path)


def kpi_card(col, label, value, help_text=None):
    with col:
        st.markdown(
            f"""
            <div class="metric-card">
                <div style="color:#8B949E; font-size:0.85rem;">{label}</div>
                <div style="color:#e6edf3; font-size:1.6rem; font-weight:600;">{value}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if help_text:
            st.caption(help_text)
