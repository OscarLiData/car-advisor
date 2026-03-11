import pandas as pd
from car.services.recommendation_service import recommend_vehicle


def test_recommend_vehicle():

    df = pd.DataFrame({
        "vehicle_price_eur":[20000,25000],
        "energy":["electric","electric"],
        "body_type":["berline","berline"],
        "co2_mixed_g_km":[0,0],
        "fuel_consumption_l_100km":[0,0],
        "max_power_kw":[100,120]
    })

    result = recommend_vehicle(df,budget=30000)

    assert not result.empty