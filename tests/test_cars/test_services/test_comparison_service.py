from car.services.comparison_service import compare_vehicules


def test_compare_vehicules_price():

    v1 = {"price": 20000}
    v2 = {"price": 35000}

    result = compare_vehicules([v1, v2])

    assert result["avg_price"] == 27500