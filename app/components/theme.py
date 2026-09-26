"""Thème visuel global — CSS injecté une fois, en-têtes de page, hero d'accueil."""

import streamlit as st

from config import PALETTE


def apply_theme():
    """Injecte les styles globaux. À appeler une seule fois, dans Home.py."""
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Newsreader:wght@500;600;700&family=Inter:wght@400;500;600&display=swap');

        html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}
        h1, h2, h3, .page-title, .hero-title {{ font-family: 'Newsreader', serif; }}

        .stApp {{ background-color: {PALETTE['background']}; }}

        section[data-testid="stSidebar"] {{ background-color: {PALETTE['navy']}; }}
        section[data-testid="stSidebar"] * {{ color: #D7DEE9 !important; }}
        section[data-testid="stSidebar"] .stMarkdown p {{ color: #8FA3C4 !important; }}
        section[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] {{
            border-radius: 8px;
        }}

        .page-eyebrow {{ color: {PALETTE['teal']}; font-size: 0.8rem; font-weight: 600; margin-bottom: 0.2rem; }}
        .page-title {{ color: {PALETTE['navy']}; font-size: 2.1rem; font-weight: 600; margin-bottom: 0.15rem; line-height: 1.2; }}
        .page-subtitle {{ color: {PALETTE['muted']}; font-size: 0.95rem; margin-bottom: 1.4rem; }}

        .hero {{
            background: linear-gradient(135deg, {PALETTE['navy']} 0%, #1C3057 100%);
            border-radius: 16px; padding: 2.4rem 2.6rem; margin-bottom: 1.6rem;
        }}
        .hero-eyebrow {{ color: {PALETTE['amber']}; font-size: 0.8rem; font-weight: 700; letter-spacing: 1.5px; margin-bottom: 0.6rem; }}
        .hero-title {{ color: #FFFFFF; font-size: 2.3rem; font-weight: 600; line-height: 1.25; margin-bottom: 0.7rem; }}
        .hero-subtitle {{ color: #C9D3E0; font-size: 1rem; max-width: 640px; line-height: 1.5; }}

        .kpi-card {{
            background: {PALETTE['surface']}; border: 1px solid {PALETTE['border']};
            border-radius: 12px; padding: 1.1rem 1.3rem; height: 100%;
        }}
        .kpi-icon {{
            width: 38px; height: 38px; border-radius: 10px; display: flex;
            align-items: center; justify-content: center; font-size: 1.1rem; margin-bottom: 0.6rem;
        }}
        .kpi-label {{ color: {PALETTE['muted']}; font-size: 0.82rem; margin-bottom: 0.15rem; }}
        .kpi-value {{ color: {PALETTE['navy']}; font-size: 1.7rem; font-weight: 700; font-family: 'Newsreader', serif; }}
        .kpi-delta {{ font-size: 0.8rem; font-weight: 600; margin-top: 0.1rem; }}

        .content-card {{
            background: {PALETTE['surface']}; border: 1px solid {PALETTE['border']};
            border-radius: 12px; padding: 1.3rem 1.5rem;
        }}
        .insight-tag {{
            display: inline-block; font-size: 0.72rem; font-weight: 700; letter-spacing: 0.5px;
            color: {PALETTE['teal']}; background: {PALETTE['teal']}1A; border-radius: 6px;
            padding: 0.15rem 0.5rem; margin-bottom: 0.5rem;
        }}
        .insight-figure {{
            font-family: 'Newsreader', serif; font-weight: 700; font-size: 1.6rem; color: {PALETTE['navy']};
        }}

        div[data-testid="stDataFrame"] {{ border: 1px solid {PALETTE['border']}; border-radius: 10px; }}
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


def hero(eyebrow, title, subtitle):
    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-eyebrow">{eyebrow}</div>
            <div class="hero-title">{title}</div>
            <div class="hero-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def card_open():
    st.markdown('<div class="content-card">', unsafe_allow_html=True)


def card_close():
    st.markdown("</div>", unsafe_allow_html=True)
