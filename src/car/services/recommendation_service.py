import numpy as np
from car.filters.budget_filter import filter_by_budget
from car.filters.energy_filter import filter_by_energy
from car.filters.body_filter import filter_by_body


def recommend_vehicle(
    df,
    budget=None,
    energy=None,
    body=None,
    w_price=0.4,
    w_co2=0.3,
    w_consumption=0.2,
    w_power=0.1,
):

    filtered = df.copy()

    print("\nTotal vehicles in dataset:", len(filtered))

    # filtre budget
    if budget is not None:
        filtered = filter_by_budget(filtered, budget)
        print("Vehicles after budget filter:", len(filtered))

    # filtre énergie
    if energy:
        print("\nEnergy requested:", energy)
        print("Available energies:", df["energy"].unique())

        filtered = filter_by_energy(filtered, energy)
        print("Vehicles after energy filter:", len(filtered))

    # filtre carrosserie
    if body:
        print("\nBody requested:", body)
        print("Available body types:", df["body_type"].unique())

        filtered = filter_by_body(filtered, body)
        print("Vehicles after body filter:", len(filtered))

    if filtered.empty:
        print("\nNo vehicles remaining after filters.")
        return filtered

    # matrice des critères
    criteria = filtered[
        [
            "vehicle_price_eur",
            "co2_mixed_g_km",
            "fuel_consumption_l_100km",
            "max_power_kw",
        ]
    ].to_numpy()

    norm = criteria / np.sqrt((criteria**2).sum(axis=0))

    weights = np.array([w_price, w_co2, w_consumption, w_power])
    weighted = norm * weights

    ideal = np.array([
        weighted[:, 0].min(),
        weighted[:, 1].min(),
        weighted[:, 2].min(),
        weighted[:, 3].max(),
    ])

    anti_ideal = np.array([
        weighted[:, 0].max(),
        weighted[:, 1].max(),
        weighted[:, 2].max(),
        weighted[:, 3].min(),
    ])

    dist_ideal = np.sqrt(((weighted - ideal) ** 2).sum(axis=1))
    dist_anti = np.sqrt(((weighted - anti_ideal) ** 2).sum(axis=1))

    score = dist_anti / (dist_ideal + dist_anti)

    filtered = filtered.copy()
    filtered["score"] = score

    return filtered.sort_values("score", ascending=False).head(10)