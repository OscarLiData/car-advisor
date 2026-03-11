import pandas as pd
from car.filters.budget_filter import filter_by_budget


def test_budget_filter():
    
    df = pd.DataFrame({
        "vehicle_price_eur": [10000, 20000, 30000]
    })

    result = filter_by_budget(df, 20000)

    assert len(result) == 2