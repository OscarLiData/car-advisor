import os
import sys

if sys.version_info < (3, 14):
    print("This project requires Python 3.14 or higher.")
    sys.exit()

from src.data_cleaner import clean_dataset
from src.data_loader import load_dataset
from src.explorer import show_graphics, show_variables
from src.assistance import run_assistance
from src.menus import (
    write_welcome,
    context_menu,
    dataset_information_menu,
    explore_dataset_menu
)
from src.exceptions import DatasetNotFoundError

DATA_PATH = "data/processed/cars_clean.csv"


def run() -> None:
    write_welcome()

    # Run cleaner only if dataset does not exist
    if not os.path.exists(DATA_PATH):
        print("Clean dataset not found. Running data cleaner...")
        clean_dataset()

    try:
        df = load_dataset(DATA_PATH)
    except DatasetNotFoundError as error:
        print(error)
        return

    while True:
        context_choice = context_menu()

        if context_choice == "1":
            while True:
                dataset_choice = dataset_information_menu()

                if dataset_choice == "1":
                    while True:
                        explore_choice = explore_dataset_menu()

                        if explore_choice == "1":
                            show_graphics(df)

                        elif explore_choice == "2":
                            show_variables(df)

                        elif explore_choice == "3":
                            break

                        else:
                            print("Please choose a valid option.")

                elif dataset_choice == "2":
                    break

                else:
                    print("Please choose a valid option.")

        elif context_choice == "2":
            run_assistance(df)

        elif context_choice == "3":
            break

        else:
            print("Please choose a valid option.")

    print("\nThank you for using the program.")


if __name__ == "__main__":
    run()