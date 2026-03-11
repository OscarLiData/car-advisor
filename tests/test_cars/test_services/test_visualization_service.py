import pandas as pd
from car.services.visualization_service import radar_chart


def test_radar_chart_returns_figure():

    df = pd.DataFrame(
        {
            "model": ["A", "B"],
            "vehicle_price_eur": [20000, 30000],
            "co2_mixed_g_km": [120, 100],
            "fuel_consumption_l_100km": [5.5, 6.0],
            "max_power_kw": [100, 120],
        }
    )

    fig = radar_chart(df)

    assert fig is not None


def test_radar_chart_empty_df():

    df = pd.DataFrame()

    import pytest

    with pytest.raises(ValueError):
        radar_chart(df)