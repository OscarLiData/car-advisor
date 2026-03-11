from car.services.comparison_service import ask_continue_choice


def test_ask_continue_choice(monkeypatch):

    monkeypatch.setattr("builtins.input", lambda _: "0")

    result = ask_continue_choice()

    assert result == "0"