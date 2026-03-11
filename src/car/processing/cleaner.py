import pandas as pd
from pathlib import Path

CLEAN_PATH = Path("data/processed/cars_clean.csv")


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:

    df = df.rename(columns={
        "Marque": "brand",
        "Libellé modèle": "model",
        "Carrosserie": "body_type",
        "Energie": "energy",
        "Prix véhicule": "vehicle_price_eur",
        "CO2 vitesse mixte Max": "co2_mixed_g_km",
        "Conso vitesse mixte Max": "fuel_consumption_l_100km",
        "Autonomie elec Max": "electric_range_km",
        "Puissance maximale": "max_power_kw",
        "Poids à vide": "vehicle_weight_kg",
        "Bonus-Malus": "eco_bonus_malus_eur",
    })

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

    numeric_cols = [
        "fuel_consumption_l_100km",
        "electric_range_km",
        "max_power_kw",
        "vehicle_weight_kg",
    ]

    existing_numeric = [c for c in numeric_cols if c in df.columns]

    if existing_numeric:
        df[existing_numeric] = df[existing_numeric].fillna(0)

    # supprimer les lignes avec brand manquant
    if "brand" in df.columns:
        df = df.dropna(subset=["brand"])

    # ratio puissance / poids
    if {"max_power_kw", "vehicle_weight_kg"}.issubset(df.columns):
        df["power_weight_ratio"] = (
            df["max_power_kw"] /
            df["vehicle_weight_kg"].replace(0, pd.NA)
        )

    if "brand" in df.columns:
        df["brand"] = df["brand"].str.upper()

    if "energy" in df.columns:
        df["energy"] = df["energy"].str.lower()

    if "body_type" in df.columns:
        df["body_type"] = df["body_type"].str.lower()

    df = df.reset_index(drop=True)

    CLEAN_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEAN_PATH, index=False)

    print("Dataset cleaned and saved:", CLEAN_PATH)

    return df