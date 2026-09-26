import sys
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))
from components.charts import themed_layout  # noqa: E402
from components.kpi import kpi_row  # noqa: E402
from components.theme import card_close, card_open, page_header  # noqa: E402
from config import PALETTE  # noqa: E402
from data_loader import load_telecom_marche  # noqa: E402

page_header("MARCHÉ TÉLÉCOM", "Performance du secteur des télécommunications", "2013–2019.")

marche = load_telecom_marche()

last = marche.iloc[-1]
col_ca = "Chiffres d'Affaires"
ca_val = f"{last[col_ca] / 1e9:,.0f} Md FCFA" if col_ca in marche.columns else "—"
inv_val = f"{last['Investissement'] / 1e9:,.0f} Md FCFA" if "Investissement" in marche.columns else "—"
tele_val = f"{last['Télédensité mobile GSM']:.1f} %" if "Télédensité mobile GSM" in marche.columns else "—"

kpi_row([
    {"label": "Chiffre d'affaires (dernière année)", "value": ca_val, "icon": "💰", "icon_color": PALETTE["navy"]},
    {"label": "Investissement (dernière année)", "value": inv_val, "icon": "🏗️", "icon_color": PALETTE["amber"]},
    {"label": "Télédensité mobile GSM", "value": tele_val, "icon": "📡", "icon_color": PALETTE["teal"]},
])

st.write("")
card_open()
st.markdown("**Parts de marché des opérateurs** *(% d'abonnés)*")
parts_cols = [c for c in marche.columns if "Part de marché" in c]
if parts_cols:
    fig = go.Figure()
    for c in parts_cols:
        label = c.replace("Part de marché ", "").replace(" (en abonnées) en %", "")
        fig.add_trace(go.Bar(x=marche["Date"], y=marche[c], name=label))
    fig = themed_layout(fig, height=400)
    fig.update_layout(barmode="stack", yaxis_title="% des abonnés")
    st.plotly_chart(fig, width="stretch")
else:
    st.info("Aucune colonne de part de marché trouvée dans les données.")
card_close()

st.write("")
card_open()
st.markdown("**Télédensité — fixe vs mobile GSM**")
tele_cols = [c for c in ["Télédensité fixe", "Télédensité mobile GSM"] if c in marche.columns]
if tele_cols:
    fig3 = go.Figure()
    for c in tele_cols:
        fig3.add_trace(go.Scatter(x=marche["Date"], y=marche[c], mode="lines+markers", name=c, line=dict(width=2.5)))
    fig3 = themed_layout(fig3, height=380)
    st.plotly_chart(fig3, width="stretch")
card_close()

with st.expander("Voir toutes les données brutes du marché télécom"):
    st.dataframe(marche, width="stretch")

st.caption("Source : opendata.gouv.tg — Récapitulation segment téléphonie et GSM au Togo.")
