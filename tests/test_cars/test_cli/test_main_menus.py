from car.cli.menus import main_menu


def test_main_menu_returns_user_choice(monkeypatch):
    """
    Test that main_menu returns the value entered by the user.
    """

    monkeypatch.setattr("builtins.input", lambda _: "1")

    result = main_menu()

    assert result == "1"