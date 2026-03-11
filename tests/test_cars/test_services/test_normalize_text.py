from car.services.comparison_service import normalize_text


def test_normalize_text():

    text = normalize_text(" Renault ")

    assert text == "renault"