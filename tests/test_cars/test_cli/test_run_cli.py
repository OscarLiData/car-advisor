import pandas as pd
from car.cli.menus import run_cli


def test_run_cli_exit(monkeypatch):

    df = pd.DataFrame({
        "vehicle_price_eur": [10000],
        "energy": ["electric"],
        "body_type": ["SUV"]
    })

    inputs = iter(["3"])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    run_cli(df)