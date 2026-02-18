def write_welcome() -> None:
    print("         VEHICLE DATA ANALYZER")


def context_menu() -> str:
    print("\nCONTEXT")
    print("1 - Dataset Information")
    print("2 - Exit")
    return input("Choose an option: ").strip()


def dataset_information_menu() -> str:
    print("\nDATASET INFORMATION")
    print("1 - Explore the Dataset")
    print("2 - Return to Context")
    return input("Choose an option: ").strip()


def explore_dataset_menu() -> str:
    print("\nEXPLORE THE DATASET")
    print("1 - Show Graphics")
    print("2 - Show Variables and Definitions")
    print("3 - Exit")
    return input("Choose an option: ").strip()
