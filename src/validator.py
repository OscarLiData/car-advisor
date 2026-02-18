def validate_menu_choice(choice: str, valid_options: list[str]) -> bool:
    """
    Check if the user's choice is valid.
    """
    return choice.strip() in valid_options
