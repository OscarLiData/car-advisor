"""
Couche base de données — SQLAlchemy (mode optionnel).

Activée uniquement si DATABASE_URL est défini dans les settings.
Si DATABASE_URL est vide, l'application fonctionne en mode CSV (défaut).

Usage :
    from car.database import get_session, VehicleDB
"""

import logging

from sqlalchemy import Column, Float, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from car.config import settings

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    pass


class VehicleDB(Base):
    """Modèle ORM — table `vehicles` en PostgreSQL."""

    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    brand = Column(String(100), nullable=False, index=True)
    model = Column(String(200), nullable=False)
    body_type = Column(String(100))
    energy = Column(String(50), index=True)
    vehicle_price_eur = Column(Float)
    co2_mixed_g_km = Column(Float)
    fuel_consumption_l_100km = Column(Float)
    electric_range_km = Column(Float)
    max_power_kw = Column(Float)
    vehicle_weight_kg = Column(Float)
    eco_bonus_malus_eur = Column(Float)
    power_weight_ratio = Column(Float)


def create_db_engine():
    """Crée l'engine SQLAlchemy depuis DATABASE_URL."""
    if not settings.database_url:
        raise RuntimeError(
            "DATABASE_URL non configuré. "
            "Définissez-le dans .env pour activer le mode PostgreSQL."
        )
    engine = create_engine(settings.database_url, echo=False)
    logger.info("Connexion PostgreSQL établie : %s", settings.database_url)
    return engine


def init_db(engine) -> None:
    """Crée les tables si elles n'existent pas."""
    Base.metadata.create_all(engine)
    logger.info("Tables initialisées")


def get_session_factory(engine) -> sessionmaker:
    return sessionmaker(bind=engine, autoflush=False, autocommit=False)
