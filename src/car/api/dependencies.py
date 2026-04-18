"""
Dépendances FastAPI.

Le DataFrame est chargé une seule fois au démarrage de l'application
(lifespan) et injecté dans chaque endpoint via Depends.
"""

import logging
from typing import Annotated

import pandas as pd
from fastapi import Depends, Request

logger = logging.getLogger(__name__)


def get_df(request: Request) -> pd.DataFrame:
    """
    Injecte le DataFrame global depuis l'état de l'application.
    Chargé une seule fois dans le lifespan de main.py.
    """
    return request.app.state.df


# Alias typé pour alléger les signatures des endpoints
DataFrameDep = Annotated[pd.DataFrame, Depends(get_df)]
