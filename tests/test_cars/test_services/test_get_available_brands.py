from car.services.comparison_service import Vehicule, get_available_brands


def test_get_available_brands():

    vehicles = [
        Vehicule("Renault","Clio","hatch","gas",10000,5,100,80,1200),
        Vehicule("Peugeot","208","hatch","gas",12000,5,100,80,1200)
    ]

    brands = get_available_brands(vehicles)

    assert brands == ["Peugeot","Renault"]