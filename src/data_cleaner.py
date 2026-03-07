import pandas as pd

# Paths
RAW_DATA_PATH = "data/processed/cars_eng.csv"
PROCESSED_DATA_PATH = "data/processed/cars_clean.csv"


def clean_dataset():

    # Load dataset
    df = pd.read_csv(RAW_DATA_PATH, sep=";", encoding="utf-8")

    # Rename columns to snake_case
    column_mapping = {
        "Brand": "brand",
        "Model": "model",
        "Car body": "body_type",
        "Energy": "energy",
        "Vehicle price": "vehicle_price_eur",
        "CO2 mixed speed Max": "co2_mixed_g_km",
        "Maximum electricity consumption": "electric_consumption_kwh_100km",
        "Maximum electrical autonomy": "electric_range_km",
        "maximal power": "max_power_kw",
        "Empty weight": "vehicle_weight_kg",
        "Power-to-weight ratio": "power_weight_ratio",
        "Bonus-Malus": "eco_bonus_malus_eur"
    }

    df = df.rename(columns=column_mapping)

    # Create fuel consumption variable (average)
    df["fuel_consumption_l_100km"] = (
        df["Fuel consumption at mixed speed Min"]
        + df["Fuel consumption at mixed speeds Max"]
    ) / 2

    # Select relevant variables
    selected_columns = [
        "brand",
        "model",
        "body_type",
        "energy",
        "vehicle_price_eur",
        "co2_mixed_g_km",
        "fuel_consumption_l_100km",
        "electric_consumption_kwh_100km",
        "electric_range_km",
        "max_power_kw",
        "vehicle_weight_kg",
        "power_weight_ratio",
        "eco_bonus_malus_eur"
    ]

    df_clean = df.filter(items=selected_columns)

    # Remove missing values
    df_clean = df_clean.dropna()

    # Save cleaned dataset
    df_clean.to_csv(PROCESSED_DATA_PATH, index=False)

    print("Clean dataset successfully saved:", PROCESSED_DATA_PATH)