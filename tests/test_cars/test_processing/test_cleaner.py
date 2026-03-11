import pandas as pd
from car.processing.cleaner import clean_dataset


def test_clean_dataset_removes_nan():

    df = pd.DataFrame({
        "brand": ["Toyota", None],
        "price": [20000, 15000]
    })

    cleaned = clean_dataset(df)

    assert len(cleaned) == 1


def test_clean_dataset_keeps_valid():

    df = pd.DataFrame({
        "brand": ["Toyota"],
        "price": [20000]
    })

    cleaned = clean_dataset(df)

    assert len(cleaned) == 1