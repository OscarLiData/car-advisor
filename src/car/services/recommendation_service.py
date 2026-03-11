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


    print("Initial vehicles:", len(filtered))

    if budget is not None:
        filtered = filter_by_budget(filtered, budget)
        print("After budget filter:", len(filtered))

    if energy:
        filtered = filter_by_energy(filtered, energy)
        print("After energy filter:", len(filtered))

    if body:
        filtered = filter_by_body(filtered, body)
        print("After body filter:", len(filtered))

    
    filtered["fuel_consumption_l_100km"] = filtered[
    "fuel_consumption_l_100km"].fillna(0)

    # suppression des lignes avec valeurs manquantes
    filtered = filtered.dropna(
        subset=[
            "vehicle_price_eur",
            "co2_mixed_g_km",
            "fuel_consumption_l_100km",
            "max_power_kw",
        ]
    )

    print("After removing missing values:", len(filtered))

    if filtered.empty:
        return filtered

    # matrice des critères
    criteria = filtered[
        [
            "vehicle_price_eur",
            "co2_mixed_g_km",
            "fuel_consumption_l_100km",
            "max_power_kw",
        ]
    ].to_numpy(dtype=float)

    # normalisation vectorielle (TOPSIS)
    denom = np.sqrt((criteria**2).sum(axis=0))
    denom[denom == 0] = 1
    norm = criteria / denom

    denominator = np.sqrt((criteria**2).sum(axis=0))

    # éviter division par zéro
    denominator[denominator == 0] = 1

    norm = criteria / denominator
    # --- poids ---
    weights = np.array([w_price, w_co2, w_consumption, w_power])

    if weights.sum() == 0:
        weights = np.ones_like(weights) / len(weights)
    else:
        weights = weights / weights.sum()

    weighted = norm * weights

    # critères coût / bénéfice
    # coût : prix, co2, consommation
    # bénéfice : puissance
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

    # distances
    dist_ideal = np.sqrt(((weighted - ideal) ** 2).sum(axis=1))
    dist_anti = np.sqrt(((weighted - anti_ideal) ** 2).sum(axis=1))

    denom_score = dist_ideal + dist_anti
    denom_score[denom_score == 0] = 1

    score = dist_anti / denom_score

    filtered = filtered.copy()
    filtered["score"] = score

    return filtered.sort_values("score", ascending=False).head(10)