import pandas as pd
from car.services.statistics_service import compute_global_statistics


def test_statistics_service():

    df = pd.DataFrame({
        "vehicle_price_eur": [10000, 20000],
        "co2_mixed_g_km": [100, 120],
        "fuel_consumption_l_100km": [5, 6]
    })

    stats = compute_global_statistics(df)

    assert stats["number_of_vehicles"] == 2