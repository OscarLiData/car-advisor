from pathlib import Path
import pandas as pd

from exceptions import DatasetNotFoundError


def load_dataset(path: str | Path) -> pd.DataFrame:
    """
    Load a CSV dataset and return a pandas DataFrame.
    """

    file_path = Path(path)

    if not file_path.exists():
        raise DatasetNotFoundError(f"Dataset not found at {file_path}")

    try:
        df = pd.read_csv(file_path)
    except Exception as error:
        raise RuntimeError(f"Error while reading the dataset: {error}")

    return df
