import pandas as pd
from car.filters.body_filter import filter_by_body


def test_body_filter():

    df = pd.DataFrame({
        "body_type": ["SUV", "sedan", "SUV"]
    })

    result = filter_by_body(df, "SUV")

    assert len(result) == 2