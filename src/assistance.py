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

    # -------- Car Body --------
    
    car_body_dict = {
    1: "Berline",
    2: "Break",
    3: "Cabriolet",
    4: "Coupe",
    5: "Tous terrains",
    6: "Minibus",
    7: "Monospace / Monospace compact",
    8: "Minispace",
    9: "Combispace"
    }
    
    print("\nChoose car body:")
    print("1 - Berline")
    print("2 - Break")
    print("3 - Cabriolet")
    print("4 - Coupe")
    print("5 - Tous terrains")
    print("6 - Minibus")
    print("7 - Monospace / Monospace compact")
    print("8 - Minispace")
    print("9 - Combispace")

    choice = input("Enter a number (or press Enter to skip): ").strip()

    if choice == "1":
        filtered_df = filtered_df[
            filtered_df["Carrosserie"].str.contains("BERLINE", case=False, na=False)
        ]

    elif choice == "2":
        filtered_df = filtered_df[
            filtered_df["Carrosserie"].str.contains("BREAK", case=False, na=False)
        ]

    elif choice == "3":
        filtered_df = filtered_df[
            filtered_df["Carrosserie"].str.contains("CABRIOLET", case=False, na=False)
        ]

    elif choice == "4":
        filtered_df = filtered_df[
            filtered_df["Carrosserie"].str.contains("COUPE", regex=False, na=False)
        ]

    elif choice == "5":
        filtered_df = filtered_df[
            filtered_df["Carrosserie"].str.contains("TS TERRAINS", regex=False, na=False)
        ]
    
    elif choice == "6":
        filtered_df = filtered_df[
            filtered_df["Carrosserie"].str.contains("MINIBUS", regex=False, na=False)
        ]

    elif choice == "7":
        filtered_df = filtered_df[
            filtered_df["Carrosserie"].str.contains("MONOSPACE", regex=False, na=False)
        ]

    elif choice == "8":
        filtered_df = filtered_df[
            filtered_df["Carrosserie"].str.contains("MINISPACE", regex=False, na=False)
        ]

    elif choice == "9":
        filtered_df = filtered_df[
            filtered_df["Carrosserie"].str.contains("COMBISPACE", regex=False, na=False)
        ]

    if filtered_df.empty:
        print("No vehicles found for this energy type.")
        return

    # -------- Energie --------
    
    fuel_dict = {
    1: "Essence",
    2: "Diesel",
    3: "Hybride",
    4: "Electrique"
    }

    print("\nChoose fuel type:")
    print("1 - Essence")
    print("2 - Gazole")
    print("3 - Electric")
    print("4 - Hybrid")

    choice_e = input("Enter a number (or press Enter to skip): ").strip()

    if choice_e == "1":
        filtered_df = filtered_df[
            filtered_df["Energie"].str.contains("ESSENCE", case=False, na=False)
        ]

    elif choice_e == "2":
        filtered_df = filtered_df[
            filtered_df["Energie"].str.contains("GAZOLE", case=False, na=False)
        ]

    elif choice_e == "3":
        filtered_df = filtered_df[
            filtered_df["Energie"].str.contains("ELECTRIC", case=False, na=False)
        ]

    elif choice_e == "4":
        filtered_df = filtered_df[
            filtered_df["Energie"].str.contains("+", regex=False, na=False)
        ]

    if filtered_df.empty:
        print("No vehicles found for this energy type.")
        return
    
    # -------- Brand --------
    
    # User's choice
    selection = -1

    # All user's choices
    brand_selection = []

    # Dictionnary of all brands
    brands = {
        1: "RENAULT",
        2: "MAZDA",
        3: "B.M.W",
        4: "SKODA",
        5: "JEEP",
        6: "CITROEN",
        7: "ALFA ROMEO",
        8: "OPEL",
        9: "KIA",
        10: "AUDI",
        11: "PORSCHE",
        12: "MINI",
        13: "FORD",
        14: "PEUGEOT",
        15: "FIAT",
        16: "LEXUS",
        17: "VOLKSWAGEN",
        18: "TOYOTA",
        19: "SUZUKI",
        20: "HYUNDAI",
        21: "DACIA",
        22: "ROLLS ROYC",
        23: "HONDA",
        24: "NISSAN",
        25: "DS",
        26: "MITSUBISHI",
        27: "TESLA",
        28: "MERCEDES",
        29: "LAMBORGHIN",
        30: "MASERATI",
        31: "ALPINE",
        32: "M.G.",
        33: "VOLVO",
        34: "CUPRA",
        35: "SUBARU",
        36: "FERRARI",
        37: "LAND ROVER"
    }
    
    print("\nChoose as much brands as you want then enter 0:")
    print(brands)

    while selection != 0 or brand_selection == []:
        try:
            selection = int(input())
        except ValueError: # If user enters a string instead of an integer
            selection = 0
    
    # If user enter a number lower of greater that he is supposed to
        if not 0 <= selection <= 37:
            selection = 0

    # Check if the brand isn't already in the list
        if selection not in brand_selection and selection != 0:
            brand_selection.append(brands[selection])

# Filter the dataframe with only the brands selected
    filtered_df = filtered_df[
        filtered_df["Marque"].isin(brand_selection)
    ]

    # -------- Transmission --------
    if "Type de boite" in df.columns:

        transmissions = sorted(filtered_df["Type de boite"].dropna().unique())

        if len(transmissions) == 0:
            print("No transmission available for this selection.")
        else:
            print("\nAvailable transmission types:")
            for i, transmission in enumerate(transmissions, start=1):
                print(f"{i} - {transmission}")

            choice_t = input("Choose transmission number (or press Enter to skip): ").strip()

            if choice_t.isdigit():
                index = int(choice_t) - 1
                if 0 <= index < len(transmissions):
                    selected_transmission = transmissions[index]
                    filtered_df = filtered_df[
                        filtered_df["Type de boite"] == selected_transmission
                    ]

    # -------- Fiscal Horsepower --------
    
    fiscal_dict = {
    1: "< 10",
    2: "10-20",
    3: "20-30",
    4: "30-40",
    5: "40-50",
    6: "50-60",
    7: "60-70",
    8: "70-80",
    9: "> 90"
    }
    
    print("\nChoose fiscal horsepower :")
    print("1 - < 10")
    print("2 - 10-20")
    print("3 - 20-30")
    print("4 - 30-40")
    print("5 - 40-50")
    print("6 - 50-60")
    print("7 - 60-70")
    print("8 - 70-80")
    print("9 - > 90")

    choice_f = input("Enter a number (or press Enter to skip): ").strip()

    if choice_f == "1":
        filtered_df = filtered_df[
            (filtered_df["Puissance fiscale"]>=0) &(filtered_df["Puissance fiscale"]<=10)
        ]

    elif choice_f == "2":
        filtered_df = filtered_df[
            (filtered_df["Puissance fiscale"]>=10) &(filtered_df["Puissance fiscale"]<=20)
        ]

    elif choice_f == "3":
        filtered_df = filtered_df[
            (filtered_df["Puissance fiscale"]>=20) &(filtered_df["Puissance fiscale"]<=30)
        ]

    elif choice_f == "4":
        filtered_df = filtered_df[
            (filtered_df["Puissance fiscale"]>=30) &(filtered_df["Puissance fiscale"]<=40)
        ]
    
    elif choice_f == "5":
        filtered_df = filtered_df[
            (filtered_df["Puissance fiscale"]>=40) &(filtered_df["Puissance fiscale"]<=50)
        ]

    elif choice_f == "6":
        filtered_df = filtered_df[
            (filtered_df["Puissance fiscale"]>=50) &(filtered_df["Puissance fiscale"]<=60)
        ]

    elif choice_f == "7":
        filtered_df = filtered_df[
            (filtered_df["Puissance fiscale"]>=60) &(filtered_df["Puissance fiscale"]<=70)
        ]

    elif choice_f == "8":
        filtered_df = filtered_df[
            (filtered_df["Puissance fiscale"]>=70) &(filtered_df["Puissance fiscale"]<=80)
        ]

    elif choice_f == "9":
        filtered_df = filtered_df[
            (filtered_df["Puissance fiscale"]>=80) &(filtered_df["Puissance fiscale"]<=100)
        ]

    if filtered_df.empty:
        print("No vehicles found for this energy type.")
        return

    # -------- Results --------
    print("Vos sélections :") 
    print(f"\n   Budget : {budget_input}") 
    print(f"\n   Car Body : {car_body_dict[int(choice)]}") 
    print(f"\n   Fuel type : {fuel_dict[int(choice_f)]}") 
    for brand in brand_selection: 
        print(f"{brand}, ", end="")  
    print(f"\n   Fiscal horsepower : {fiscal_dict[int(choice_f)]}") 

    print("\nNumber of matching vehicles:", len(filtered_df))

    if not filtered_df.empty:
        print(filtered_df.head())
    else:
        print("No vehicles found with these criteria.")
