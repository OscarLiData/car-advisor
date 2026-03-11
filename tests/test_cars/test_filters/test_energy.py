import pandas as pd
from car.filters.energy_filter import filter_by_energy


def test_energy_filter():

    df = pd.DataFrame({
        "energy": ["elec", "gazole", "elec"]
    })

    result = filter_by_energy(df, "electric")

    assert len(result) == 2