import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils import DATA, load_csv  # noqa: E402

st.set_page_config(page_title="Recommandations", page_icon="🎯", layout="wide")
st.title("🎯 Recommandations stratégiques")

synth = load_csv(DATA / "synthese_region.csv")
region_prioritaire = synth.sort_values("habitants_par_etab_financier", ascending=False).iloc[0]["region"]

st.markdown(f"""
### 1. Prioriser **{region_prioritaire}** pour l'extension de l'accès financier
C'est la région avec le plus grand nombre d'habitants par établissement financier. Un déploiement
ciblé d'agents mobile money supplémentaires y aurait l'impact marginal le plus élevé par point
de service ajouté.

### 2. Capitaliser sur le mobile money dans les zones sans établissement financier
Les préfectures desservies uniquement par le mobile money (voir page *Inclusion financière*)
devraient être la cible prioritaire de programmes d'éducation financière et d'élargissement de
l'offre de services (épargne, micro-crédit) via les agents existants, plutôt que d'attendre
l'implantation de nouvelles agences bancaires physiques, structurellement coûteuse.

### 3. Accélérer la couverture Internet en dehors des grandes villes
La part de la population utilisant Internet reste sous 40 % à l'échelle nationale. Sans donnée
ouverte de couverture réseau mobile (2G/3G/4G) par zone, il est recommandé que l'Agence Togo
Digital publie ces données pour permettre un ciblage géographique fin des investissements en
infrastructure (limite méthodologique documentée dans ce projet).

### 4. Encourager l'interopérabilité et la concurrence entre opérateurs mobile money
Une part significative des points mobile money n'opère qu'avec un seul opérateur. Favoriser le
multi-opérateur (déjà observé sur une partie du réseau) réduit la dépendance des usagers et
renforce la résilience du service dans les zones les moins densément couvertes.

### 5. Suivre dans le temps le ratio agents mobile money / établissements financiers
Ce ratio, aujourd'hui très supérieur à 1 dans toutes les régions, est un bon indicateur simple à
suivre annuellement pour mesurer la progression de l'inclusion financière portée par le mobile
money plutôt que par le secteur bancaire traditionnel.
""")

st.caption("Recommandations formulées à partir des analyses présentées dans les pages précédentes de ce dashboard.")
