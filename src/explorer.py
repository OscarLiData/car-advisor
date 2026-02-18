import pandas as pd
import matplotlib.pyplot as plt


def get_numeric_columns(df: pd.DataFrame) -> list[str]:
    """
    Return the list of numeric columns in the dataset.
    """
    return df.select_dtypes(include="number").columns.tolist()


def show_variables(df: pd.DataFrame) -> None:
    """
    Display basic information about the dataset.
    """
    print("\n DATASET INFORMATION\n")

    print(f"Number of rows: {df.shape[0]}")
    print(f"Number of columns: {df.shape[1]}\n")

    print("Columns:")
    print(df.columns.tolist())

    print("\nData types:")
    print(df.dtypes)


def show_graphics(df: pd.DataFrame) -> None:
    """
    Display a histogram for the first numeric column.
    """
    numeric_columns = get_numeric_columns(df)

    if not numeric_columns:
        print("No numeric columns available.")
        return

    column = numeric_columns[0]

    plt.figure()
    df[column].hist(bins=20)
    plt.title(f"Distribution of {column}")
    plt.xlabel(column)
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.show()
