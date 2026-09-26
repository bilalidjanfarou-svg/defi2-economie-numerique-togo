import sys
from pathlib import Path

import plotly.express as px
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))
from components.charts import MAP_STYLE, MAP_STYLE_KEY, density_geo, region_bar_chart, scatter_geo, themed_layout  # noqa: E402
from components.kpi import kpi_row  # noqa: E402
from components.theme import card_close, card_open, page_header  # noqa: E402
from config import PALETTE  # noqa: E402
from data_loader import load_agents_mm, load_etablissements  # noqa: E402

page_header("CARTOGRAPHIE", "Points d'accès financiers au Togo", "Répartition géographique des agents mobile money et des établissements financiers.")

agents = load_agents_mm()
etabs = load_etablissements()


def region_view(df, default_zoom=6.3):
    if df.empty:
        return dict(lat=8.6, lon=1.1), default_zoom
    span = max(df["lat"].max() - df["lat"].min(), df["lon"].max() - df["lon"].min(), 0.05)
    zoom = 8.4 if span < 1.5 else 7.2 if span < 3 else default_zoom
    return dict(lat=df["lat"].mean(), lon=df["lon"].mean()), zoom


# ---------------------------------------------------------------------------
# Barre de filtres
# ---------------------------------------------------------------------------
f1, f2, f3 = st.columns(3)
with f1:
    regions = sorted(set(agents["region"].dropna()) | set(etabs["region"].dropna()))
    region_choice = st.selectbox("Région", ["Toutes les régions"] + regions)
with f2:
    type_choice = st.selectbox("Type de point d'accès", ["Mobile Money", "Établissements financiers"])
with f3:
    vue = st.selectbox("Affichage", ["Points", "Densité"]) if type_choice == "Mobile Money" else "Points"

a = agents if region_choice == "Toutes les régions" else agents[agents["region"] == region_choice]
e = etabs if region_choice == "Toutes les régions" else etabs[etabs["region"] == region_choice]
center, zoom = region_view(a if not a.empty else etabs)

# ---------------------------------------------------------------------------
# Carte
# ---------------------------------------------------------------------------
card_open()
if type_choice == "Mobile Money":
    if vue == "Densité":
        fig = density_geo(a, lat="lat", lon="lon", radius=6, center=center, zoom=zoom, height=560,
                           color_continuous_scale=[PALETTE["background"], PALETTE["teal"], PALETTE["amber"]])
        fig.update_layout(coloraxis_colorbar=dict(title="Densité"))
    else:
        MAX_POINTS = 6000
        a_map = a.sample(MAX_POINTS, random_state=42) if len(a) > MAX_POINTS else a
        fig = scatter_geo(a_map, lat="lat", lon="lon", color="operateur", hover_name="prefecture",
                           hover_data={"region": True, "commune": True, "lat": False, "lon": False, "operateur": True},
                           center=center, zoom=zoom, height=560, opacity=0.75,
                           color_discrete_sequence=[PALETTE["teal"], PALETTE["amber"], PALETTE["navy"], "#7C9CBF", "#C97B2E"])
        fig.update_traces(marker=dict(size=6))
        if len(a) > MAX_POINTS:
            st.caption(f"Échantillon de {MAX_POINTS:,} points affiché sur {len(a):,} au total.".replace(",", " "))
else:
    fig = scatter_geo(e, lat="lat", lon="lon", color="categorie", hover_name="etab_nom",
                       hover_data={"region": True, "prefecture": True, "statut_simplifie": True, "lat": False, "lon": False, "categorie": True},
                       center=center, zoom=zoom, height=560, opacity=0.85,
                       color_discrete_sequence=[PALETTE["navy"], PALETTE["teal"], PALETTE["amber"], "#7C9CBF", "#C97B2E"])
    fig.update_traces(marker=dict(size=8))

fig.update_layout(**{MAP_STYLE_KEY: MAP_STYLE}, margin=dict(t=0, b=0, l=0, r=0),
                   legend=dict(orientation="h", y=-0.04, font=dict(color=PALETTE["muted"])),
                   paper_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig, width="stretch")
card_close()

# ---------------------------------------------------------------------------
# KPI sous la carte
# ---------------------------------------------------------------------------
st.write("")
kpi_row([
    {"label": "Agents Mobile Money", "value": f"{len(a):,}".replace(",", " "), "icon": "💳", "icon_color": PALETTE["amber"]},
    {"label": "Établissements financiers", "value": f"{len(e):,}".replace(",", " "), "icon": "🏦", "icon_color": PALETTE["navy"]},
    {"label": "Régions couvertes", "value": str(len(regions)), "icon": "🗺️", "icon_color": PALETTE["teal"]},
])

# ---------------------------------------------------------------------------
# Détail par préfecture / catégorie
# ---------------------------------------------------------------------------
st.write("")
if type_choice == "Mobile Money":
    card_open()
    st.markdown("**Nombre d'agents par préfecture (top 15)**")
    top_pref = a.groupby("prefecture").size().sort_values(ascending=False).head(15)
    fig_bar = px.bar(top_pref, orientation="h", labels={"value": "Nb agents", "prefecture": ""}, color_discrete_sequence=[PALETTE["teal"]])
    fig_bar = themed_layout(fig_bar, height=440, legend=False)
    fig_bar.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig_bar, width="stretch")
    card_close()
else:
    c1, c2 = st.columns(2)
    with c1:
        card_open()
        st.markdown("**Par catégorie**")
        cat_count = e["categorie"].value_counts()
        fig_cat = px.pie(values=cat_count.values, names=cat_count.index, hole=0.55,
                          color_discrete_sequence=[PALETTE["navy"], PALETTE["teal"], PALETTE["amber"], "#7C9CBF", "#C97B2E"])
        fig_cat = themed_layout(fig_cat, height=340)
        fig_cat.update_traces(textinfo="percent", textfont=dict(color=PALETTE["surface"]))
        st.plotly_chart(fig_cat, width="stretch")
        card_close()
    with c2:
        card_open()
        st.markdown("**Par statut d'usage**")
        stat_count = e["statut_simplifie"].value_counts()
        fig_stat = px.pie(values=stat_count.values, names=stat_count.index, hole=0.55, color=stat_count.index,
                           color_discrete_map={"Actif": PALETTE["teal"], "Inactif": PALETTE["amber"], "Inconnu": PALETTE["muted"]})
        fig_stat = themed_layout(fig_stat, height=340)
        fig_stat.update_traces(textinfo="percent", textfont=dict(color=PALETTE["surface"]))
        st.plotly_chart(fig_stat, width="stretch")
        card_close()

st.caption("Sources : opendata.gouv.tg — Agents mobile money, Établissements financiers géolocalisés.")
