import sys
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))
from components.charts import themed_layout  # noqa: E402
from components.kpi import kpi_row  # noqa: E402
from components.theme import card_close, card_open, page_header  # noqa: E402
from config import PALETTE  # noqa: E402
from data_loader import load_internet_usage, load_telecom_internet  # noqa: E402
from metrics import get_internet_progress, get_internet_rate  # noqa: E402

page_header("INTERNET", "Adoption d'Internet au Togo", "Part de la population utilisant Internet, 1996–2022.")

pct, annee = get_internet_rate()
progress = get_internet_progress(years_back=3)

kpi_row([
    {"label": "Dernière valeur", "value": f"{pct:.1f} %", "icon": "🌐", "icon_color": PALETTE["teal"]},
    {"label": "Progression (3 ans)", "value": f"{progress:+.1f} pts" if progress is not None else "—", "icon": "📈", "icon_color": PALETTE["amber"], "delta": f"{progress:+.1f} pts" if progress is not None else None},
    {"label": "Période couverte", "value": "1996–2022", "icon": "📅", "icon_color": PALETTE["navy"]},
])

st.write("")
card_open()
df = load_internet_usage()
fig = go.Figure(go.Scatter(
    x=df["annee"], y=df["pct_population"], mode="lines+markers",
    line=dict(color=PALETTE["teal"], width=3), fill="tozeroy", fillcolor="rgba(23,162,184,0.10)",
))
fig = themed_layout(fig, height=420, legend=False)
fig.update_layout(yaxis_title="% de la population", xaxis_title=None)
st.plotly_chart(fig, width="stretch")
card_close()

df = df.copy()
df["delta"] = df["pct_population"].diff()
periode_accel = df.loc[df["delta"].idxmax()] if df["delta"].notna().any() else None

st.write("")
col1, col2 = st.columns(2)
with col1:
    if periode_accel is not None:
        st.info(f"📈 **Plus forte accélération** : +{periode_accel['delta']:.1f} points en {int(periode_accel['annee'])} (vs. année précédente).")
with col2:
    plateaux = df[df["delta"].abs() < 0.5].dropna()
    if not plateaux.empty:
        annees_plateau = ", ".join(str(int(a)) for a in plateaux["annee"].tail(5))
        st.warning(f"📉 **Périodes de quasi-stagnation** (variation < 0.5 pt) : {annees_plateau}")

st.write("")
page_header("ABONNÉS", "Taux de pénétration et technologies", None)

telecom_net = load_telecom_internet()
cols_dispo = [c for c in telecom_net.columns if c != "Date"]
default_cols = [c for c in [
    "Taux de pénétration Internet (Toutes technologies) (%)",
    "Taux de pénétration Internet haut débit (%)",
] if c in cols_dispo]
choix = st.multiselect("Indicateurs à afficher", cols_dispo, default=default_cols)

card_open()
if choix:
    fig2 = go.Figure()
    for c in choix:
        fig2.add_trace(go.Scatter(x=telecom_net["Date"], y=telecom_net[c], mode="lines+markers", name=c, line=dict(width=2.5)))
    fig2 = themed_layout(fig2, height=400)
    st.plotly_chart(fig2, width="stretch")
else:
    st.caption("Sélectionne au moins un indicateur ci-dessus.")
card_close()

st.caption("Sources : opendata.gouv.tg — Usage Internet (Banque Mondiale), Abonnés Internet Togo.")
