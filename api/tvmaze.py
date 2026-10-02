"""Lógica de la API TVMaze (series) + caché de series."""

import logging
from urllib.parse import quote_plus

from api.client import hacer_request
from constants import BASE_URL_TVMAZE, CACHE_PREFIX_SERIES

logger = logging.getLogger(__name__)

CACHE_SERIES: dict = {}


def buscar_series(nombre: str) -> list:
    """Busca series en TVMaze"""
    cache_key = f"{CACHE_PREFIX_SERIES}{nombre}"
    if cache_key in CACHE_SERIES:
        logger.debug("Usando cache de series para %s", nombre)
        return CACHE_SERIES[cache_key]

    url = f"{BASE_URL_TVMAZE}/search/shows?q={quote_plus(nombre)}"
    data = hacer_request(url)

    CACHE_SERIES[cache_key] = data
    return data


def obtener_detalles_serie(id_serie: int) -> dict:
    """Obtiene detalles de serie"""
    url = f"{BASE_URL_TVMAZE}/shows/{id_serie}"
    return hacer_request(url)
