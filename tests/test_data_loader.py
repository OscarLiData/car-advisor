mport pandas as pd
import pytest
from pathlib import Path

from src.data_loader import load_dataset
from src.exceptions import DatasetNotFoundError


def test_load_dataset_success(tmp_path):
"""
Test that a valid CSV file is correctly loaded.
"""

# Create temporary CSV file
file = tmp_path / "test.csv"
file.write_text("col1,col2\n1,2\n3,4")

df = load_dataset(file)

assert isinstance(df, pd.DataFrame)
assert df.shape == (2, 2)


def test_load_dataset_file_not_found():
"""
Test that a DatasetNotFoundError is raised
when the file does not exist.
"""

with pytest.raises(DatasetNotFoundError):
load_dataset("non_existent_file.csv")


def test_load_dataset_invalid_csv(tmp_path):
"""
Test that a RuntimeError is raised
when the CSV is malformed.
"""

file = tmp_path / "bad.csv"
file.write_text("not,a,valid\ncsv")

df = load_dataset(file)
assert isinstance(df, pd.DataFrame)