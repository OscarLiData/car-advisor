import pandas as pd
from pathlib import Path

DATA_PATH = Path("data/raw/ademe-car-labelling.csv")


def load_dataset():

    df = pd.read_csv(DATA_PATH)

    return df