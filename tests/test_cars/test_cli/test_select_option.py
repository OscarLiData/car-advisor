import pandas as pd
from car.cli.menus import select_option


def test_select_option_returns_correct_option(monkeypatch):

    df = pd.DataFrame({
        "energy": ["electric", "diesel"]
    })

    options = ["electric", "diesel"]

    monkeypatch.setattr("builtins.input", lambda _: "1")

    result = select_option(df, "energy", options, "energy")

    assert result == "electric"