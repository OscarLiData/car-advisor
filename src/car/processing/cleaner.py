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

    df = df[columns]

    numeric_cols = [
        "fuel_consumption_l_100km",
        "electric_range_km",
        "max_power_kw",
        "vehicle_weight_kg",
    ]

    df[numeric_cols] = df[numeric_cols].fillna(0)

    # ratio puissance / poids
    df["power_weight_ratio"] = (
        df["max_power_kw"] /
        df["vehicle_weight_kg"].replace(0, pd.NA)
    )

    df["brand"] = df["brand"].str.upper()
    df["energy"] = df["energy"].str.lower()
    df["body_type"] = df["body_type"].str.lower()

    df = df.reset_index(drop=True)

    # sauvegarde
    CLEAN_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEAN_PATH, index=False)

    print("Dataset cleaned and saved:", CLEAN_PATH)

    return df