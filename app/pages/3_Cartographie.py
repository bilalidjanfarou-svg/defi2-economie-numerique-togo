import sys
from pathlib import Path

import plotly.express as px
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import DATA, load_csv  # noqa: E402

st.set_page_config(page_title="Cartographie", page_icon="🗺️", layout="wide")
st.title("🗺️ Cartographie des points d'accès financiers")

agents = load_csv(DATA / "agents_mobile_money.csv")
etabs = load_csv(DATA / "etablissements_financiers.csv")

st.markdown(
    "Répartition géographique des **agents mobile money** et des **établissements financiers** "
    "(banques, micro-finance, assurances, mutuelles)."
)

regions = sorted(set(agents["region"].dropna()) | set(etabs["region"].dropna()))
region_choice = st.selectbox("Filtrer par région", ["Toutes"] + regions)

a = agents if region_choice == "Toutes" else agents[agents["region"] == region_choice]
e = etabs if region_choice == "Toutes" else etabs[etabs["region"] == region_choice]

# Échantillonnage pour la fluidité de la carte si volume très important
MAX_POINTS = 6000
a_map = a.sample(MAX_POINTS, random_state=42) if len(a) > MAX_POINTS else a

tab1, tab2 = st.tabs(["📍 Agents Mobile Money", "🏦 Établissements financiers"])

with tab1:
    st.caption(f"{len(a):,} agents mobile money{' (échantillon affiché sur la carte)' if len(a) > MAX_POINTS else ''}".replace(",", " "))
    fig = px.scatter_mapbox(
        a_map, lat="lat", lon="lon", color="operateur",
        hover_data=["region", "prefecture", "commune"],
        zoom=6, height=600,
    )
    fig.update_layout(mapbox_style="carto-darkmatter", template="plotly_dark", margin=dict(t=0, b=0))
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Nombre d'agents par préfecture")
    top_pref = a.groupby("prefecture").size().sort_values(ascending=False).head(15)
    fig_bar = px.bar(top_pref, orientation="h", labels={"value": "Nb agents", "prefecture": ""})
    fig_bar.update_layout(template="plotly_dark", height=450, margin=dict(t=10), showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True)

with tab2:
    st.caption(f"{len(e):,} établissements référencés".replace(",", " "))
    fig2 = px.scatter_mapbox(
        e, lat="lat", lon="lon", color="categorie",
        hover_data=["region", "prefecture", "etab_nom", "statut_simplifie"],
        zoom=6, height=600,
    )
    fig2.update_layout(mapbox_style="carto-darkmatter", template="plotly_dark", margin=dict(t=0, b=0))
    st.plotly_chart(fig2, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Par catégorie")
        cat_count = e["categorie"].value_counts()
        fig_cat = px.pie(values=cat_count.values, names=cat_count.index, hole=0.45)
        fig_cat.update_layout(template="plotly_dark", height=380, margin=dict(t=10))
        st.plotly_chart(fig_cat, use_container_width=True)
    with c2:
        st.subheader("Par statut d'usage")
        stat_count = e["statut_simplifie"].value_counts()
        fig_stat = px.pie(values=stat_count.values, names=stat_count.index, hole=0.45,
                           color=stat_count.index,
                           color_discrete_map={"Actif": "#22D3EE", "Inactif": "#F59E0B", "Inconnu": "#8B949E"})
        fig_stat.update_layout(template="plotly_dark", height=380, margin=dict(t=10))
        st.plotly_chart(fig_stat, use_container_width=True)

st.caption("Sources : opendata.gouv.tg — Agents mobile money, Établissements financiers géolocalisés.")
