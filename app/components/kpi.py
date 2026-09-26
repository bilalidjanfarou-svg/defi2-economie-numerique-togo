"""Cartes KPI réutilisables, avec variation (delta) optionnelle."""

import streamlit as st

from config import PALETTE


def kpi_card(col, label, value, icon="●", icon_color=None, delta=None, delta_positive_is_good=True):
    """delta : texte court, ex. '+4.2%' ou '+17 pts'. Coloré en vert/rouge selon le signe."""
    icon_color = icon_color or PALETTE["teal"]
    delta_html = ""
    if delta:
        is_positive = delta.strip().startswith("+")
        good = is_positive == delta_positive_is_good
        color = PALETTE["green"] if good else PALETTE["red"]
        delta_html = f'<div class="kpi-delta" style="color:{color};">{delta}</div>'
    with col:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-icon" style="background:{icon_color}22; color:{icon_color};">{icon}</div>
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
                {delta_html}
            </div>
            """,
            unsafe_allow_html=True,
        )


def kpi_row(items):
    """items : liste de dicts {label, value, icon, icon_color, delta}. Crée les colonnes automatiquement."""
    cols = st.columns(len(items))
    for col, item in zip(cols, items):
        kpi_card(
            col, item["label"], item["value"],
            icon=item.get("icon", "●"), icon_color=item.get("icon_color"),
            delta=item.get("delta"),
        )
