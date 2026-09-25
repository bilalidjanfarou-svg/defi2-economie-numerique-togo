import sys
from pathlib import Path

import plotly.express as px
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import DATA, PALETTE, apply_theme, kpi_card, load_csv, page_header, themed_layout  # noqa: E402

st.set_page_config(page_title="Cartographie", page_icon="🗺️", layout="wide")
apply_theme()

with st.sidebar:
    st.markdown("### 📶 Togo AI Lab")
    st.caption("Défi 2 · Économie Numérique")

page_header("CARTOGRAPHIE", "Points d'accès financiers", "Répartition géographique des agents mobile money et des établissements financiers.")

agents = load_csv(DATA / "agents_mobile_money.csv")
etabs = load_csv(DATA / "etablissements_financiers.csv")

MAPBOX_STYLE = "carto-positron"


def region_view(df, default_zoom=6.3):
    """Calcule le centre et le zoom adaptés à l'étendue des points affichés."""
    if df.empty:
        return dict(lat=8.6, lon=1.1), default_zoom
    lat_span = df["lat"].max() - df["lat"].min()
    lon_span = df["lon"].max() - df["lon"].min()
    span = max(lat_span, lon_span, 0.05)
    zoom = 6.3
    if span < 1.5:
        zoom = 8.4
    elif span < 3:
        zoom = 7.2
    center = dict(lat=df["lat"].mean(), lon=df["lon"].mean())
    return center, zoom


# ---------------------------------------------------------------------------
# Filtres communs
# ---------------------------------------------------------------------------
f1, f2, f3 = st.columns([1.3, 1, 1])
with f1:
    regions = sorted(set(agents["region"].dropna()) | set(etabs["region"].dropna()))
    region_choice = st.selectbox("Région", ["Toutes les régions"] + regions)
with f2:
    vue = st.radio("Affichage des agents MM", ["Points", "Densité"], horizontal=True)
with f3:
    st.write("")

a = agents if region_choice == "Toutes les régions" else agents[agents["region"] == region_choice]
e = etabs if region_choice == "Toutes les régions" else etabs[etabs["region"] == region_choice]

center, zoom = region_view(a if not a.empty else etabs)

# ---------------------------------------------------------------------------
# KPI de contexte
# ---------------------------------------------------------------------------
k1, k2, k3, k4 = st.columns(4)
kpi_card(k1, "Agents Mobile Money", f"{len(a):,}".replace(",", " "), "💳", PALETTE["amber"])
kpi_card(k2, "Établissements financiers", f"{len(e):,}".replace(",", " "), "🏦", PALETTE["navy"])
top_pref = a["prefecture"].value_counts().idxmax() if not a.empty else "—"
kpi_card(k3, "Préfecture la mieux dotée (MM)", top_pref, "📍", PALETTE["teal"])
n_ops = a["operateur"].nunique() if not a.empty else 0
kpi_card(k4, "Opérateurs actifs", str(n_ops), "📡", PALETTE["teal"])

st.write("")

tab1, tab2 = st.tabs(["📍 Agents Mobile Money", "🏦 Établissements financiers"])

# ---------------------------------------------------------------------------
# Onglet Mobile Money
# ---------------------------------------------------------------------------
with tab1:
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    if vue == "Densité":
        fig = px.density_mapbox(
            a, lat="lat", lon="lon", radius=6, center=center, zoom=zoom, height=580,
            color_continuous_scale=[PALETTE["bg"], PALETTE["teal"], PALETTE["amber"]],
        )
        fig.update_layout(coloraxis_colorbar=dict(title="Densité"))
    else:
        MAX_POINTS = 6000
        a_map = a.sample(MAX_POINTS, random_state=42) if len(a) > MAX_POINTS else a
        fig = px.scatter_mapbox(
            a_map, lat="lat", lon="lon", color="operateur",
            hover_name="prefecture",
            hover_data={"region": True, "commune": True, "lat": False, "lon": False, "operateur": True},
            center=center, zoom=zoom, height=580, opacity=0.75,
            color_discrete_sequence=[PALETTE["teal"], PALETTE["amber"], PALETTE["navy"], "#7C9CBF", "#C97B2E"],
        )
        fig.update_traces(marker=dict(size=6))
        if len(a) > MAX_POINTS:
            st.caption(f"Échantillon de {MAX_POINTS:,} points affiché sur {len(a):,} au total (pour la fluidité de la carte).".replace(",", " "))
    fig.update_layout(
        mapbox_style=MAPBOX_STYLE, margin=dict(t=0, b=0, l=0, r=0),
        legend=dict(orientation="h", y=-0.04, font=dict(color=PALETTE["muted"])),
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.write("")
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("**Nombre d'agents par préfecture (top 15)**")
    top_pref_chart = a.groupby("prefecture").size().sort_values(ascending=False).head(15)
    fig_bar = px.bar(top_pref_chart, orientation="h", labels={"value": "Nb agents", "prefecture": ""},
                      color_discrete_sequence=[PALETTE["teal"]])
    fig_bar = themed_layout(fig_bar, height=440, legend=False)
    fig_bar.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Onglet Établissements financiers
# ---------------------------------------------------------------------------
with tab2:
    ff1, ff2 = st.columns(2)
    with ff1:
        cats = sorted(e["categorie"].dropna().unique())
        cat_choice = st.multiselect("Catégorie", cats, default=cats)
    with ff2:
        stats = sorted(e["statut_simplifie"].dropna().unique())
        stat_choice = st.multiselect("Statut d'usage", stats, default=stats)

    e_filt = e[e["categorie"].isin(cat_choice) & e["statut_simplifie"].isin(stat_choice)]

    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.caption(f"{len(e_filt):,} établissements affichés".replace(",", " "))
    fig2 = px.scatter_mapbox(
        e_filt, lat="lat", lon="lon", color="categorie",
        hover_name="etab_nom",
        hover_data={"region": True, "prefecture": True, "statut_simplifie": True, "lat": False, "lon": False, "categorie": True},
        center=center, zoom=zoom, height=580, opacity=0.85,
        color_discrete_sequence=[PALETTE["navy"], PALETTE["teal"], PALETTE["amber"], "#7C9CBF", "#C97B2E"],
    )
    fig2.update_traces(marker=dict(size=8))
    fig2.update_layout(
        mapbox_style=MAPBOX_STYLE, margin=dict(t=0, b=0, l=0, r=0),
        legend=dict(orientation="h", y=-0.04, font=dict(color=PALETTE["muted"])),
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.write("")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("**Par catégorie**")
        cat_count = e_filt["categorie"].value_counts()
        fig_cat = px.pie(values=cat_count.values, names=cat_count.index, hole=0.55,
                          color_discrete_sequence=[PALETTE["navy"], PALETTE["teal"], PALETTE["amber"], "#7C9CBF", "#C97B2E"])
        fig_cat = themed_layout(fig_cat, height=340)
        fig_cat.update_traces(textinfo="percent", textfont=dict(color=PALETTE["surface"]))
        st.plotly_chart(fig_cat, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("**Par statut d'usage**")
        stat_count = e_filt["statut_simplifie"].value_counts()
        fig_stat = px.pie(values=stat_count.values, names=stat_count.index, hole=0.55,
                           color=stat_count.index,
                           color_discrete_map={"Actif": PALETTE["teal"], "Inactif": PALETTE["amber"], "Inconnu": PALETTE["muted"]})
        fig_stat = themed_layout(fig_stat, height=340)
        fig_stat.update_traces(textinfo="percent", textfont=dict(color=PALETTE["surface"]))
        st.plotly_chart(fig_stat, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

st.caption("Sources : opendata.gouv.tg — Agents mobile money, Établissements financiers géolocalisés.")