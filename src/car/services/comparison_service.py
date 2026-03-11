from __future__ import annotations

import csv
import difflib
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from statistics import mean


DATA_FILE = Path("data/processed/cars_clean.csv")


@dataclass
class Vehicule:
    brand: str
    model: str
    body_type: str
    energy: str
    price: float
    fuel_consumption: float
    co2: float
    power_kw: float
    weight_kg: float


def compare_cars(vehicules) -> dict:
    """Return basic statistics for a list of vehicles."""

    if not vehicules:
        return {}

    def get(attr, v):
        if isinstance(v, dict):
            return v.get(attr)
        return getattr(v, attr)

    prices = [get("price", v) for v in vehicules if get("price", v) is not None]

    return {
        "avg_price": mean(prices) if prices else None,
    }


def load_cars(data_file: Path) -> list[Vehicule]:

    vehicules = []

    with data_file.open(encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            vehicules.append(
                Vehicule(
                    brand=row["brand"],
                    model=row["model"],
                    body_type=row["body_type"],
                    energy=row["energy"],
                    price=float(row["vehicle_price_eur"]),
                    fuel_consumption=float(row["fuel_consumption_l_100km"]),
                    co2=float(row["co2_mixed_g_km"]),
                    power_kw=float(row["max_power_kw"]),
                    weight_kg=float(row["vehicle_weight_kg"]),
                )
            )

    return vehicules


def get_available_brands(vehicules: list[Vehicule]) -> list[str]:
    return sorted({v.brand for v in vehicules})


def normalize_text(text: str) -> str:
    return text.strip().lower()


def fuzzy_choose_brand(brands: list[str], label: str) -> str:

    print(f"\nSelect {label}:")

    while True:
        user_input = input("Brand: ").strip()

        if user_input.lower() in {"exit", "quit"}:
            return ""

        normalized_input = normalize_text(user_input)

        for brand in brands:
            if normalize_text(brand) == normalized_input:
                return brand

        close_matches = difflib.get_close_matches(
            normalized_input,
            [normalize_text(b) for b in brands],
            n=1,
            cutoff=0.6,
        )

        if close_matches:
            for brand in brands:
                if normalize_text(brand) == close_matches[0]:
                    print(f"Did you mean: {brand}? Selected.")
                    return brand

        print("Unknown brand.")


def ask_main_menu_choice() -> str:

    print("\n===== Main menu =====")
    print("1 - List all vehicles")
    print("2 - Compare one brand")
    print("3 - Compare two brands")
    print("0 - Quit")

    while True:
        choice = input("Your choice: ").strip()

        if choice in {"0", "1", "2", "3"}:
            return choice

        print("Invalid choice.")


def ask_continue_choice() -> str:

    print("\nWhat do you want to do next?")
    print("1 - Back to main menu")
    print("0 - Quit")

    while True:
        choice = input("Your choice: ").strip()

        if choice in {"0", "1"}:
            return choice

        print("Invalid choice.")


def filter_cars_by_brand(vehicules: list[Vehicule], brand: str) -> list[Vehicule]:
    return [v for v in vehicules if v.brand == brand]


def display_brand_list_with_counts(vehicules: list[Vehicule]) -> None:

    brand_to_models: dict[str, set[str]] = defaultdict(set)

    for v in vehicules:
        brand_to_models[v.brand].add(v.model)

    print("\n=== Brand list ===")

    for brand in sorted(brand_to_models):
        print(f"{brand} : {len(brand_to_models[brand])} models")


def main() -> None:

    if not DATA_FILE.exists():
        raise FileNotFoundError(DATA_FILE)

    vehicules = load_vehicules(DATA_FILE)
    brands = get_available_brands(vehicules)

    while True:

        choice = ask_main_menu_choice()

        if choice == "0":
            print("Goodbye!")
            return

        if choice == "1":
            display_brand_list_with_counts(vehicules)

        if choice == "2":

            brand = fuzzy_choose_brand(brands, "brand")

            if brand:
                brand_vehicules = filter_vehicules_by_brand(vehicules, brand)

                print(f"{len(brand_vehicules)} vehicles found.")

        if choice == "3":

            brand1 = fuzzy_choose_brand(brands, "brand 1")
            brand2 = fuzzy_choose_brand(brands, "brand 2")

            if brand1 and brand2:

                vehicules1 = filter_vehicules_by_brand(vehicules, brand1)
                vehicules2 = filter_vehicules_by_brand(vehicules, brand2)

                print(f"{brand1}: {len(vehicules1)} vehicles")
                print(f"{brand2}: {len(vehicules2)} vehicles")

        next_choice = ask_continue_choice()

        if next_choice == "0":
            print("Goodbye!")
            return


if __name__ == "__main__":
    main()
