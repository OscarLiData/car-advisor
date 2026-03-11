from car.services.comparison_service import compare_cars


def test_compare_cars_average_price():

    vehicles = [
        {"price": 10000},
        {"price": 20000}
    ]

    result = compare_cars(vehicles)

    assert result["avg_price"] == 15000