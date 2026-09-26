import sys
from pathlib import Path

import plotly.express as px
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))
from components.charts import region_bar_chart, themed_layout  # noqa: E402
from components.theme import card_close, card_open, page_header  # noqa: E402
from config import PALETTE  # noqa: E402
from metrics import get_mm_only_prefectures, get_regional_metrics  # noqa: E402

page_header("INCLUSION FINANCIÈRE", "Le rôle du mobile money", "Habitants par point de service et territoires desservis uniquement par le mobile money.")

synth = get_regional_metrics()

c1, c2 = st.columns(2)
with c1:
    card_open()
    st.markdown("**Habitants par agent Mobile Money**")
    st.plotly_chart(region_bar_chart(synth, "habitants_par_agent_mm", None, color=PALETTE["teal"]), width="stretch")
    st.markdown(
        f'<div class="insight-tag">📌 LECTURE</div><div style="color:{PALETTE["muted"]}; font-size:0.88rem;">'
        "Plus ce nombre est élevé, plus chaque agent mobile money dessert un grand nombre d'habitants "
        "— donc moins l'accès y est pratique.</div>",
        unsafe_allow_html=True,
    )
    card_close()
with c2:
    card_open()
    st.markdown("**Habitants par établissement financier**")
    st.plotly_chart(region_bar_chart(synth, "habitants_par_etab_financier", None, color=PALETTE["amber"]), width="stretch")
    st.markdown(
        f'<div class="insight-tag">📌 LECTURE</div><div style="color:{PALETTE["muted"]}; font-size:0.88rem;">'
        "Cet indicateur permet de comparer la densité de points de service bancaires classiques entre régions.</div>",
        unsafe_allow_html=True,
    )
    card_close()

st.write("")
st.info("👉 Plus un territoire a d'habitants par point de service, plus l'accès y est difficile. **Savanes** cumule le ratio le plus défavorable sur les deux indicateurs.")

st.write("")
card_open()
st.markdown("**Agents mobile money pour 1 établissement financier**")
fig3 = px.bar(synth.sort_values("agents_mm_par_etab_financier", ascending=False), x="region", y="agents_mm_par_etab_financier",
              color="agents_mm_par_etab_financier", color_continuous_scale=[PALETTE["border"], PALETTE["navy"]])
fig3 = themed_layout(fig3, height=380, legend=False)
fig3.update_layout(coloraxis_showscale=False, xaxis_title=None, yaxis_title="Agents MM / établissement")
st.plotly_chart(fig3, width="stretch")
st.markdown(
    f'<div class="insight-tag">📌 LECTURE</div><div style="color:{PALETTE["muted"]}; font-size:0.88rem;">'
    "Un ratio élevé confirme que le mobile money couvre un territoire bien plus large que le réseau bancaire "
    "classique — c'est la porte d'entrée dominante vers les services financiers.</div>",
    unsafe_allow_html=True,
)
card_close()

st.write("")
page_header("TERRITOIRES", "Préfectures desservies uniquement par le mobile money", None)

mm_only = get_mm_only_prefectures()
card_open()
if mm_only:
    st.warning(f"**{len(mm_only)} préfectures** n'ont aucun établissement financier référencé mais disposent d'agents mobile money :")
    st.write(", ".join(mm_only))
else:
    st.success("Toutes les préfectures avec agents mobile money ont aussi au moins un établissement financier.")
card_close()

st.caption("Sources : agents mobile money et établissements financiers géolocalisés, opendata.gouv.tg.")
