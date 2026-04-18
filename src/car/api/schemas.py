"""
Schémas Pydantic pour l'API.

Séparation claire entre :
- VehicleOut : ce que l'API renvoie (lecture)
- RecommendQuery : paramètres de la recommandation TOPSIS
"""

from pydantic import BaseModel, Field


class VehicleOut(BaseModel):
    """Représentation d'un véhicule renvoyé par l'API."""

    brand: str
    model: str
    body_type: str
    energy: str
    vehicle_price_eur: float
    co2_mixed_g_km: float
    fuel_consumption_l_100km: float
    electric_range_km: float
    max_power_kw: float
    vehicle_weight_kg: float
    eco_bonus_malus_eur: float

    model_config = {"from_attributes": True}


class VehicleRecommended(VehicleOut):
    """Véhicule avec son score TOPSIS (0 → 1, plus élevé = meilleur)."""

    score: float = Field(..., ge=0.0, le=1.0, description="Score TOPSIS normalisé")


class StatsOut(BaseModel):
    """Statistiques globales du dataset."""

    number_of_vehicles: int
    average_price: float
    average_co2: float
    average_consumption: float


class HealthOut(BaseModel):
    """Réponse du health check."""

    status: str
    version: str
    vehicles_loaded: int
