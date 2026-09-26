import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))
from components.theme import card_close, card_open, page_header  # noqa: E402
from config import PALETTE  # noqa: E402
from metrics import get_mm_only_prefectures, get_priority_region  # noqa: E402

BASE = Path(__file__).resolve().parent

page_header("INSIGHTS & PISTES D'ACTION", "Ce que montrent les données", "Constats tirés des analyses précédentes — pas des affirmations scientifiques, mais des pistes à documenter davantage.")

priority = get_priority_region()
mm_only = get_mm_only_prefectures()


def insight_card(num, title, text, figure=None, figure_label=None, link_page=None, link_label=None):
    card_open()
    st.markdown(f'<div class="insight-tag">INSIGHT {num}</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-family:Newsreader,serif; font-weight:600; font-size:1.2rem; color:{PALETTE["navy"]}; margin-bottom:0.4rem;">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="color:{PALETTE["muted"]}; font-size:0.92rem; line-height:1.5; margin-bottom:0.8rem;">{text}</div>', unsafe_allow_html=True)
    if figure:
        st.markdown(f'<div class="insight-figure">{figure}</div><div style="color:{PALETTE["muted"]}; font-size:0.8rem; margin-bottom:0.8rem;">{figure_label}</div>', unsafe_allow_html=True)
    if link_page:
        st.page_link(link_page, label=link_label, icon="→")
    card_close()
    st.write("")


insight_card(
    "01", "Accès aux services financiers",
    "Les données montrent des écarts importants entre les régions concernant le nombre d'habitants par "
    f"point de service. <b>{priority['region']}</b> cumule le ratio le plus défavorable — un déploiement "
    "ciblé d'agents mobile money y aurait l'impact marginal le plus élevé.",
    figure=f"{priority['habitants_par_etab_financier']:,.0f}".replace(",", " "),
    figure_label=f"habitants / établissement financier — {priority['region']}",
    link_page=str(BASE / "finance.py"), link_label="Voir l'inclusion financière",
)

insight_card(
    "02", "Le mobile money, porte d'entrée dominante",
    "Le réseau mobile money représente un nombre de points d'accès beaucoup plus important que le réseau "
    f"financier classique. {len(mm_only)} préfectures ne disposent d'aucun établissement financier référencé "
    "mais sont desservies par des agents mobile money — c'est leur seul point d'accès recensé.",
    figure=str(len(mm_only)),
    figure_label="préfectures desservies uniquement par le mobile money",
    link_page=str(BASE / "cartographie.py"), link_label="Explorer la cartographie",
)

insight_card(
    "03", "Publier les données de couverture réseau",
    "Aucune donnée ouverte de couverture réseau mobile (2G/3G/4G) par zone n'existe aujourd'hui pour le "
    "Togo. Leur publication par l'Agence Togo Digital permettrait un ciblage géographique fin des "
    "investissements en infrastructure — c'est une limite méthodologique de cette analyse, pas un résultat.",
)

insight_card(
    "04", "Encourager le multi-opérateur",
    "Une part significative des points mobile money n'opère qu'avec un seul opérateur. Favoriser le "
    "multi-opérateur réduirait la dépendance des usagers et renforcerait la résilience du service dans "
    "les zones les moins densément couvertes.",
    link_page=str(BASE / "cartographie.py"), link_label="Voir la répartition par opérateur",
)

insight_card(
    "05", "Suivre le ratio agents MM / établissements financiers",
    "Un indicateur simple et déjà disponible pour mesurer chaque année la progression de l'inclusion "
    "financière portée par le mobile money plutôt que par le secteur bancaire traditionnel.",
    link_page=str(BASE / "finance.py"), link_label="Voir le ratio par région",
)

st.caption("Insights formulés à partir des analyses présentées dans les autres vues de cette plateforme.")
