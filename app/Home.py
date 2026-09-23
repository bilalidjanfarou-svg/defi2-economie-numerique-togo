"""
Home.py — Point d'entrée du dashboard
Défi 2 Économie Numérique — Togo AI Lab
Adoption du numérique & inclusion financière par mobile money
"""

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent))
from utils import DATA, load_csv, kpi_card  # noqa: E402

st.set_page_config(
    page_title="Défi 2 — Économie Numérique Togo",
    page_icon="📶",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Thème sombre léger (cohérent avec le dashboard du Défi 1 — "Atlas Connectivité")
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    .stApp { background-color: #0e1117; }
    .metric-card {
        background: #161b22; border: 1px solid #2a2f3a; border-radius: 10px;
        padding: 1rem 1.2rem; margin-bottom: .5rem;
    }
    h1, h2, h3 { color: #e6edf3; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("📶 Adoption du numérique & inclusion financière au Togo")
st.caption("Défi 2 — Économie Numérique · Togo AI Lab")

st.markdown(
    """
Moins de **4 personnes sur 10** utilisent Internet au Togo, et les banques restent concentrées
dans les villes. Le **mobile money** est devenu, pour beaucoup de ménages, la principale porte
d'entrée vers les services financiers.

Ce tableau de bord explore :
- l'évolution de l'usage d'Internet et du marché des télécoms,
- la répartition géographique des établissements financiers et des agents mobile money,
- les écarts d'accès entre régions,
- des recommandations pour accélérer l'inclusion numérique et financière.

👉 Utilise le menu à gauche pour naviguer entre les pages.
"""
)

st.divider()

# ---------------------------------------------------------------------------
# KPIs de synthèse (dernière année disponible)
# ---------------------------------------------------------------------------
synth = load_csv(DATA / "synthese_region.csv")
internet_pct = load_csv(DATA / "internet_usage_pct.csv")
pop_togo = load_csv(DATA / "population_togo.csv")

last_pct = internet_pct.sort_values("annee").iloc[-1]

c1, c2, c3, c4 = st.columns(4)
kpi_card(c1, "Population du Togo (2022)", f"{int(pop_togo['population'].iloc[0]):,}".replace(",", " "))
kpi_card(c2, f"Utilisateurs Internet ({int(last_pct['annee'])})", f"{last_pct['pct_population']:.1f} %")
kpi_card(c3, "Agents Mobile Money recensés", f"{int(synth['nb_agents_mm'].sum()):,}".replace(",", " "))
kpi_card(c4, "Établissements financiers actifs", f"{int(synth['nb_etab_financiers_actifs'].sum()):,}".replace(",", " "))

st.divider()
st.subheader("Aperçu régional")
st.dataframe(
    synth.style.format({
        "population": "{:,.0f}",
        "nb_agents_mm": "{:,.0f}",
        "nb_etab_financiers_actifs": "{:,.0f}",
        "habitants_par_agent_mm": "{:,.0f}",
        "habitants_par_etab_financier": "{:,.0f}",
        "agents_mm_par_etab_financier": "{:,.1f}",
    }),
    use_container_width=True,
    hide_index=True,
)

st.caption(
    "Sources : Agence Togo Digital / opendata.gouv.tg — Internet, télécoms, établissements "
    "financiers, agents mobile money, RGPH-5 (2022)."
)
