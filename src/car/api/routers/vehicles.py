"""
Router /vehicles — liste, filtrage, recommandation, comparaison, statistiques.
"""

import logging

import pandas as pd
from fastapi import APIRouter, HTTPException, Query

from car.api.dependencies import DataFrameDep
from car.api.schemas import StatsOut, VehicleOut, VehicleRecommended
from car.filters.body_filter import filter_by_body
from car.filters.budget_filter import filter_by_budget
from car.filters.energy_filter import filter_by_energy
from car.services.recommendation_service import recommend_vehicle
from car.services.statistics_service import compute_global_statistics

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/vehicles", tags=["vehicles"])


def _df_to_vehicles(df: pd.DataFrame) -> list[VehicleOut]:
    """Convertit un DataFrame en liste de VehicleOut."""
    # On remplace les NaN résiduels par 0 pour la sérialisation JSON
    df = df.fillna(0)
    return [VehicleOut(**row) for row in df.to_dict(orient="records")]


# ---------------------------------------------------------------------------
# GET /vehicles/brands
# ---------------------------------------------------------------------------


@router.get("/brands", response_model=list[str], summary="Liste des marques disponibles")
def get_brands(df: DataFrameDep) -> list[str]:
    """Retourne la liste triée des marques présentes dans le dataset."""
    return sorted(df["brand"].unique().tolist())


# ---------------------------------------------------------------------------
# GET /vehicles/stats
# ---------------------------------------------------------------------------


@router.get("/stats", response_model=StatsOut, summary="Statistiques globales du dataset")
def get_stats(df: DataFrameDep) -> StatsOut:
    """Prix moyen, CO2 moyen, consommation moyenne, nombre de véhicules."""
    stats = compute_global_statistics(df)
    return StatsOut(**stats)


# ---------------------------------------------------------------------------
# GET /vehicles — liste avec filtres optionnels
# ---------------------------------------------------------------------------


@router.get(
    "",
    response_model=list[VehicleOut],
    summary="Liste des véhicules avec filtres optionnels",
)
def list_vehicles(
    df: DataFrameDep,
    brand: str | None = Query(None, description="Filtrer par marque (ex: TOYOTA)"),
    energy: str | None = Query(None, description="Type d'énergie : electric, diesel, gasoline"),
    body: str | None = Query(None, description="Type de carrosserie : berline, suv, ..."),
    budget: float | None = Query(None, description="Budget maximum en €"),
    limit: int = Query(50, ge=1, le=500, description="Nombre maximum de résultats"),
) -> list[VehicleOut]:
    """
    Retourne une liste de véhicules filtrés.
    Tous les paramètres sont optionnels et cumulables.
    """
    filtered = df.copy()

    if brand:
        filtered = filtered[filtered["brand"].str.upper() == brand.upper()]
    if budget is not None:
        filtered = filter_by_budget(filtered, budget)
    if energy:
        filtered = filter_by_energy(filtered, energy)
    if body:
        filtered = filter_by_body(filtered, body)

    if filtered.empty:
        return []

    return _df_to_vehicles(filtered.head(limit))


# ---------------------------------------------------------------------------
# GET /vehicles/recommend — TOPSIS
# ---------------------------------------------------------------------------


@router.get(
    "/recommend",
    response_model=list[VehicleRecommended],
    summary="Recommandation multi-critères TOPSIS",
)
def recommend(
    df: DataFrameDep,
    budget: float | None = Query(None, description="Budget maximum en €"),
    energy: str | None = Query(None, description="electric | diesel | gasoline"),
    body: str | None = Query(None, description="berline | suv | monospace | ..."),
    w_price: float = Query(0.4, ge=0, le=1, description="Poids du critère prix"),
    w_co2: float = Query(0.3, ge=0, le=1, description="Poids du critère CO2"),
    w_consumption: float = Query(0.2, ge=0, le=1, description="Poids consommation"),
    w_power: float = Query(0.1, ge=0, le=1, description="Poids puissance"),
) -> list[VehicleRecommended]:
    """
    Recommande jusqu'à 10 véhicules via l'algorithme TOPSIS.

    Le score (0 → 1) représente le compromis optimal entre prix, CO2,
    consommation et puissance, pondéré par les w_* fournis.
    """
    results = recommend_vehicle(
        df,
        budget=budget,
        energy=energy,
        body=body,
        w_price=w_price,
        w_co2=w_co2,
        w_consumption=w_consumption,
        w_power=w_power,
    )

    if results.empty:
        return []

    results = results.fillna(0)
    return [VehicleRecommended(**row) for row in results.to_dict(orient="records")]


# ---------------------------------------------------------------------------
# GET /vehicles/compare — comparaison de deux marques
# ---------------------------------------------------------------------------


@router.get(
    "/compare",
    response_model=dict,
    summary="Comparaison statistique de deux marques",
)
def compare_brands(
    df: DataFrameDep,
    brand1: str = Query(..., description="Première marque (ex: TOYOTA)"),
    brand2: str = Query(..., description="Deuxième marque (ex: RENAULT)"),
) -> dict:
    """
    Compare les statistiques moyennes (prix, CO2, consommation, puissance)
    de deux marques.
    """
    df1 = df[df["brand"].str.upper() == brand1.upper()]
    df2 = df[df["brand"].str.upper() == brand2.upper()]

    if df1.empty:
        raise HTTPException(status_code=404, detail=f"Marque introuvable : {brand1}")
    if df2.empty:
        raise HTTPException(status_code=404, detail=f"Marque introuvable : {brand2}")

    def _stats(frame: pd.DataFrame, name: str) -> dict:
        return {
            "brand": name.upper(),
            "vehicle_count": len(frame),
            "avg_price_eur": round(frame["vehicle_price_eur"].mean(), 2),
            "avg_co2_g_km": round(frame["co2_mixed_g_km"].mean(), 2),
            "avg_consumption_l_100km": round(frame["fuel_consumption_l_100km"].mean(), 2),
            "avg_power_kw": round(frame["max_power_kw"].mean(), 2),
        }

    return {
        brand1.upper(): _stats(df1, brand1),
        brand2.upper(): _stats(df2, brand2),
    }
