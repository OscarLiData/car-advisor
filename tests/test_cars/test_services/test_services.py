import pytest
import pandas as pd
from car.services.recommendation_service import recommend_vehicle
from car.services.statistics_service import compute_global_statistics
from car.services.comparison_service import (
    Vehicule,
    compare_cars,
    get_available_brands,
    filter_cars_by_brand,
    normalize_text,
    display_brand_list_with_counts,
    load_cars,
)
import csv


# ---------------------------------------------------------------------------
# recommendation_service
# ---------------------------------------------------------------------------


def test_recommend_vehicle_returns_nonempty(sample_df):
    result = recommend_vehicle(sample_df, budget=50000)
    assert not result.empty


def test_recommend_vehicle_respects_budget(sample_df):
    result = recommend_vehicle(sample_df, budget=20000)
    assert (result["vehicle_price_eur"] <= 20000).all()


def test_recommend_vehicle_respects_energy(sample_df):
    result = recommend_vehicle(sample_df, energy="electric")
    assert result["energy"].str.contains("elec").all()


def test_recommend_vehicle_has_score_column(sample_df):
    result = recommend_vehicle(sample_df, budget=50000)
    assert "score" in result.columns


def test_recommend_vehicle_empty_when_no_match(sample_df):
    result = recommend_vehicle(sample_df, budget=1)
    assert result.empty


def test_recommend_vehicle_score_between_0_and_1(sample_df):
    result = recommend_vehicle(sample_df, budget=50000)
    assert (result["score"] >= 0).all()
    assert (result["score"] <= 1).all()


# ---------------------------------------------------------------------------
# statistics_service
# ---------------------------------------------------------------------------


def test_compute_global_statistics_vehicle_count(sample_df):
    stats = compute_global_statistics(sample_df)
    assert stats["number_of_vehicles"] == len(sample_df)


def test_compute_global_statistics_average_price(sample_df):
    stats = compute_global_statistics(sample_df)
    expected = sample_df["vehicle_price_eur"].mean()
    assert stats["average_price"] == pytest.approx(expected)


def test_compute_global_statistics_average_co2(sample_df):
    stats = compute_global_statistics(sample_df)
    expected = sample_df["co2_mixed_g_km"].mean()
    assert stats["average_co2"] == pytest.approx(expected)


# ---------------------------------------------------------------------------
# comparison_service — Vehicule dataclass
# ---------------------------------------------------------------------------


def _make_vehicule(brand="RENAULT", model="Clio", price=18000.0) -> Vehicule:
    return Vehicule(
        brand=brand,
        model=model,
        body_type="berline",
        energy="gazole",
        price=price,
        fuel_consumption=4.2,
        co2=95.0,
        power_kw=66.0,
        weight_kg=1180.0,
    )


def test_compare_cars_average_price():
    vehicles = [{"price": 10000}, {"price": 20000}]
    result = compare_cars(vehicles)
    assert result["avg_price"] == 15000.0


def test_compare_cars_empty_returns_empty_dict():
    assert compare_cars([]) == {}


def test_get_available_brands_sorted():
    vehicles = [_make_vehicule("TOYOTA"), _make_vehicule("RENAULT")]
    brands = get_available_brands(vehicles)
    assert brands == ["RENAULT", "TOYOTA"]


def test_filter_cars_by_brand():
    vehicles = [_make_vehicule("RENAULT"), _make_vehicule("TOYOTA")]
    result = filter_cars_by_brand(vehicles, "RENAULT")
    assert len(result) == 1
    assert result[0].brand == "RENAULT"


def test_normalize_text():
    assert normalize_text("  TOYOTA  ") == "toyota"


def test_display_brand_list_with_counts_output(capsys):
    vehicles = [_make_vehicule("RENAULT", "Clio"), _make_vehicule("RENAULT", "Zoe")]
    display_brand_list_with_counts(vehicles)
    captured = capsys.readouterr()
    assert "RENAULT" in captured.out
    assert "2" in captured.out


def test_load_cars_from_csv(tmp_path):
    file = tmp_path / "cars.csv"
    with open(file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "brand", "model", "body_type", "energy",
            "vehicle_price_eur", "fuel_consumption_l_100km",
            "co2_mixed_g_km", "max_power_kw", "vehicle_weight_kg",
        ])
        writer.writerow(["RENAULT", "Clio", "berline", "gazole", 18000, 4.2, 95, 66, 1180])
    cars = load_cars(file)
    assert len(cars) == 1
    assert cars[0].brand == "RENAULT"
