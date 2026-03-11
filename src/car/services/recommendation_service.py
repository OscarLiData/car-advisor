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
    """
    Recommend vehicles using the TOPSIS multi-criteria decision method.
    """

    filtered = df.copy()

    # --- filtres ---

    if budget is not None:
        filtered = filter_by_budget(filtered, budget)

    if energy:
        filtered = filter_by_energy(filtered, energy)

    if body:
        filtered = filter_by_body(filtered, body)

    if filtered.empty:
        return filtered

    # --- matrice des critères ---

    criteria = filtered[
        [
            "vehicle_price_eur",
            "co2_mixed_g_km",
            "fuel_consumption_l_100km",
            "max_power_kw",
        ]
    ].to_numpy()

    # --- normalisation vectorielle ---

    norm = criteria / np.sqrt((criteria**2).sum(axis=0))

    # --- poids ---

    weights = np.array([w_price, w_co2, w_consumption, w_power])

    # normalisation des poids
    weights = weights / weights.sum()

    weighted = norm * weights

    # --- solution idéale et anti-idéale ---

    ideal = np.array([
        weighted[:, 0].min(),  # prix
        weighted[:, 1].min(),  # CO2
        weighted[:, 2].min(),  # consommation
        weighted[:, 3].max(),  # puissance
    ])

    anti_ideal = np.array([
        weighted[:, 0].max(),
        weighted[:, 1].max(),
        weighted[:, 2].max(),
        weighted[:, 3].min(),
    ])

    # --- distances ---

    dist_ideal = np.sqrt(((weighted - ideal) ** 2).sum(axis=1))
    dist_anti = np.sqrt(((weighted - anti_ideal) ** 2).sum(axis=1))

    # --- score TOPSIS ---

    score = dist_anti / (dist_ideal + dist_anti)

    filtered = filtered.copy()
    filtered["score"] = score

    # --- classement final ---

    return filtered.sort_values("score", ascending=False).head(10)