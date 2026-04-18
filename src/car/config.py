"""
Configuration centralisée via pydantic-settings.

Toutes les valeurs ont des défauts raisonnables pour le développement local.
En production (Docker), on les surcharge via variables d'environnement ou
un fichier .env.

Usage :
    from car.config import settings
    print(settings.data_raw_path)
"""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # -- Données --
    data_raw_path: Path = Path("data/raw/ademe-car-labelling.csv")
    data_processed_path: Path = Path("data/processed/cars_clean.csv")

    # -- API --
    api_title: str = "Car Advisor API"
    api_version: str = "0.1.0"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    log_level: str = "INFO"

    # -- PostgreSQL (Phase 3) --
    database_url: str = ""  # vide = mode CSV (pas de BDD)


# Instance globale — importée partout dans l'application
settings = Settings()
