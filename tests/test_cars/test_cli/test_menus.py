from car.cli.menus import main_menu


def test_main_menu_choice(monkeypatch):

    monkeypatch.setattr("builtins.input", lambda _: "1")

    choice = main_menu()

    assert choice == "1"