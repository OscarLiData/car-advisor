import pandas as pd
from car.services.recommendation_service import recommend_vehicle


def test_zero_weights():

    data = {
        "brand": ["A", "B"],
        "model": ["X", "Y"],
        "vehicle_price_eur": [20000, 25000],
        "energy": ["electric", "electric"],
        "body_type": ["berline", "berline"],
        "co2_mixed_g_km": [0, 0],
        "fuel_consumption_l_100km": [0, 0],
        "max_power_kw": [100, 120],
    }

    df = pd.DataFrame(data)

    results = recommend_vehicle(
        df,
        budget=30000,
        energy="electric",
        body="berline",
        w_price=0,
        w_co2=0,
        w_consumption=0,
        w_power=0,
    )

    assert not results["score"].isna().any()