import pandas as pd
import unicodedata
from pathlib import Path

CLEAN_PATH = Path("data/processed/cars_clean.csv")


def normalize_columns(columns):

    normalized = []

    for col in columns:

        col = col.strip().lower()
        col = col.replace(" ", "_")

        col = unicodedata.normalize("NFKD", col)
        col = col.encode("ascii", "ignore").decode("utf-8")

        normalized.append(col)

    return normalized


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:

    # Normalisation des colonnes
    df.columns = normalize_columns(df.columns)

    # Mapping des colonnes utiles
    rename_map = {
        "marque": "brand",
        "modele": "model",
        "carrosserie": "body_type",
        "energie": "energy",
        "prix_vehicule": "vehicle_price_eur",
        "co2_vitesse_mixte_max": "co2_mixed_g_km",
        "conso_vitesse_mixte_max": "fuel_consumption_l_100km",
        "autonomie_elec_max": "electric_range_km",
        "puissance_maximale": "max_power_kw",
        "poids_a_vide": "vehicle_weight_kg",
        "bonus-malus": "eco_bonus_malus_eur",
    }

    df = df.rename(columns=rename_map)

    # Colonnes finales
    columns = [
        "brand",
        "model",
        "body_type",
        "energy",
        "vehicle_price_eur",
        "co2_mixed_g_km",
        "fuel_consumption_l_100km",
        "electric_range_km",
        "max_power_kw",
        "vehicle_weight_kg",
        "eco_bonus_malus_eur",
    ]

    df = df[[c for c in columns if c in df.columns]]

    # Conversion numérique
    numeric_cols = [
        "vehicle_price_eur",
        "co2_mixed_g_km",
        "fuel_consumption_l_100km",
        "electric_range_km",
        "max_power_kw",
        "vehicle_weight_kg",
    ]

    existing_numeric = [c for c in numeric_cols if c in df.columns]

    df[existing_numeric] = df[existing_numeric].apply(
        pd.to_numeric,
        errors="coerce"
    )

    # Remplissage valeurs manquantes
    df[existing_numeric] = df[existing_numeric].fillna(0)

    # Suppression lignes invalides
    if "brand" in df.columns:
        df = df.dropna(subset=["brand"])

    # Feature engineering
    if {"max_power_kw", "vehicle_weight_kg"}.issubset(df.columns):

        df["power_weight_ratio"] = (
            df["max_power_kw"] /
            df["vehicle_weight_kg"].replace(0, pd.NA)
        )

    # Normalisation texte
    if "brand" in df.columns:
        df["brand"] = df["brand"].str.upper()

    if "energy" in df.columns:
        df["energy"] = df["energy"].str.lower()

    if "body_type" in df.columns:
        df["body_type"] = df["body_type"].str.lower()

    df = df.reset_index(drop=True)

    # Sauvegarde dataset nettoyé
    CLEAN_PATH.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(CLEAN_PATH, index=False)

    print("Dataset cleaned and saved:", CLEAN_PATH)

    return df