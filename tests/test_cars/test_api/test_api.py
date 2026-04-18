"""
Tests de l'API FastAPI.

On utilise le TestClient de Starlette (inclus dans FastAPI) + httpx.
Le DataFrame est mocké dans app.state pour ne pas dépendre du CSV réel.
"""

import pandas as pd
import pytest
from fastapi.testclient import TestClient

from car.api.main import app


@pytest.fixture
def client(sample_df) -> TestClient:
    """
    Client de test avec le DataFrame mocké dans app.state.
    Pas besoin de charger le vrai CSV ADEME.
    """
    app.state.df = sample_df
    return TestClient(app)


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------


def test_health_returns_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["vehicles_loaded"] > 0


# ---------------------------------------------------------------------------
# GET /vehicles/brands
# ---------------------------------------------------------------------------


def test_get_brands_returns_list(client):
    response = client.get("/vehicles/brands")
    assert response.status_code == 200
    brands = response.json()
    assert isinstance(brands, list)
    assert "TOYOTA" in brands


def test_get_brands_sorted(client):
    response = client.get("/vehicles/brands")
    brands = response.json()
    assert brands == sorted(brands)


# ---------------------------------------------------------------------------
# GET /vehicles/stats
# ---------------------------------------------------------------------------


def test_get_stats_structure(client):
    response = client.get("/vehicles/stats")
    assert response.status_code == 200
    data = response.json()
    assert "number_of_vehicles" in data
    assert "average_price" in data
    assert "average_co2" in data


def test_get_stats_vehicle_count(client, sample_df):
    response = client.get("/vehicles/stats")
    data = response.json()
    assert data["number_of_vehicles"] == len(sample_df)


# ---------------------------------------------------------------------------
# GET /vehicles — filtres
# ---------------------------------------------------------------------------


def test_list_vehicles_no_filter(client, sample_df):
    response = client.get("/vehicles")
    assert response.status_code == 200
    assert len(response.json()) == len(sample_df)


def test_list_vehicles_filter_by_brand(client):
    response = client.get("/vehicles?brand=TOYOTA")
    assert response.status_code == 200
    data = response.json()
    assert all(v["brand"] == "TOYOTA" for v in data)


def test_list_vehicles_filter_by_budget(client):
    response = client.get("/vehicles?budget=20000")
    assert response.status_code == 200
    data = response.json()
    assert all(v["vehicle_price_eur"] <= 20000 for v in data)


def test_list_vehicles_filter_by_energy(client):
    response = client.get("/vehicles?energy=electric")
    assert response.status_code == 200
    data = response.json()
    assert all("elec" in v["energy"] for v in data)


def test_list_vehicles_unknown_brand_returns_empty(client):
    response = client.get("/vehicles?brand=BRAND_XYZ_INEXISTANTE")
    assert response.status_code == 200
    assert response.json() == []


# ---------------------------------------------------------------------------
# GET /vehicles/recommend
# ---------------------------------------------------------------------------


def test_recommend_returns_list(client):
    response = client.get("/vehicles/recommend?budget=50000")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_recommend_has_score_field(client):
    response = client.get("/vehicles/recommend?budget=50000")
    data = response.json()
    assert len(data) > 0
    assert "score" in data[0]


def test_recommend_score_in_range(client):
    response = client.get("/vehicles/recommend?budget=50000")
    for v in response.json():
        assert 0.0 <= v["score"] <= 1.0


def test_recommend_empty_when_impossible_budget(client):
    response = client.get("/vehicles/recommend?budget=1")
    assert response.status_code == 200
    assert response.json() == []


# ---------------------------------------------------------------------------
# GET /vehicles/compare
# ---------------------------------------------------------------------------


def test_compare_brands_structure(client):
    response = client.get("/vehicles/compare?brand1=TOYOTA&brand2=RENAULT")
    assert response.status_code == 200
    data = response.json()
    assert "TOYOTA" in data
    assert "RENAULT" in data


def test_compare_brands_has_avg_price(client):
    response = client.get("/vehicles/compare?brand1=TOYOTA&brand2=TESLA")
    data = response.json()
    assert "avg_price_eur" in data["TOYOTA"]


def test_compare_unknown_brand_returns_404(client):
    response = client.get("/vehicles/compare?brand1=TOYOTA&brand2=BRAND_XYZ")
    assert response.status_code == 404
