"""
Script d'ingestion : charge le CSV ADEME nettoyé en base PostgreSQL.

Usage :
    python -m car.ingest
    make ingest

Ce script est pensé pour être lancé une fois au démarrage du conteneur
(via docker-compose depends_on + healthcheck), ou manuellement après
une mise à jour du dataset ADEME.

Il est idempotent : si la table est déjà peuplée avec le même nombre de
lignes, l'ingestion est sautée (comportement contrôlable via --force).
"""

import argparse
import logging
import sys

from sqlalchemy.orm import Session

from car.config import settings
from car.data.loader import load_dataset
from car.database import VehicleDB, create_db_engine, get_session_factory, init_db

logger = logging.getLogger(__name__)


def ingest(force: bool = False) -> int:
    """
    Charge le DataFrame nettoyé en base PostgreSQL.

    Args:
        force: si True, vide la table avant de réinsérer.

    Returns:
        Nombre de lignes insérées.
    """
    engine = create_db_engine()
    init_db(engine)
    SessionLocal = get_session_factory(engine)

    df = load_dataset(save=False)
    logger.info("Dataset chargé : %d lignes à ingérer", len(df))

    with SessionLocal() as session:
        existing_count = session.query(VehicleDB).count()

        if existing_count == len(df) and not force:
            logger.info(
                "Table déjà peuplée (%d lignes). "
                "Utilisez --force pour réingérer.",
                existing_count,
            )
            return 0

        if force and existing_count > 0:
            session.query(VehicleDB).delete()
            session.commit()
            logger.info("Table vidée (--force)")

        records = df.fillna(0).to_dict(orient="records")
        session.bulk_insert_mappings(VehicleDB, records)
        session.commit()

    logger.info("Ingestion terminée : %d véhicules insérés", len(df))
    return len(df)


def main() -> None:
    logging.basicConfig(
        level="INFO",
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        stream=sys.stdout,
    )

    parser = argparse.ArgumentParser(description="Ingestion du dataset ADEME → PostgreSQL")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Vide la table avant de réinsérer (idempotent garanti)",
    )
    args = parser.parse_args()

    inserted = ingest(force=args.force)
    sys.exit(0 if inserted >= 0 else 1)


if __name__ == "__main__":
    main()
