from car.data.loader import load_dataset
from car.processing.cleaner import clean_dataset
from car.cli.menus import main_menu


def main() -> None:
    df = load_dataset()
    clean_dataset(df)
    main_menu()


if __name__ == "__main__":
    main()