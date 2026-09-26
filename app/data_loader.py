"""Chargement centralisé des données traitées (data/processed/)."""

from pathlib import Path

import pandas as pd
import streamlit as st

DATA = Path(__file__).resolve().parent.parent / "data" / "processed"


@st.cache_data
def _read(name):
    return pd.read_csv(DATA / name)


def load_synthese_region():
    return _read("synthese_region.csv")


def load_population_togo():
    return _read("population_togo.csv")


def load_internet_usage():
    return _read("internet_usage_pct.csv").sort_values("annee")


def load_telecom_internet():
    return _read("telecom_internet.csv")


def load_telecom_marche():
    return _read("telecom_marche.csv")


def load_agents_mm():
    return _read("agents_mobile_money.csv")


def load_etablissements():
    return _read("etablissements_financiers.csv")
