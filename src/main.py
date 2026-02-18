from data_loader import load_dataset
from explorer import show_graphics, show_variables
from assistance import run_assistance
from menus import (
    write_welcome,
    context_menu,
    dataset_information_menu,
    explore_dataset_menu
)
from exceptions import DatasetNotFoundError


def run() -> None:
    write_welcome()

    try:
        df = load_dataset("data/ademe-car-labelling.csv")
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

