import csv
from pathlib import Path
from car.services.comparison_service import load_cars


def test_load_cars(tmp_path):

    file = tmp_path / "cars.csv"

    with open(file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "brand","model","body_type","energy",
            "vehicle_price_eur","fuel_consumption_l_100km",
            "co2_mixed_g_km","max_power_kw","vehicle_weight_kg"
        ])
        writer.writerow(["Renault","Clio","hatch","gas",20000,5,100,80,1200])

    cars = load_cars(file)

    assert len(cars) == 1