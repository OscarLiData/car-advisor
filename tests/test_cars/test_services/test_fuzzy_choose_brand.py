from car.services.comparison_service import fuzzy_choose_brand


def test_fuzzy_choose_brand(monkeypatch):

    brands = ["Renault", "Peugeot"]

    monkeypatch.setattr("builtins.input", lambda _: "Renault")

    result = fuzzy_choose_brand(brands,"brand")

    assert result == "Renault"