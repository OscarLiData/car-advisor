import pandas as pd


def run_assistance(df: pd.DataFrame) -> None:
    print("\nVEHICLE ASSISTANCE")

    filtered_df = df.copy()

    # -------- Budget --------
    if "Prix véhicule" in df.columns:
        min_price = df["Prix véhicule"].min()
        max_price = df["Prix véhicule"].max()

        print(f"\nPrice range: {min_price:.0f} € - {max_price:.0f} €")

        budget_input = input("Enter maximum budget (or press Enter to skip): ").strip()

        if budget_input:
            try:
                budget = float(budget_input)
                filtered_df = filtered_df[
                    filtered_df["Prix véhicule"] <= budget
                ]

                if filtered_df.empty:
                    print("No vehicles found under this budget.")
                    return

            except ValueError:
                print("Invalid budget input.")
    else:
        print("Column 'Prix véhicule' not found.")
        return

    # -------- Energie --------
    print("\nChoose fuel type:")
    print("1 - Essence")
    print("2 - Gazole")
    print("3 - Electric")
    print("4 - Hybrid")

    choice = input("Enter a number (or press Enter to skip): ").strip()

    if choice == "1":
        filtered_df = filtered_df[
            filtered_df["Energie"].str.contains("ESSENCE", case=False, na=False)
        ]

    elif choice == "2":
        filtered_df = filtered_df[
            filtered_df["Energie"].str.contains("GAZOLE", case=False, na=False)
        ]

    elif choice == "3":
        filtered_df = filtered_df[
            filtered_df["Energie"].str.contains("ELECTRIC", case=False, na=False)
        ]

    elif choice == "4":
        filtered_df = filtered_df[
            filtered_df["Energie"].str.contains("+", regex=False, na=False)
        ]

    if filtered_df.empty:
        print("No vehicles found for this energy type.")
        return

    # -------- Transmission --------
    if "Type de boite" in df.columns:

        transmissions = sorted(filtered_df["Type de boite"].dropna().unique())

        if len(transmissions) == 0:
            print("No transmission available for this selection.")
        else:
            print("\nAvailable transmission types:")
            for i, transmission in enumerate(transmissions, start=1):
                print(f"{i} - {transmission}")

            choice = input("Choose transmission number (or press Enter to skip): ").strip()

            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(transmissions):
                    selected_transmission = transmissions[index]
                    filtered_df = filtered_df[
                        filtered_df["Type de boite"] == selected_transmission
                    ]

    # -------- Results --------
    print("\nNumber of matching vehicles:", len(filtered_df))

    if not filtered_df.empty:
        print(filtered_df.head())
    else:
        print("No vehicles found with these criteria.")
