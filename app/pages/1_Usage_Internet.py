import sys
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import DATA, PALETTE, load_csv  # noqa: E402

st.set_page_config(page_title="Usage Internet", page_icon="🌐", layout="wide")
st.title("🌐 Évolution de l'usage d'Internet")

pct = load_csv(DATA / "internet_usage_pct.csv").sort_values("annee")
telecom_net = load_csv(DATA / "telecom_internet.csv")

# ---------------------------------------------------------------------------
# Courbe % population utilisant Internet (1996-2022)
# ---------------------------------------------------------------------------
st.subheader("Part de la population utilisant Internet (1996–2022)")

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=pct["annee"], y=pct["pct_population"], mode="lines+markers",
    line=dict(color=PALETTE["primary"], width=3), fill="tozeroy",
    fillcolor="rgba(59,130,246,0.15)", name="% population",
))
fig.update_layout(
    template="plotly_dark", height=420,
    yaxis_title="% de la population", xaxis_title="Année",
    margin=dict(t=20, b=20),
)
st.plotly_chart(fig, use_container_width=True)

# Repère des périodes d'accélération : variation annuelle
pct = pct.copy()
pct["delta"] = pct["pct_population"].diff()
periode_accel = pct.loc[pct["delta"].idxmax()] if pct["delta"].notna().any() else None

col1, col2 = st.columns(2)
with col1:
    if periode_accel is not None:
        st.info(
            f"📈 **Plus forte accélération** : +{periode_accel['delta']:.1f} points en "
            f"{int(periode_accel['annee'])} (vs. année précédente)."
        )
with col2:
    plateaux = pct[pct["delta"].abs() < 0.5].dropna()
    if not plateaux.empty:
        annees_plateau = ", ".join(str(int(a)) for a in plateaux["annee"].tail(5))
        st.warning(f"📉 **Périodes de quasi-stagnation** (variation < 0.5 pt) : {annees_plateau}")

st.divider()

# ---------------------------------------------------------------------------
# Abonnés Internet par technologie (haut débit vs total)
# ---------------------------------------------------------------------------
st.subheader("Abonnés Internet — taux de pénétration et technologies")

cols_dispo = [c for c in telecom_net.columns if c != "Date"]
default_cols = [c for c in [
    "Taux de pénétration Internet (Toutes technologies) (%)",
    "Taux de pénétration Internet haut débit (%)",
] if c in cols_dispo]

choix = st.multiselect("Indicateurs à afficher", cols_dispo, default=default_cols)

if choix:
    fig2 = go.Figure()
    colors = [PALETTE["primary"], PALETTE["secondary"], PALETTE["accent"], "#A78BFA", "#F472B6"]
    for i, c in enumerate(choix):
        fig2.add_trace(go.Scatter(
            x=telecom_net["Date"], y=telecom_net[c], mode="lines+markers",
            name=c, line=dict(color=colors[i % len(colors)], width=2.5),
        ))
    fig2.update_layout(template="plotly_dark", height=450, xaxis_title="Année", margin=dict(t=20))
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.caption("Sélectionne au moins un indicateur ci-dessus.")

st.caption("Sources : opendata.gouv.tg — Usage Internet (Banque Mondiale), Abonnés Internet Togo.")
