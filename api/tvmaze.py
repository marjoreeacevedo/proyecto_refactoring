"""Lógica de la API TVMaze (series) + caché de series."""

from api.client import hacer_request
from constants import BASE_URL_TVMAZE, CACHE_PREFIX_SERIES

CACHE_SERIES = {}


def buscar_series(nombre: str) -> list:
    """Busca series en TVMaze"""
    global CACHE_SERIES

    cache_key = f"{CACHE_PREFIX_SERIES}{nombre}"
    if cache_key in CACHE_SERIES:
        return CACHE_SERIES[cache_key]

    url = f"{BASE_URL_TVMAZE}/search/shows?q={nombre}"
    data = hacer_request(url)

    CACHE_SERIES[cache_key] = data
    return data


def obtener_detalles_serie(id_serie: int) -> dict:
    """Obtiene detalles de serie"""
    url = f"{BASE_URL_TVMAZE}/shows/{id_serie}"
    return hacer_request(url)
