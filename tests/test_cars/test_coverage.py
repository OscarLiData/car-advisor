"""
Tests complémentaires pour atteindre 100% de couverture.

Couvre :
- api/main.py     lignes 45-56 (lifespan : chargement OK + FileNotFoundError)
- api/routers/vehicles.py  ligne 83  (filtre body dans list_vehicles)
                           ligne 158 (HTTPException brand1 introuvable)
- data/loader.py  lignes 26-27 (branche save=True)
"""

from pathlib import Path
from unittest.mock import patch

import pandas as pd
import pytest
from fastapi.testclient import TestClient

from car.api.main import app
from car.data.loader import load_dataset


# ---------------------------------------------------------------------------
# Fixture locale — nom différent pour éviter le conflit avec test_api.py
# ---------------------------------------------------------------------------


@pytest.fixture
def api_client(sample_df) -> TestClient:
    app.state.df = sample_df
    return TestClient(app)


# ---------------------------------------------------------------------------
# api/main.py — lifespan (lignes 45-56)
# ---------------------------------------------------------------------------


def test_lifespan_loads_dataset_successfully(sample_df):
    """Lignes 45-52 : le lifespan charge le dataset et le stocke dans app.state."""
    with patch("car.api.main.load_dataset", return_value=sample_df):
        with TestClient(app) as client:
            response = client.get("/health")
            assert response.status_code == 200
            assert response.json()["vehicles_loaded"] == len(sample_df)


def test_lifespan_raises_on_missing_file():
    """Lignes 53-56 : FileNotFoundError propagée si le CSV est absent."""
    with patch("car.api.main.load_dataset", side_effect=FileNotFoundError("not found")):
        with pytest.raises(FileNotFoundError):
            with TestClient(app):
                pass


# ---------------------------------------------------------------------------
# api/routers/vehicles.py — ligne 83 (filtre body dans list_vehicles)
# ---------------------------------------------------------------------------


def test_list_vehicles_filter_by_body(api_client):
    """Ligne 83 : le filtre body est appliqué dans list_vehicles."""
    response = api_client.get("/vehicles?body=berline")
    assert response.status_code == 200
    data = response.json()
    assert all(v["body_type"] == "berline" for v in data)


def test_list_vehicles_filter_body_no_match(api_client):
    """Ligne 83 + retour [] : body inconnu → liste vide."""
    response = api_client.get("/vehicles?body=cabriolet_xyz")
    assert response.status_code == 200
    assert response.json() == []


# ---------------------------------------------------------------------------
# api/routers/vehicles.py — ligne 158 (HTTPException brand1 introuvable)
# ---------------------------------------------------------------------------


def test_compare_unknown_brand1_returns_404(api_client):
    """Ligne 158 : brand1 introuvable → 404."""
    response = api_client.get("/vehicles/compare?brand1=BRAND_XYZ&brand2=TOYOTA")
    assert response.status_code == 404
    assert "BRAND_XYZ" in response.json()["detail"]


# ---------------------------------------------------------------------------
# data/loader.py — lignes 26-27 (branche save=True)
# ---------------------------------------------------------------------------


def test_load_dataset_save_true(tmp_path):
    """Lignes 26-27 : save=True écrit le fichier nettoyé sur disque."""
    raw_csv = tmp_path / "raw.csv"
    raw_csv.write_text(
        "Marque,Modele,Carrosserie,Energie,Prix vehicule,"
        "CO2 vitesse mixte max,Conso vitesse mixte max,"
        "Autonomie elec max,Puissance maximale,Poids a vide,Bonus-malus\n"
        "TOYOTA,Yaris,berline,Essence,15000,110,5.5,,72,1050,Neutre 0\n"
    )
    processed_path = tmp_path / "processed" / "cars_clean.csv"

    df = load_dataset(raw_path=raw_csv, save=True, processed_path=processed_path)

    assert processed_path.exists()
    loaded = pd.read_csv(processed_path)
    assert len(loaded) == len(df)


def test_load_dataset_save_false_does_not_write(tmp_path):
    """save=False (défaut) : aucun fichier créé."""
    raw_csv = tmp_path / "raw.csv"
    raw_csv.write_text(
        "Marque,Modele,Carrosserie,Energie,Prix vehicule,"
        "CO2 vitesse mixte max,Conso vitesse mixte max,"
        "Autonomie elec max,Puissance maximale,Poids a vide,Bonus-malus\n"
        "RENAULT,Clio,berline,Gazole,18000,95,4.2,,66,1180,Neutre 0\n"
    )
    processed_path = tmp_path / "should_not_exist.csv"

    load_dataset(raw_path=raw_csv, save=False, processed_path=processed_path)

    assert not processed_path.exists()
