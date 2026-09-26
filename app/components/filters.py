"""Filtres réutilisables entre les vues."""

import streamlit as st


def region_filter(options, key, label="Région", all_label="Toutes les régions"):
    choice = st.selectbox(label, [all_label] + sorted(options), key=key)
    return None if choice == all_label else choice
