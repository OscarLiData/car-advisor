from car.services.statistics_service import compute_global_statistics


def main_menu(df):

    while True:

        print("\nSmart Vehicle Decision Analytics")
        print("1 - View global statistics")
        print("2 - Exit")

        choice = input("Select an option: ")

        if choice == "1":

            stats = compute_global_statistics(df)

            print("\nGlobal statistics")
            for key, value in stats.items():
                print(f"{key}: {value}")

        elif choice == "2":

            print("Goodbye")
            break

        else:
            print("Invalid choice")