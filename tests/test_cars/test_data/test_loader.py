from car.data.loader import load_dataset


def test_load_dataset():
    """
    Test that the dataset loads correctly.
    """

    df = load_dataset()

    assert df is not None
    assert len(df) > 0