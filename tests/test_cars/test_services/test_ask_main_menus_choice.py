from car.services.comparison_service import ask_main_menu_choice


def test_ask_main_menu_choice(monkeypatch):

    monkeypatch.setattr("builtins.input", lambda _: "1")

    result = ask_main_menu_choice()

    assert result == "1"