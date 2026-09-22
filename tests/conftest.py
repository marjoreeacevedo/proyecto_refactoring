"""Fixtures compartidas: datos falsos + aislamiento del estado global."""

import pytest

import config
from api import omdb, tvmaze
from services import movie_service as ms


@pytest.fixture
def pelicula_omdb():
    """Dict falso con formato OMDB."""
    return {
        "Title": "Test Movie",
        "Year": "2000",
        "imdbRating": "7.5",
        "Genre": "Drama",
        "Director": "Alguien",
        "Actors": "A, B",
        "Plot": "Trama de prueba",
        "Country": "Nunca Jamás",
        "Awards": "Ninguno",
    }


@pytest.fixture(autouse=True)
def aislar_estado():
    """Restaura globales (favoritas, historial, cachés, timeout) tras cada test."""
    fav = list(ms.PELICULAS_FAVORITAS)
    hist = list(ms.HISTORIAL_BUSQUEDAS)
    cache_pelis = dict(omdb.CACHE_PELICULAS)
    cache_series = dict(tvmaze.CACHE_SERIES)
    timeout = config.CONFIG["timeout"]
    yield
    ms.PELICULAS_FAVORITAS[:] = fav
    ms.HISTORIAL_BUSQUEDAS[:] = hist
    omdb.CACHE_PELICULAS.clear()
    omdb.CACHE_PELICULAS.update(cache_pelis)
    tvmaze.CACHE_SERIES.clear()
    tvmaze.CACHE_SERIES.update(cache_series)
    config.CONFIG["timeout"] = timeout
