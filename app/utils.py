"""Fonctions utilitaires et thème visuel partagés entre les pages du dashboard."""

from pathlib import Path

import pandas as pd
import streamlit as st

DATA = Path(__file__).resolve().parent.parent / "data" / "processed"

# ---------------------------------------------------------------------------
# Palette — cohérente avec le rapport PowerPoint du Défi 2
# ---------------------------------------------------------------------------
PALETTE = {
    "navy": "#12203C",
    "navy_light": "#1C3057",
    "teal": "#17A2B8",
    "amber": "#F4A100",
    "bg": "#F7F8FA",
    "surface": "#FFFFFF",
    "text": "#1A1A1A",
    "muted": "#6B7684",
    "border": "#E4E7EC",
}

CHART_SEQUENCE = [PALETTE["teal"], PALETTE["amber"], PALETTE["navy"], "#7C9CBF", "#C97B2E"]


@st.cache_data
def load_csv(path):
    return pd.read_csv(path)


def apply_theme():
    """Injecte les styles globaux : polices, fond, cartes, sidebar, tableaux."""
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Newsreader:wght@500;600;700&family=Inter:wght@400;500;600&display=swap');

        html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}
        h1, h2, h3, .page-title {{ font-family: 'Newsreader', serif; }}

        .stApp {{ background-color: {PALETTE['bg']}; }}

        section[data-testid="stSidebar"] {{
            background-color: {PALETTE['navy']};
        }}
        section[data-testid="stSidebar"] * {{ color: #D7DEE9 !important; }}
        section[data-testid="stSidebar"] .stMarkdown p {{ color: #8FA3C4 !important; }}

        /* Titres de page */
        .page-eyebrow {{
            color: {PALETTE['teal']}; font-size: 0.8rem; font-weight: 600;
            margin-bottom: 0.2rem;
        }}
        .page-title {{
            color: {PALETTE['navy']}; font-size: 2.1rem; font-weight: 600;
            margin-bottom: 0.15rem; line-height: 1.2;
        }}
        .page-subtitle {{ color: {PALETTE['muted']}; font-size: 0.95rem; margin-bottom: 1.4rem; }}

        /* Cartes KPI */
        .kpi-card {{
            background: {PALETTE['surface']}; border: 1px solid {PALETTE['border']};
            border-radius: 12px; padding: 1.1rem 1.3rem; height: 100%;
        }}
        .kpi-icon {{
            width: 38px; height: 38px; border-radius: 10px; display: flex;
            align-items: center; justify-content: center; font-size: 1.1rem;
            margin-bottom: 0.6rem;
        }}
        .kpi-label {{ color: {PALETTE['muted']}; font-size: 0.82rem; margin-bottom: 0.15rem; }}
        .kpi-value {{ color: {PALETTE['navy']}; font-size: 1.7rem; font-weight: 700; font-family: 'Newsreader', serif; }}

        /* Cartes contenu génériques */
        .content-card {{
            background: {PALETTE['surface']}; border: 1px solid {PALETTE['border']};
            border-radius: 12px; padding: 1.3rem 1.5rem;
        }}

        div[data-testid="stDataFrame"] {{ border: 1px solid {PALETTE['border']}; border-radius: 10px; }}

        /* Onglets */
        .stTabs [data-baseweb="tab"] {{ font-family: 'Inter', sans-serif; font-weight: 500; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_header(eyebrow, title, subtitle=None):
    st.markdown(f'<div class="page-eyebrow">{eyebrow}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-title">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="page-subtitle">{subtitle}</div>', unsafe_allow_html=True)


def kpi_card(col, label, value, icon="●", icon_color=None):
    icon_color = icon_color or PALETTE["teal"]
    with col:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-icon" style="background:{icon_color}22; color:{icon_color};">{icon}</div>
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def themed_layout(fig, height=420, legend=True):
    """Applique un habillage clair cohérent à toutes les figures Plotly."""
    fig.update_layout(
        template="plotly_white",
        height=height,
        font=dict(family="Inter, sans-serif", color=PALETTE["text"], size=12),
        title_font=dict(family="Newsreader, serif", size=16, color=PALETTE["navy"]),
        margin=dict(t=40 if fig.layout.title.text else 20, b=30, l=40, r=20),
        plot_bgcolor=PALETTE["surface"],
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=legend,
        legend=dict(orientation="h", y=-0.18, x=0, font=dict(size=11, color=PALETTE["muted"])),
        colorway=CHART_SEQUENCE,
        xaxis=dict(gridcolor=PALETTE["border"], zeroline=False),
        yaxis=dict(gridcolor=PALETTE["border"], zeroline=False),
    )
    return fig