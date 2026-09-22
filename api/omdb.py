"""Lógica de la API OMDB (películas) + caché de películas."""

from typing import Optional

from api.client import hacer_request
from config import CONFIG
from constants import API_KEY_OMDB, BASE_URL_OMDB

CACHE_PELICULAS = {}


def buscar_pelicula(titulo: str) -> Optional[dict]:
    """Busca película sin validación"""
    global CACHE_PELICULAS

    if titulo in CACHE_PELICULAS:
        if CONFIG["debug"]:
            print(f"DEBUG: Usando cache para {titulo}")
        return CACHE_PELICULAS[titulo]

    url = f"{BASE_URL_OMDB}?t={titulo}&apikey={API_KEY_OMDB}"
    data = hacer_request(url)

    if data.get("Response") == "True":
        CACHE_PELICULAS[titulo] = data
        return data
    else:
        return None


def buscar_peliculas_por_actor(actor: str) -> list:
    """Busca películas por actor sin paginación"""
    url = f"{BASE_URL_OMDB}?s={actor}&type=movie&apikey={API_KEY_OMDB}"
    data = hacer_request(url)

    if data.get("Response") == "True":
        return data.get("Search", [])
    return []
