"""
Point d'entrée de l'API FastAPI.

Lifespan : le dataset ADEME est chargé une seule fois au démarrage
et stocké dans app.state.df — injecté ensuite via Depends dans chaque endpoint.
"""

import logging
import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from car.api.routers.vehicles import router as vehicles_router
from car.api.schemas import HealthOut
from car.config import settings
from car.data.loader import load_dataset

# ---------------------------------------------------------------------------
# Logging structuré
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=settings.log_level.upper(),
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Lifespan — chargement du dataset au démarrage
# ---------------------------------------------------------------------------


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Chargement unique du dataset au démarrage de l'application.
    Stocké dans app.state.df pour être injecté dans les endpoints.
    """
    logger.info("Démarrage : chargement du dataset ADEME...")
    try:
        df = load_dataset(save=False)
        app.state.df = df
        logger.info("Dataset chargé : %d véhicules", len(df))
    except FileNotFoundError as e:
        logger.error("Impossible de charger le dataset : %s", e)
        raise

    yield  # l'application tourne ici

    logger.info("Arrêt de l'application")


# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------

app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description=(
        "API d'analyse des véhicules selon les données ADEME. "
        "Expose un moteur de recommandation multi-critères (TOPSIS) "
        "et des endpoints de filtrage et comparaison."
    ),
    lifespan=lifespan,
)

# CORS — permissif en dev, à restreindre en prod
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------

app.include_router(vehicles_router)


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------


@app.get("/health", response_model=HealthOut, tags=["monitoring"])
def health() -> HealthOut:
    """
    Vérifie que l'API est opérationnelle et indique combien de véhicules
    sont chargés en mémoire.
    """
    df = app.state.df
    return HealthOut(
        status="ok",
        version=settings.api_version,
        vehicles_loaded=len(df),
    )


# ---------------------------------------------------------------------------
# Entrypoint CLI : python -m car.api.main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    uvicorn.run(
        "car.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
        log_level=settings.log_level.lower(),
    )
