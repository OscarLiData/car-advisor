"""
Tests complémentaires pour comparison_service.py.

On mocke input() pour tester les fonctions interactives sans intervention
humaine. Les fonctions avec I/O (fuzzy_choose_brand, ask_main_menu_choice,
ask_continue_choice, main) sont testées via unittest.mock.patch.
"""

from unittest.mock import patch, call
import pytest
from car.services.comparison_service import (
    Vehicule,
    compare_cars,
    fuzzy_choose_brand,
    ask_main_menu_choice,
    ask_continue_choice,
    main,
    load_cars,
    DATA_FILE,
)


# ---------------------------------------------------------------------------
# Helpers
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


BRANDS = ["RENAULT", "TOYOTA", "TESLA"]


# ---------------------------------------------------------------------------
# compare_cars — cas supplémentaires
# ---------------------------------------------------------------------------


def test_compare_cars_with_vehicule_objects():
    """compare_cars fonctionne aussi avec des objets Vehicule (getattr)."""
    vehicles = [_make_vehicule(price=10000.0), _make_vehicule(price=30000.0)]
    result = compare_cars(vehicles)
    assert result["avg_price"] == pytest.approx(20000.0)


def test_compare_cars_ignores_none_prices():
    """Les prix None sont ignorés dans le calcul de la moyenne."""
    vehicles = [{"price": None}, {"price": 20000}]
    result = compare_cars(vehicles)
    assert result["avg_price"] == pytest.approx(20000.0)


def test_compare_cars_all_none_prices():
    """Si tous les prix sont None, avg_price vaut None."""
    vehicles = [{"price": None}]
    result = compare_cars(vehicles)
    assert result["avg_price"] is None


# ---------------------------------------------------------------------------
# fuzzy_choose_brand
# ---------------------------------------------------------------------------


def test_fuzzy_choose_brand_exact_match():
    """Saisie exacte (insensible à la casse) retourne la marque."""
    with patch("builtins.input", return_value="renault"):
        result = fuzzy_choose_brand(BRANDS, "brand")
    assert result == "RENAULT"


def test_fuzzy_choose_brand_fuzzy_match():
    """Saisie approximative retourne la marque la plus proche."""
    with patch("builtins.input", return_value="renult"):
        result = fuzzy_choose_brand(BRANDS, "brand")
    assert result == "RENAULT"


def test_fuzzy_choose_brand_exit_returns_empty():
    """Saisie 'exit' retourne une chaîne vide."""
    with patch("builtins.input", return_value="exit"):
        result = fuzzy_choose_brand(BRANDS, "brand")
    assert result == ""


def test_fuzzy_choose_brand_quit_returns_empty():
    """Saisie 'quit' retourne une chaîne vide."""
    with patch("builtins.input", return_value="quit"):
        result = fuzzy_choose_brand(BRANDS, "brand")
    assert result == ""


def test_fuzzy_choose_brand_unknown_then_exit(capsys):
    """Saisie inconnue affiche un message, puis exit à la 2e tentative."""
    with patch("builtins.input", side_effect=["zzzzzzz", "exit"]):
        result = fuzzy_choose_brand(BRANDS, "brand")
    assert result == ""
    captured = capsys.readouterr()
    assert "Unknown brand" in captured.out


# ---------------------------------------------------------------------------
# ask_main_menu_choice
# ---------------------------------------------------------------------------


def test_ask_main_menu_choice_valid_options():
    """Chaque option valide (0-3) est acceptée directement."""
    for option in ["0", "1", "2", "3"]:
        with patch("builtins.input", return_value=option):
            assert ask_main_menu_choice() == option


def test_ask_main_menu_choice_invalid_then_valid(capsys):
    """Une saisie invalide affiche un message puis redemande."""
    with patch("builtins.input", side_effect=["9", "1"]):
        result = ask_main_menu_choice()
    assert result == "1"
    assert "Invalid" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# ask_continue_choice
# ---------------------------------------------------------------------------


def test_ask_continue_choice_back_to_menu():
    with patch("builtins.input", return_value="1"):
        assert ask_continue_choice() == "1"


def test_ask_continue_choice_quit():
    with patch("builtins.input", return_value="0"):
        assert ask_continue_choice() == "0"


def test_ask_continue_choice_invalid_then_valid(capsys):
    with patch("builtins.input", side_effect=["5", "0"]):
        result = ask_continue_choice()
    assert result == "0"
    assert "Invalid" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# main()
# ---------------------------------------------------------------------------


def test_main_quit_immediately(tmp_path):
    """Option 0 au menu principal : on quitte sans rien faire."""
    csv_file = tmp_path / "cars_clean.csv"
    _write_csv(csv_file)

    with patch("car.services.comparison_service.DATA_FILE", csv_file), \
         patch("builtins.input", side_effect=["0"]):
        main()  # ne doit pas lever d'exception


def test_main_list_vehicles_then_quit(tmp_path, capsys):
    """Option 1 : affiche les marques, puis quitte."""
    csv_file = tmp_path / "cars_clean.csv"
    _write_csv(csv_file)

    with patch("car.services.comparison_service.DATA_FILE", csv_file), \
         patch("builtins.input", side_effect=["1", "0"]):
        main()

    assert "RENAULT" in capsys.readouterr().out


def test_main_compare_one_brand_then_quit(tmp_path, capsys):
    """Option 2 : filtre par marque, affiche le nombre de véhicules, quitte."""
    csv_file = tmp_path / "cars_clean.csv"
    _write_csv(csv_file)

    with patch("car.services.comparison_service.DATA_FILE", csv_file), \
         patch("builtins.input", side_effect=["2", "RENAULT", "0"]):
        main()

    assert "1 vehicles" in capsys.readouterr().out


def test_main_compare_two_brands_then_quit(tmp_path, capsys):
    """Option 3 : compare deux marques, affiche les comptages, quitte."""
    csv_file = tmp_path / "cars_clean.csv"
    _write_csv(csv_file)

    with patch("car.services.comparison_service.DATA_FILE", csv_file), \
         patch("builtins.input", side_effect=["3", "RENAULT", "TOYOTA", "0"]):
        main()

    out = capsys.readouterr().out
    assert "RENAULT" in out
    assert "TOYOTA" in out


def test_main_file_not_found():
    """Lève FileNotFoundError si le CSV est absent."""
    from pathlib import Path
    with patch("car.services.comparison_service.DATA_FILE", Path("/nonexistent/path.csv")):
        with pytest.raises(FileNotFoundError):
            main()


# ---------------------------------------------------------------------------
# Helpers CSV
# ---------------------------------------------------------------------------


def _write_csv(path):
    import csv
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "brand", "model", "body_type", "energy",
            "vehicle_price_eur", "fuel_consumption_l_100km",
            "co2_mixed_g_km", "max_power_kw", "vehicle_weight_kg",
        ])
        writer.writerow(["RENAULT", "Clio", "berline", "gazole", 18000, 4.2, 95, 66, 1180])
        writer.writerow(["TOYOTA", "Yaris", "berline", "essence", 15000, 5.5, 110, 72, 1050])
