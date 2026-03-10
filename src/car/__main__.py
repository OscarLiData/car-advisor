from car.data.loader import load_dataset
from car.cli.menus import main_menu


def main():

    df = load_dataset()

    main_menu(df)


if __name__ == "__main__":
    main()