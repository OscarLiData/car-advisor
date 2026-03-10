def filter_by_budget(df, max_price):

    return df[df["vehicle_price_eur"] <= max_price]