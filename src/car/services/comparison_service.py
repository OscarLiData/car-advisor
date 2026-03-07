"""Car comparison tool using a CSV dataset.

User can:
- list all vehicles
- compare a single brand
- compare two brands

For each selected brand, the tool computes:
- average vehicle price
- average fuel consumption
- average CO2 emissions
- average engine power
- average vehicle weight
"""

from __future__ import annotations

import csv
import difflib
from dataclasses import dataclass
from pathlib import Path
from statistics import mean


DATA_FILE = Path("data/processed/cars_clean.csv")


@dataclass
class Car:
    """Represent a single car entry."""

    brand: str
    model: str
    body_type: str
    energy: str
    price: float
    fuel_consumption: float
    co2: float
    power_kw: float
    weight_kg: float


def load_cars(data_file: Path) -> list[Car]:
    """Load cars from the CSV dataset."""
    cars: list[Car] = []

    with data_file.open(encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            car = Car(
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
            cars.append(car)

    return cars


def get_available_brands(cars: list[Car]) -> list[str]:
    """Return the list of distinct brands sorted alphabetically."""
    return sorted({car.brand for car in cars})


def normalize_text(text: str) -> str:
    """Normalize text for comparison (lowercase and strip)."""
    return text.strip().lower()


def fuzzy_choose_brand(brands: list[str], label: str) -> str:
    """Ask the user to type a brand name with fuzzy matching."""
    print(f"\nSelect {label}:")
    print("Type the brand name you want to analyze.")
    print("Example: BMW, Renault, Audi")
    print("Type 'exit' to cancel.\n")

    while True:
        user_input = input("Brand: ").strip()
        if not user_input:
            print("Please enter a brand name.")
            continue

        if user_input.lower() in {"exit", "quit"}:
            return ""

        normalized_input = normalize_text(user_input)
        normalized_brands = [normalize_text(b) for b in brands]

        for brand in brands:
            if normalize_text(brand) == normalized_input:
                return brand

        close_matches = difflib.get_close_matches(
            normalized_input,
            normalized_brands,
            n=1,
            cutoff=0.6,
        )

        if close_matches:
            best_match_normalized = close_matches[0]
            for brand in brands:
                if normalize_text(brand) == best_match_normalized:
                    print(f"Did you mean: {brand}? Selected.\n")
                    return brand

        print("Unknown brand, please try again or type 'exit' to cancel.")


def ask_main_menu_choice() -> str:
    """Ask the user for the main menu choice."""
    print("\n===== Main menu =====")
    print("1 - List all vehicles")
    print("2 - Compare one brand")
    print("3 - Compare two brands")
    print("0 - Quit")

    while True:
        choice = input("Your choice: ").strip()
        if choice in {"0", "1", "2", "3"}:
            return choice
        print("Invalid choice, please enter 0, 1, 2 or 3.")


def ask_continue_choice() -> str:
    """Ask the user what to do after a comparison or listing."""
    print("\nWhat do you want to do next?")
    print("1 - New comparison / listing")
    print("2 - Back to main menu")
    print("0 - Quit")

    while True:
        choice = input("Your choice: ").strip()
        if choice in {"0", "1", "2"}:
            return choice
        print("Invalid choice, please enter 0, 1 or 2.")


def filter_cars_by_brand(cars: list[Car], brand: str) -> list[Car]:
    """Return a list of cars matching the selected brand."""
    return [car for car in cars if car.brand == brand]


def compute_statistics(cars: list[Car]) -> dict:
    """Compute statistics for a set of cars."""
    prices = [car.price for car in cars]
    fuel = [car.fuel_consumption for car in cars]
    co2_values = [car.co2 for car in cars]
    power = [car.power_kw for car in cars]
    weight = [car.weight_kg for car in cars]

    return {
        "count": len(cars),
        "avg_price": mean(prices),
        "avg_fuel": mean(fuel),
        "avg_co2": mean(co2_values),
        "avg_power": mean(power),
        "avg_weight": mean(weight),
    }


def display_single_result(brand: str, stats: dict) -> None:
    """Display comparison results for one brand."""
    print("\n=== Comparison results ===")
    print(f"Brand: {brand}")
    print(f"Number of models: {stats['count']}")
    print(f"Average price: {stats['avg_price']:.0f} €")
    print(f"Average fuel consumption: {stats['avg_fuel']:.2f} L/100km")
    print(f"Average CO2 emissions: {stats['avg_co2']:.2f} g/km")
    print(f"Average engine power: {stats['avg_power']:.1f} kW")
    print(f"Average vehicle weight: {stats['avg_weight']:.0f} kg")
    print("==========================\n")


def display_two_results(
    brand1: str,
    stats1: dict,
    brand2: str,
    stats2: dict,
) -> None:
    """Display comparison results for two brands."""
    print("\n=== Comparison results (two brands) ===")
    header = f"{'Metric':30} | {brand1:15} | {brand2:15}"
    print(header)
    print("-" * len(header))

    def line(label: str, value1: str, value2: str) -> None:
        print(f"{label:30} | {value1:15} | {value2:15}")

    line("Number of models",
         str(stats1["count"]),
         str(stats2["count"]))
    line("Average price (€)",
         f"{stats1['avg_price']:.0f}",
         f"{stats2['avg_price']:.0f}")
    line("Avg fuel (L/100km)",
         f"{stats1['avg_fuel']:.2f}",
         f"{stats2['avg_fuel']:.2f}")
    line("Avg CO2 (g/km)",
         f"{stats1['avg_co2']:.2f}",
         f"{stats2['avg_co2']:.2f}")
    line("Avg power (kW)",
         f"{stats1['avg_power']:.1f}",
         f"{stats2['avg_power']:.1f}")
    line("Avg weight (kg)",
         f"{stats1['avg_weight']:.0f}",
         f"{stats2['avg_weight']:.0f}")

    print("=" * len(header))
    print()


def display_all_vehicles(cars: list[Car]) -> None:
    """Display the full vehicle list."""
    print("\n=== Vehicle list ===")
    header = (
        f"{'Brand':10} | {'Model':20} | {'Body':12} | "
        f"{'Energy':10} | {'Price (€)':10} | {'CO2':6} | "
        f"{'Fuel (L/100km)':14} | {'Power (kW)':11} | {'Weight (kg)':11}"
    )
    print(header)
    print("-" * len(header))

    for car in cars:
        print(
            f"{car.brand:10} | "
            f"{car.model:20} | "
            f"{car.body_type:12} | "
            f"{car.energy[:10]:10} | "
            f"{car.price:10.0f} | "
            f"{car.co2:6.1f} | "
            f"{car.fuel_consumption:14.2f} | "
            f"{car.power_kw:11.1f} | "
            f"{car.weight_kg:11.0f}"
        )

    print("=" * len(header))
    print()


def main() -> None:
    """Main program entry point."""
    if not DATA_FILE.exists():
        msg = f"Dataset not found: {DATA_FILE}"
        raise FileNotFoundError(msg)

    cars = load_cars(DATA_FILE)
    brands = get_available_brands(cars)

    while True:
        menu_choice = ask_main_menu_choice()

        if menu_choice == "0":
            print("Goodbye!")
            return

        if menu_choice == "1":
            # List all vehicles.
            display_all_vehicles(cars)

        if menu_choice == "2":
            # Compare one brand.
            brand = fuzzy_choose_brand(brands, label="brand 1")
            if not brand:
                print("Operation cancelled.")
            else:
                brand_cars = filter_cars_by_brand(cars, brand)
                if not brand_cars:
                    print("No cars found for this brand.")
                else:
                    stats = compute_statistics(brand_cars)
                    display_single_result(brand, stats)

        if menu_choice == "3":
            # Compare two brands.
            brand1 = fuzzy_choose_brand(brands, label="brand 1")
            if not brand1:
                print("Operation cancelled.")
            else:
                brand2 = fuzzy_choose_brand(brands, label="brand 2")
                if not brand2:
                    print("Operation cancelled.")
                else:
                    brand1_cars = filter_cars_by_brand(cars, brand1)
                    brand2_cars = filter_cars_by_brand(cars, brand2)

                    if not brand1_cars:
                        print(f"No cars found for brand: {brand1}")
                    elif not brand2_cars:
                        print(f"No cars found for brand: {brand2}")
                    else:
                        stats1 = compute_statistics(brand1_cars)
                        stats2 = compute_statistics(brand2_cars)
                        display_two_results(brand1, stats1, brand2, stats2)

        # After the action, ask what to do next.
        next_choice = ask_continue_choice()
        if next_choice == "0":
            print("Goodbye!")
            return
        if next_choice == "1":
            # Loop again but keep the same cars / brands in memory.
            continue
        if next_choice == "2":
            # Back to main menu: just continue, the loop will restart.
            continue


if __name__ == "__main__":
    main()
