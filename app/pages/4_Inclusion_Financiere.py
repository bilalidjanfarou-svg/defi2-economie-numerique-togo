import sys
from pathlib import Path

import plotly.express as px
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import DATA, PALETTE, load_csv  # noqa: E402

st.set_page_config(page_title="Inclusion financière", page_icon="💳", layout="wide")
st.title("💳 Inclusion financière & rôle du mobile money")

synth = load_csv(DATA / "synthese_region.csv")
agents = load_csv(DATA / "agents_mobile_money.csv")
etabs = load_csv(DATA / "etablissements_financiers.csv")

st.subheader("Habitants par point de service, par région")
c1, c2 = st.columns(2)
with c1:
    fig1 = px.bar(
        synth.sort_values("habitants_par_agent_mm"), x="habitants_par_agent_mm", y="region",
        orientation="h", title="Habitants par agent Mobile Money",
        color_discrete_sequence=[PALETTE["secondary"]],
    )
    fig1.update_layout(template="plotly_dark", height=380, margin=dict(t=40))
    st.plotly_chart(fig1, use_container_width=True)
with c2:
    fig2 = px.bar(
        synth.sort_values("habitants_par_etab_financier"), x="habitants_par_etab_financier", y="region",
        orientation="h", title="Habitants par établissement financier",
        color_discrete_sequence=[PALETTE["primary"]],
    )
    fig2.update_layout(template="plotly_dark", height=380, margin=dict(t=40))
    st.plotly_chart(fig2, use_container_width=True)

st.info(
    "👉 Plus un territoire a d'habitants par point de service, plus l'accès y est difficile. "
    "**Savanes** cumule le ratio le plus défavorable sur les deux indicateurs."
)

st.divider()

st.subheader("Agents mobile money pour 1 établissement financier")
fig3 = px.bar(
    synth.sort_values("agents_mm_par_etab_financier", ascending=False),
    x="region", y="agents_mm_par_etab_financier",
    color="agents_mm_par_etab_financier", color_continuous_scale="Blues",
    labels={"agents_mm_par_etab_financier": "Agents MM / établissement"},
)
fig3.update_layout(template="plotly_dark", height=400, margin=dict(t=20), coloraxis_showscale=False)
st.plotly_chart(fig3, use_container_width=True)
st.caption(
    "Un ratio élevé confirme que le mobile money couvre un territoire bien plus large que le "
    "réseau bancaire classique — c'est la porte d'entrée dominante vers les services financiers."
)

st.divider()

st.subheader("Préfectures desservies uniquement par le mobile money")
pref_agents = set(agents["prefecture"].dropna().unique())
pref_etabs = set(etabs["prefecture"].dropna().unique())
mm_only = sorted(pref_agents - pref_etabs)

if mm_only:
    st.warning(
        f"**{len(mm_only)} préfectures** n'ont aucun établissement financier référencé mais "
        f"disposent d'agents mobile money — le mobile money y est le seul point d'accès recensé :"
    )
    st.write(", ".join(mm_only))
else:
    st.success("Toutes les préfectures avec agents mobile money ont aussi au moins un établissement financier.")

st.caption("Sources : agents mobile money et établissements financiers géolocalisés, opendata.gouv.tg.")
