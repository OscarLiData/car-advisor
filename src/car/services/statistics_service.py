def compute_global_statistics(df):

    stats = {
        "number_of_cars": len(df),
    }

    if "price" in df.columns:
        stats["average_price"] = df["price"].mean()

    if "consumption" in df.columns:
        stats["average_consumption"] = df["consumption"].mean()

    if "co2" in df.columns:
        stats["average_co2"] = df["co2"].mean()

    return stats