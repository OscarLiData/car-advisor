from car.services.comparison_service import Vehicule, display_brand_list_with_counts


def test_display_brand_list_with_counts(capsys):

    vehicles = [
        Vehicule("Renault","Clio","hatch","gas",10000,5,100,80,1200)
    ]

    display_brand_list_with_counts(vehicles)

    captured = capsys.readouterr()

    assert "Renault" in captured.out