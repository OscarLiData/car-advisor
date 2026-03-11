from car.cli.assistance import show_help


def test_show_help(capsys):

    show_help()

    captured = capsys.readouterr()

    assert "help" in captured.out.lower()