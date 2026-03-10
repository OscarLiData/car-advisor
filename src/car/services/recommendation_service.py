

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


DATA_FILE = Path("data/processed/cars_clean.csv")


@dataclass
class Car:
    # Represent a single car entry.

    brand: str
    model: str
    body_type: str
    energy: str
    price: float
    fuel_consumption: float
    co2: float
    power_kw: float
    weight_kg: float
    electric_range_km: float


def load_cars(data_file: Path) -> list[Car]:
    # Load cars from the CSV dataset.
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
                electric_range_km=float(row["electric_range_km"]),
            )
            cars.append(car)

    return cars


def normalize_text(text: str) -> str:
    # Normalize text for comparison (lowercase and strip).
    return text.strip().lower()


def ask_budget() -> float:
    # Ask the user for a maximum budget.
    print("\nEnter your maximum budget (example: 30000).")

    while True:
        value = input("Max budget (€): ").strip()
        try:
            budget = float(value)
            if budget <= 0:
                raise ValueError
            return budget
        except ValueError:
            print("Please enter a positive numeric value.")


def ask_energy_type() -> str:
    # Ask the user for an energy type (partial text, optional).
    print(
        "\nEnter one of the following energy types: "
        "(ELECTRIC, DIESEL, GASOLINE, ELECTRIC + GASOLINE HR, "
        "ELEC+DIESEL HR)"
    )
    print("Press Enter or type 'any' to accept all energy types.")

    while True:
        value = input("Energy type: ").strip()
        if not value or value.lower() == "any":
            return ""
        return value


def ask_body_type() -> str:
    # Ask the user for a body type (partial text, optional).
    print("\nEnter a body type (partial text is ok).")
    print(
        "Examples: 'SEDAN', 'OFF-ROAD', 'STATION WAGON', 'MPV', "
        "'MINI MPV', 'MPV COMPACT', 'CABRIOLET', 'COUPE', "
        "'CONVERTIBLE', 'LEISURE ACTIVITY VEHICLE', 'MINIBUS'"
    )
    print("Press Enter or type 'any' to accept all body types.")

    while True:
        value = input("Body type: ").strip()
        if not value or value.lower() == "any":
            return ""
        return value


def ask_priority_criterion() -> str:
    # Ask the user for a priority criterion.
    print("\nChoose a priority criterion:")
    print("1 - Lowest price")
    print("2 - Lowest fuel consumption")
    print("3 - Lowest CO2 emissions")
    print("4 - Highest engine power")
    print("5 - Highest electric driving range")

    mapping = {
        "1": "price_low",
        "2": "fuel_low",
        "3": "co2_low",
        "4": "power_high",
        "5": "range_high",
    }

    while True:
        choice = input("Your choice: ").strip()
        if choice in mapping:
            return mapping[choice]
        print("Invalid choice, please enter 1, 2, 3, 4 or 5.")


def filter_cars(
    cars: list[Car],
    max_budget: float,
    energy_pattern: str,
    body_pattern: str,
) -> list[Car]:
    # Apply budget, energy and body type filters to the dataset.
    result: list[Car] = []

    energy_pattern_norm = normalize_text(energy_pattern)
    body_pattern_norm = normalize_text(body_pattern)

    for car in cars:
        if car.price > max_budget:
            continue

        if energy_pattern_norm:
            if energy_pattern_norm not in normalize_text(car.energy):
                continue

        if body_pattern_norm:
            if body_pattern_norm not in normalize_text(car.body_type):
                continue

        result.append(car)

    return result


def select_best_cars(
    cars: list[Car],
    priority: str,
    top_n: int = 5,
) -> list[Car]:
    # Select the best matching cars according to the priority criterion.
    if not cars:
        return []

    if priority == "price_low":
        key_func = lambda c: c.price
        reverse = False
    elif priority == "fuel_low":
        key_func = lambda c: c.fuel_consumption
        reverse = False
    elif priority == "co2_low":
        key_func = lambda c: c.co2
        reverse = False
    elif priority == "power_high":
        key_func = lambda c: c.power_kw
        reverse = True
    elif priority == "range_high":
        key_func = lambda c: c.electric_range_km
        reverse = True
    else:
        key_func = lambda c: c.price
        reverse = False

    sorted_cars = sorted(cars, key=key_func, reverse=reverse)
    return sorted_cars[:top_n]


def display_found_cars(cars: list[Car]) -> None:
    # Display a list of matching cars.
    if not cars:
        print("\nNo vehicles match your criteria.\n")
        return

    print("\n=== Best matching vehicles ===")
    header = (
        f"{'Brand':10} | {'Model':20} | {'Body':12} | "
        f"{'Energy':10} | {'Price (€)':10} | {'CO2':6} | "
        f"{'Fuel (L/100km)':14} | {'Power (kW)':11} | "
        f"{'Elec range (km)':15}"
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
            f"{car.electric_range_km:15.0f}"
        )

    print("=" * len(header))
    print()


def ask_new_search_choice() -> bool:
    # Ask the user if they want to perform a new search.
    print("\nWhat do you want to do next?")
    print("1 - New search")
    print("0 - Quit")

    while True:
        choice = input("Your choice: ").strip()
        if choice == "1":
            return True
        if choice == "0":
            return False
        print("Invalid choice, please enter 1 or 0.")


def main() -> None:
    # Main program entry point.
    if not DATA_FILE.exists():
        msg = f"Dataset not found: {DATA_FILE}"
        raise FileNotFoundError(msg)

    print("=== Find a car tool ===")

    cars = load_cars(DATA_FILE)

    while True:
        budget = ask_budget()
        energy = ask_energy_type()
        body = ask_body_type()
        priority = ask_priority_criterion()

        filtered_cars = filter_cars(
            cars=cars,
            max_budget=budget,
            energy_pattern=energy,
            body_pattern=body,
        )

        best_cars = select_best_cars(filtered_cars, priority, top_n=5)
        display_found_cars(best_cars)

        if not ask_new_search_choice():
            print("\nEnd of search. Goodbye!")
            break


if __name__ == "__main__":
    main()
=======
import numpy as np
from car.filters.budget_filter import filter_by_budget
from car.filters.energy_filter import filter_by_energy
from car.filters.body_filter import filter_by_body


def recommend_vehicle(
    df,
    budget=None,
    energy=None,
    body=None,
    w_price=0.4,
    w_co2=0.3,
    w_consumption=0.2,
    w_power=0.1,
):

    filtered = df.copy()

    if budget:
        filtered = filter_by_budget(filtered, budget)

    if energy:
        filtered = filter_by_energy(filtered, energy)

    if body:
        filtered = filter_by_body(filtered, body)

    if filtered.empty:
        return filtered

    # critères
    criteria = filtered[
        [
            "vehicle_price_eur",
            "co2_mixed_g_km",
            "fuel_consumption_l_100km",
            "max_power_kw",
        ]
    ].values

    # normalisation
    norm = criteria / np.sqrt((criteria**2).sum(axis=0))

    # pondération
    weights = np.array([w_price, w_co2, w_consumption, w_power])
    weighted = norm * weights

    # solution idéale et anti-idéale
    ideal = np.array(
        [
            weighted[:, 0].min(),  # prix à minimiser
            weighted[:, 1].min(),  # CO2 à minimiser
            weighted[:, 2].min(),  # consommation à minimiser
            weighted[:, 3].max(),  # puissance à maximiser
        ]
    )

    anti_ideal = np.array(
        [
            weighted[:, 0].max(),
            weighted[:, 1].max(),
            weighted[:, 2].max(),
            weighted[:, 3].min(),
        ]
    )

    # distances
    dist_ideal = np.sqrt(((weighted - ideal) ** 2).sum(axis=1))
    dist_anti = np.sqrt(((weighted - anti_ideal) ** 2).sum(axis=1))

    # score TOPSIS
    score = dist_anti / (dist_ideal + dist_anti)

    filtered["score"] = score

    filtered = filtered.sort_values("score", ascending=False)

    return filtered.head(10)
>>>>>>> ac12e2b (update)
