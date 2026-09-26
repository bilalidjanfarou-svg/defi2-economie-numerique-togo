import sys
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))
from components.charts import themed_layout  # noqa: E402
from components.kpi import kpi_row  # noqa: E402
from components.theme import card_close, card_open, hero  # noqa: E402
from config import APP_TAGLINE, PALETTE  # noqa: E402
from data_loader import load_internet_usage  # noqa: E402
from metrics import (  # noqa: E402
    get_internet_rate,
    get_regional_metrics,
    get_total_agents,
    get_total_financial_institutions,
    get_total_population,
)

hero(
    "TOGO DIGITAL INSIGHT",
    "Comprendre l'économie numérique à travers les données",
    APP_TAGLINE + " — évolution d'Internet, des télécommunications et du mobile money.",
)

pct, annee = get_internet_rate()
kpi_row([
    {"label": "Population du Togo (2022)", "value": f"{get_total_population():,}".replace(",", " "), "icon": "👥", "icon_color": PALETTE["navy"]},
    {"label": f"Utilisateurs Internet ({annee})", "value": f"{pct:.1f} %", "icon": "🌐", "icon_color": PALETTE["teal"]},
    {"label": "Agents Mobile Money", "value": f"{get_total_agents():,}".replace(",", " "), "icon": "💳", "icon_color": PALETTE["amber"]},
    {"label": "Établissements financiers actifs", "value": f"{get_total_financial_institutions():,}".replace(",", " "), "icon": "🏦", "icon_color": PALETTE["navy"]},
])

st.write("")
c1, c2 = st.columns([1.4, 1])

with c1:
    card_open()
    st.markdown("**Évolution de l'usage d'Internet** *(1996–2022)*")
    df = load_internet_usage()
    fig = go.Figure(go.Scatter(
        x=df["annee"], y=df["pct_population"], mode="lines+markers",
        line=dict(color=PALETTE["teal"], width=3), fill="tozeroy", fillcolor="rgba(23,162,184,0.10)",
    ))
    fig = themed_layout(fig, height=300, legend=False)
    st.plotly_chart(fig, width="stretch")
    card_close()

with c2:
    card_open()
    st.markdown("**Répartition régionale — Agents Mobile Money**")
    synth = get_regional_metrics()
    fig2 = go.Figure(go.Bar(
        x=synth.sort_values("nb_agents_mm")["nb_agents_mm"],
        y=synth.sort_values("nb_agents_mm")["region"],
        orientation="h", marker_color=PALETTE["amber"],
    ))
    fig2 = themed_layout(fig2, height=300, legend=False)
    st.plotly_chart(fig2, width="stretch")
    card_close()

st.write("")
with st.expander("📋 Afficher les données détaillées par région"):
    synth = get_regional_metrics()
    st.dataframe(
        synth.rename(columns={
            "region": "Région", "population": "Population", "nb_agents_mm": "Agents MM",
            "nb_etab_financiers_actifs": "Étab. financiers actifs",
            "habitants_par_agent_mm": "Hab. / agent MM",
            "habitants_par_etab_financier": "Hab. / étab. financier",
            "agents_mm_par_etab_financier": "Agents MM / étab.",
        }).style.format({
            "Population": "{:,.0f}", "Agents MM": "{:,.0f}", "Étab. financiers actifs": "{:,.0f}",
            "Hab. / agent MM": "{:,.0f}", "Hab. / étab. financier": "{:,.0f}", "Agents MM / étab.": "{:,.1f}",
        }),
        width="stretch", hide_index=True,
    )

st.caption("Sources : opendata.gouv.tg — Internet, télécoms, établissements financiers, agents mobile money, RGPH-5 (2022).")
