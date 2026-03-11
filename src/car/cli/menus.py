from car.services.statistics_service import compute_global_statistics
from car.services.recommendation_service import recommend_vehicle
from car.services.visualization_service import radar_chart


def select_option(options, label):

    print(f"\nAvailable {label}:\n")

    for i, option in enumerate(options, start=1):
        print(f"{i} - {option}")

    while True:
        try:
            choice = int(input("\nSelect a number: "))

            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print("Invalid choice")

        except ValueError:
            print("Please enter a number")


def main_menu(df):

    while True:

        print("\nSmart Vehicle Decision Analytics")
        print("1 - View global statistics")
        print("2 - Find a vehicle")
        print("3 - Exit")

        choice = input("Select an option: ")

        if choice == "1":

            stats = compute_global_statistics(df)

            print("\nGlobal statistics\n")

            for key, value in stats.items():
                print(f"{key}: {value}")

        elif choice == "2":

            print("\nVehicle search\n")

            price_min = df["vehicle_price_eur"].min()
            price_max = df["vehicle_price_eur"].max()

            print(f"Vehicles available: {len(df)}")
            print(f"Price range: {price_min:.0f}€ – {price_max:.0f}€\n")

            try:
                budget = float(input("Maximum budget (€): "))
            except ValueError:
                print("Invalid budget")
                continue

            energy_options = sorted(df["energy"].unique())
            body_options = sorted(df["body_type"].unique())

            energy = select_option(energy_options, "energy types")
            body = select_option(body_options, "body types")

            print("\nImportance of criteria (0 → not important, 1 → very important)\n")

            try:
                w_price = float(input("Importance of price: "))
                w_co2 = float(input("Importance of CO2 emissions: "))
                w_consumption = float(input("Importance of fuel consumption: "))
                w_power = float(input("Importance of power: "))
            except ValueError:
                print("Invalid weight value")
                continue

            results = recommend_vehicle(
                df,
                budget,
                energy,
                body,
                w_price,
                w_co2,
                w_consumption,
                w_power,
            )

            print(f"\nVehicles found: {len(results)}\n")

            if results.empty:

                print("No vehicles match your criteria")

            else:

                display_columns = [
                    "brand",
                    "model",
                    "vehicle_price_eur",
                    "energy",
                    "body_type",
                    "co2_mixed_g_km",
                    "fuel_consumption_l_100km",
                    "max_power_kw",
                    "score",
                ]

                print(results[display_columns])

                show_chart = input("\nShow radar comparison chart? (y/n): ")

                if show_chart.lower() == "y":
                    radar_chart(results.head(5))

        elif choice == "3":

            print("\nGoodbye\n")
            break

        else:

            print("\nInvalid choice\n")