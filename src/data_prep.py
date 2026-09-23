"""
data_prep.py — Nettoyage et préparation des données
Défi 2 Économie Numérique — Togo AI Lab

Lit les CSV bruts dans data/raw/, produit des tables propres dans data/processed/ :
  - population_prefecture.csv       (population par préfecture/région, 2022)
  - telecom_marche.csv              (indicateurs marché télécom, wide format, par année)
  - telecom_internet.csv            (indicateurs internet fixe/mobile, wide format, par année)
  - internet_usage_pct.csv          (% population utilisant Internet, 1996-2022, WorldBank)
  - agents_mobile_money.csv         (points géolocalisés + lat/lon, par préfecture/commune)
  - etablissements_financiers.csv   (points géolocalisés + lat/lon, catégorie normalisée)
  - synthese_prefecture.csv         (table finale : population, nb agents MM, nb étab. financiers,
                                      ratios habitants/point de service par préfecture)
"""

import re
import unicodedata
from pathlib import Path

import pandas as pd

RAW = Path(__file__).resolve().parent.parent / "data" / "raw"
OUT = Path(__file__).resolve().parent.parent / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Utilitaires
# ---------------------------------------------------------------------------

def normalize_text(s):
    """Uppercase, sans accents, espaces normalisés — pour matcher les libellés entre fichiers."""
    if pd.isna(s):
        return s
    s = str(s).strip()
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"\s+", " ", s).upper()
    return s


def extract_lat_lon(geom_series):
    """Extrait (lon, lat) d'une colonne WKT 'POINT (lon lat)'."""
    coords = geom_series.str.extract(r"POINT \(([-\d.]+) ([-\d.]+)\)")
    lon = pd.to_numeric(coords[0], errors="coerce")
    lat = pd.to_numeric(coords[1], errors="coerce")
    return lat, lon


# ---------------------------------------------------------------------------
# 1) Population — le fichier est au niveau canton/localité, on agrège par préfecture
# ---------------------------------------------------------------------------

def prep_population():
    df = pd.read_csv(RAW / "population_2022.csv")
    df.columns = [c.strip() for c in df.columns]
    df = df.rename(columns={"découpage-administratif": "libelle", "Value": "population"})
    df["population"] = pd.to_numeric(df["population"], errors="coerce")

    # Liste des 5 régions + le total pays : à isoler du reste (niveaux canton/préfecture/commune)
    regions = {"TOGO", "SAVANES", "KARA", "CENTRALE", "PLATEAUX", "MARITIME"}
    df["libelle_norm"] = df["libelle"].apply(normalize_text)

    df_national = df[df["libelle_norm"] == "TOGO"][["population"]].assign(niveau="pays")
    df_regions = df[df["libelle_norm"].isin(regions - {"TOGO"})].copy()
    df_regions["niveau"] = "region"

    # Tout le reste = communes/cantons/préfectures mélangés dans le fichier source ;
    # on les garde tels quels comme table de détail, à rapprocher manuellement des préfectures
    # si besoin plus fin. Pour le dashboard, la maille région suffit pour les ratios population.
    df_regions[["libelle", "population"]].to_csv(OUT / "population_regions.csv", index=False)
    df_national[["population"]].to_csv(OUT / "population_togo.csv", index=False)
    return df_regions[["libelle", "population"]]


# ---------------------------------------------------------------------------
# 2) Indicateurs télécom marché (mesqyx) — long -> wide (une colonne par indicateur)
# ---------------------------------------------------------------------------

def prep_telecom_marche():
    df = pd.read_csv(RAW / "telecom_marche.csv")
    df.columns = [c.strip() for c in df.columns]
    df["Date"] = pd.to_numeric(df["Date"], errors="coerce").astype("Int64")
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
    wide = df.pivot_table(index="Date", columns="indicateur", values="Value", aggfunc="first")
    wide = wide.sort_index()
    wide.to_csv(OUT / "telecom_marche.csv")
    return wide


# ---------------------------------------------------------------------------
# 3) Indicateurs internet (cxnvmoc) — long -> wide
# ---------------------------------------------------------------------------

def prep_telecom_internet():
    df = pd.read_csv(RAW / "telecom_internet.csv")
    df.columns = [c.strip() for c in df.columns]
    df["Date"] = pd.to_numeric(df["Date"], errors="coerce").astype("Int64")
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
    wide = df.pivot_table(index="Date", columns="indicateur", values="Value", aggfunc="first")
    wide = wide.sort_index()
    wide.to_csv(OUT / "telecom_internet.csv")
    return wide


# ---------------------------------------------------------------------------
# 4) % population utilisant Internet (Banque Mondiale, 1996-2022)
# ---------------------------------------------------------------------------

def prep_internet_usage():
    df = pd.read_csv(RAW / "internet_usage_pct.csv")
    df = df[["date", "value"]].rename(columns={"date": "annee", "value": "pct_population"})
    df = df.dropna(subset=["pct_population"]).sort_values("annee")
    df.to_csv(OUT / "internet_usage_pct.csv", index=False)
    return df


# ---------------------------------------------------------------------------
# 5) Agents mobile money — géolocalisation + nettoyage opérateur
# ---------------------------------------------------------------------------

def prep_agents_mm():
    df = pd.read_csv(RAW / "agents_mobile_money.csv")
    df.columns = [c.strip() for c in df.columns]
    df["lat"], df["lon"] = extract_lat_lon(df["geometry"])

    # Correction connue (héritée du Défi 1) : faute de frappe préfecture
    df["prefecture_nom_bdd"] = df["prefecture_nom_bdd"].replace(
        {"Tandjoaré": "Tandjouaré"}
    )

    # Normalise le champ opérateur (garde la donnée mais expose un flag multi-opérateur)
    df["operateur"] = df["operateur"].fillna("Nsp")
    df["multi_operateur"] = df["operateur"].str.contains(",")

    df = df.dropna(subset=["lat", "lon"])
    keep = [
        "region_nom_bdd", "prefecture_nom_bdd", "commune_nom_bdd", "canton_nom_bdd",
        "operateur", "multi_operateur", "lat", "lon",
    ]
    df = df[keep].rename(columns={
        "region_nom_bdd": "region",
        "prefecture_nom_bdd": "prefecture",
        "commune_nom_bdd": "commune",
        "canton_nom_bdd": "canton",
    })
    df.to_csv(OUT / "agents_mobile_money.csv", index=False)
    return df


# ---------------------------------------------------------------------------
# 6) Établissements financiers — géolocalisation + catégorie normalisée + statut d'usage
# ---------------------------------------------------------------------------

def prep_etablissements():
    df = pd.read_csv(RAW / "etablissements_financiers.csv")
    df.columns = [c.strip() for c in df.columns]
    df["lat"], df["lon"] = extract_lat_lon(df["geometry"])

    # Normalise les doublons de libellé (ex : "Micro-Finace" vs "Micro-Finance")
    df["activite_categorie"] = df["activite_categorie"].replace({"Micro-Finace": "Micro-Finance"})

    # Normalise le statut d'usage en 3 classes : Actif / Inactif / Inconnu
    statut_map = {
        "Utilisé": "Actif", "Utilise": "Actif", "Location ": "Actif", "Location": "Actif",
        "Fermé": "Inactif", "Abandonné": "Inactif", "Inacheve": "Inactif",
        "Sans Local": "Inactif", "Néant": "Inactif", "En construction": "Inactif",
        "En réfection": "Inactif",
    }
    df["statut_simplifie"] = df["activite_statut"].map(statut_map).fillna("Inconnu")

    df = df.dropna(subset=["lat", "lon"])
    keep = [
        "region_nom_bdd", "prefecture_nom_bdd", "commune_nom_bdd", "canton_nom_bdd",
        "etab_nom", "activite_categorie", "statut_simplifie", "lat", "lon",
    ]
    df = df[keep].rename(columns={
        "region_nom_bdd": "region",
        "prefecture_nom_bdd": "prefecture",
        "commune_nom_bdd": "commune",
        "canton_nom_bdd": "canton",
        "activite_categorie": "categorie",
    })
    df.to_csv(OUT / "etablissements_financiers.csv", index=False)
    return df


# ---------------------------------------------------------------------------
# 7) Synthèse par région : population, offre de services, ratios d'inclusion
# ---------------------------------------------------------------------------

def build_synthese(pop_regions, agents, etabs):
    pop = pop_regions.copy()
    pop["region_norm"] = pop["libelle"].apply(normalize_text)

    agg_agents = agents.groupby("region").size().rename("nb_agents_mm").reset_index()
    agg_agents["region_norm"] = agg_agents["region"].apply(normalize_text)

    agg_etabs = (
        etabs[etabs["statut_simplifie"] == "Actif"]
        .groupby("region").size().rename("nb_etab_financiers_actifs").reset_index()
    )
    agg_etabs["region_norm"] = agg_etabs["region"].apply(normalize_text)

    synth = pop.merge(agg_agents[["region_norm", "nb_agents_mm"]], on="region_norm", how="left")
    synth = synth.merge(agg_etabs[["region_norm", "nb_etab_financiers_actifs"]], on="region_norm", how="left")
    synth[["nb_agents_mm", "nb_etab_financiers_actifs"]] = synth[
        ["nb_agents_mm", "nb_etab_financiers_actifs"]
    ].fillna(0)

    synth["habitants_par_agent_mm"] = (synth["population"] / synth["nb_agents_mm"]).round(0)
    synth["habitants_par_etab_financier"] = (
        synth["population"] / synth["nb_etab_financiers_actifs"]
    ).round(0)
    synth["agents_mm_par_etab_financier"] = (
        synth["nb_agents_mm"] / synth["nb_etab_financiers_actifs"]
    ).round(1)

    synth = synth[[
        "libelle", "population", "nb_agents_mm", "nb_etab_financiers_actifs",
        "habitants_par_agent_mm", "habitants_par_etab_financier", "agents_mm_par_etab_financier",
    ]].rename(columns={"libelle": "region"})

    synth.to_csv(OUT / "synthese_region.csv", index=False)
    return synth


def run_all():
    print("→ Population...")
    pop_regions = prep_population()
    print("→ Marché télécom...")
    prep_telecom_marche()
    print("→ Internet (abonnés)...")
    prep_telecom_internet()
    print("→ Internet (% population, Banque Mondiale)...")
    prep_internet_usage()
    print("→ Agents mobile money...")
    agents = prep_agents_mm()
    print("→ Établissements financiers...")
    etabs = prep_etablissements()
    print("→ Synthèse régionale...")
    synth = build_synthese(pop_regions, agents, etabs)
    print("Terminé. Fichiers écrits dans:", OUT)
    print(synth)


if __name__ == "__main__":
    run_all()
