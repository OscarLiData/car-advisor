import pandas as pd
from pathlib import Path
from car.processing.cleaner import clean_dataset

DATA_PATH = Path("data/raw/ademe-car-labelling.csv")


def load_dataset():

    df = pd.read_csv(DATA_PATH)

    df = clean_dataset(df)

    return df