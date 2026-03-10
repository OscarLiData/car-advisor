def compute_global_statistics(df):

    stats = {
        "number_of_vehicles": len(df),
        "average_price": df["vehicle_price_eur"].mean(),
        "average_co2": df["co2_mixed_g_km"].mean(),
        "average_consumption": df["fuel_consumption_l_100km"].mean(),
    }

    return stats