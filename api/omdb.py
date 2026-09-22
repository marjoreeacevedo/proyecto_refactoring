"""Lógica de la API OMDB (películas) + caché de películas."""

import logging

from api.client import hacer_request
from exceptions.movie_not_found import MovieNotFoundError
from constants import API_KEY_OMDB, BASE_URL_OMDB

logger = logging.getLogger(__name__)

CACHE_PELICULAS = {}


def buscar_pelicula(titulo: str) -> dict:
    """Busca película; lanza MovieNotFoundError si OMDB no la tiene."""
    global CACHE_PELICULAS

    if titulo in CACHE_PELICULAS:
        logger.debug("Usando cache para %s", titulo)
        return CACHE_PELICULAS[titulo]

    url = f"{BASE_URL_OMDB}?t={titulo}&apikey={API_KEY_OMDB}"
    data = hacer_request(url)

    if data.get("Response") == "True":
        CACHE_PELICULAS[titulo] = data
        return data
    raise MovieNotFoundError(f"No se encontró la película: {titulo}")


def buscar_peliculas_por_actor(actor: str) -> list:
    """Busca películas por actor sin paginación"""
    url = f"{BASE_URL_OMDB}?s={actor}&type=movie&apikey={API_KEY_OMDB}"
    data = hacer_request(url)

    if data.get("Response") == "True":
        return data.get("Search", [])
    return []
