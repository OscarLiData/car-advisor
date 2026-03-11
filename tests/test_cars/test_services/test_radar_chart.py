import pandas as pd
from car.services.visualization_service import radar_chart


def test_radar_chart_returns_figure():

    df = pd.DataFrame({
        "model":["A"],
        "vehicle_price_eur":[20000],
        "co2_mixed_g_km":[100],
        "fuel_consumption_l_100km":[5],
        "max_power_kw":[100]
    })

    fig = radar_chart(df)

    assert fig is not None