"""Indicateurs agrégés — calculés une fois, réutilisés par les vues et les KPI."""

from data_loader import (
    load_agents_mm,
    load_etablissements,
    load_internet_usage,
    load_population_togo,
    load_synthese_region,
)


def get_total_population():
    return int(load_population_togo()["population"].iloc[0])


def get_internet_rate():
    """Retourne (pourcentage, année) de la dernière valeur disponible."""
    df = load_internet_usage()
    last = df.iloc[-1]
    return float(last["pct_population"]), int(last["annee"])


def get_internet_progress(years_back=3):
    """Progression en points entre la dernière valeur et celle ~years_back plus tôt."""
    df = load_internet_usage()
    last = df.iloc[-1]
    prior_candidates = df[df["annee"] <= last["annee"] - years_back]
    if prior_candidates.empty:
        return None
    prior = prior_candidates.iloc[-1]
    return round(last["pct_population"] - prior["pct_population"], 1)


def get_total_agents():
    return int(load_synthese_region()["nb_agents_mm"].sum())


def get_total_financial_institutions():
    return int(load_synthese_region()["nb_etab_financiers_actifs"].sum())


def get_regional_metrics():
    return load_synthese_region()


def get_n_regions():
    return load_synthese_region()["region"].nunique()


def get_priority_region():
    """Région avec le ratio habitants/établissement le plus défavorable."""
    synth = get_regional_metrics()
    return synth.sort_values("habitants_par_etab_financier", ascending=False).iloc[0]


def get_mm_only_prefectures():
    """Préfectures desservies uniquement par le mobile money (pas d'établissement financier)."""
    agents = load_agents_mm()
    etabs = load_etablissements()
    pref_agents = set(agents["prefecture"].dropna().unique())
    pref_etabs = set(etabs["prefecture"].dropna().unique())
    return sorted(pref_agents - pref_etabs)
