from car.data.loader import load_dataset
from car.processing.cleaner import clean_dataset
from car.cli.menus import run_cli


def main():

    df = load_dataset()
    clean_dataset(df)

    run_cli(df)


if __name__ == "__main__":
    main()