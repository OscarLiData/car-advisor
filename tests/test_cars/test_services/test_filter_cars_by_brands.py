from car.services.comparison_service import Vehicule, filter_cars_by_brand

def test_filter_cars_by_brand():

    vehicles = [
        Vehicule("Renault","Clio","hatch","gas",10000,5,100,80,1200),
        Vehicule("Peugeot","208","hatch","gas",12000,5,100,80,1200)
    ]

    result = filter_cars_by_brand(vehicles,"Renault")

    assert len(result) == 1
