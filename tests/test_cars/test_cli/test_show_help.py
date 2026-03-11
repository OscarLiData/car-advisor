from car.cli.assistance import show_help


def test_show_help_prints_message(capsys):
    """
    Test that show_help prints the help message.
    """

    show_help()

    captured = capsys.readouterr()

    assert "vehicle data" in captured.out