# TOGO DIGITAL INSIGHT — Défi 2 Économie Numérique (Togo AI Lab)

Observatoire de l'adoption du numérique et du rôle du mobile money dans l'inclusion financière au Togo.

## Structure

```
data/raw/          CSV bruts (population, télécom, finance, mobile money, internet)
data/processed/     Sorties nettoyées de src/data_prep.py
src/data_prep.py    Pipeline de nettoyage et d'agrégation
report/             Génération du rapport PowerPoint (10 slides)

app/
├── Home.py          Point d'entrée : configuration + navigation groupée (st.navigation)
├── config.py         Palette et identité de l'application
├── data_loader.py    Chargement centralisé et mis en cache des données
├── metrics.py         Indicateurs agrégés réutilisés par plusieurs vues
├── components/        Briques UI réutilisables (thème, KPI, graphiques, filtres)
│   ├── theme.py
│   ├── kpi.py
│   ├── charts.py
│   └── filters.py
└── views/              Une page par fichier, orchestrées par Home.py
    ├── accueil.py       Vue d'ensemble (hero + KPI + aperçu régional)
    ├── internet.py
    ├── telecom.py
    ├── cartographie.py
    ├── finance.py        Inclusion financière (graphiques + lecture guidée)
    └── insights.py        Constats liés aux données, avec liens vers le détail
```

## Installation

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Utilisation

1. **Préparer les données** (à relancer si les CSV bruts changent) :
   ```bash
   python src/data_prep.py
   ```

2. **Lancer le dashboard** :
   ```bash
   streamlit run app/Home.py
   ```
   Navigation groupée dans la sidebar : Vue d'ensemble · Données (Internet, Télécoms,
   Inclusion financière) · Explorer (Cartographie, Insights).

3. **Régénérer le rapport PowerPoint** :
   ```bash
   cd report && node build_report.js
   ```
   Produit `report/Defi2_Economie_Numerique_Togo.pptx` (10 slides).

## Livrables du challenge

- Tableau de bord interactif → zippé depuis `app/` + `data/processed/` + `requirements.txt`
- Rapport PowerPoint → `report/Defi2_Economie_Numerique_Togo.pptx`

## Limites connues

- Aucune donnée ouverte de couverture réseau mobile (2G/3G/4G) par zone.
- Le fichier population 2022 est au niveau canton ; l'agrégation région a été
  reconstituée par correspondance de libellés normalisés.
- Le statut d'usage des établissements financiers est déclaratif (janvier 2025).

