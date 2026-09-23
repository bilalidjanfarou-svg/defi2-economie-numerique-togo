import sys
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import DATA, PALETTE, load_csv  # noqa: E402

st.set_page_config(page_title="Marché télécom", page_icon="📡", layout="wide")
st.title("📡 Marché des télécommunications")

marche = load_csv(DATA / "telecom_marche.csv")

# ---------------------------------------------------------------------------
# Parts de marché (abonnés)
# ---------------------------------------------------------------------------
st.subheader("Parts de marché des opérateurs (en % d'abonnés)")

parts_cols = [c for c in marche.columns if "Part de marché" in c]
if parts_cols:
    fig = go.Figure()
    colors = [PALETTE["primary"], PALETTE["accent"], PALETTE["secondary"]]
    for i, c in enumerate(parts_cols):
        label = c.replace("Part de marché ", "").replace(" (en abonnées) en %", "")
        fig.add_trace(go.Bar(x=marche["Date"], y=marche[c], name=label, marker_color=colors[i % len(colors)]))
    fig.update_layout(template="plotly_dark", barmode="stack", height=420, xaxis_title="Année",
                       yaxis_title="% des abonnés", margin=dict(t=20))
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Aucune colonne de part de marché trouvée dans les données.")

st.divider()

# ---------------------------------------------------------------------------
# Chiffre d'affaires & Investissements
# ---------------------------------------------------------------------------
c1, c2 = st.columns(2)

with c1:
    st.subheader("Chiffre d'affaires du secteur")
    if "Chiffres d'Affaires" in marche.columns:
        fig_ca = go.Figure(go.Scatter(
            x=marche["Date"], y=marche["Chiffres d'Affaires"], mode="lines+markers",
            line=dict(color=PALETTE["primary"], width=3), fill="tozeroy",
            fillcolor="rgba(59,130,246,0.15)",
        ))
        fig_ca.update_layout(template="plotly_dark", height=380, margin=dict(t=10))
        st.plotly_chart(fig_ca, use_container_width=True)

with c2:
    st.subheader("Investissements")
    if "Investissement" in marche.columns:
        fig_inv = go.Figure(go.Bar(
            x=marche["Date"], y=marche["Investissement"], marker_color=PALETTE["accent"],
        ))
        fig_inv.update_layout(template="plotly_dark", height=380, margin=dict(t=10))
        st.plotly_chart(fig_inv, use_container_width=True)

st.divider()

# ---------------------------------------------------------------------------
# Télédensité fixe vs mobile
# ---------------------------------------------------------------------------
st.subheader("Télédensité — fixe vs mobile GSM")
tele_cols = [c for c in ["Télédensité fixe", "Télédensité mobile GSM"] if c in marche.columns]
if tele_cols:
    fig3 = go.Figure()
    for i, c in enumerate(tele_cols):
        fig3.add_trace(go.Scatter(
            x=marche["Date"], y=marche[c], mode="lines+markers", name=c,
            line=dict(width=2.5, color=[PALETTE["primary"], PALETTE["secondary"]][i]),
        ))
    fig3.update_layout(template="plotly_dark", height=400, xaxis_title="Année", margin=dict(t=20))
    st.plotly_chart(fig3, use_container_width=True)

with st.expander("Voir toutes les données brutes du marché télécom"):
    st.dataframe(marche, use_container_width=True)

st.caption("Source : opendata.gouv.tg — Récapitulation segment téléphonie et GSM au Togo.")
