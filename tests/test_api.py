"""Integración mockeada: requests.get parcheado, ninguna llamada real."""

from unittest.mock import MagicMock, patch

import pytest
import requests as rq

from api import omdb, tvmaze
from api.client import hacer_request
from exceptions import ApiError, MovieNotFoundError


def _respuesta(payload=None, mala_json=False):
    r = MagicMock()
    r.status_code = 200
    r.raise_for_status.return_value = None
    if mala_json:
        r.json.side_effect = ValueError("no es json")
    else:
        r.json.return_value = payload
    return r


def test_request_ok():
    with patch("api.client.requests.get", return_value=_respuesta({"ok": True})):
        assert hacer_request("http://x") == {"ok": True}


def test_request_fallo_red():
    with patch("api.client.requests.get", side_effect=rq.ConnectionError("caído")):
        with pytest.raises(ApiError):
            hacer_request("http://x")


def test_request_json_invalido():
    with patch("api.client.requests.get", return_value=_respuesta(mala_json=True)):
        with pytest.raises(ApiError):
            hacer_request("http://x")


def test_buscar_pelicula_ok_y_cache():
    payload = {"Response": "True", "Title": "T"}
    with patch("api.client.requests.get", return_value=_respuesta(payload)) as get:
        assert omdb.buscar_pelicula("Unica") == payload
        assert "Unica" in omdb.CACHE_PELICULAS
        omdb.buscar_pelicula("Unica")  # segunda: desde caché
        assert get.call_count == 1


def test_buscar_pelicula_inexistente():
    with patch("api.client.requests.get", return_value=_respuesta({"Response": "False"})):
        with pytest.raises(MovieNotFoundError):
            omdb.buscar_pelicula("No Existe XYZ")


def test_buscar_series_cachea_con_prefijo():
    payload = [{"show": {"name": "S"}}]
    with patch("api.client.requests.get", return_value=_respuesta(payload)):
        assert tvmaze.buscar_series("algo") == payload
        assert "series_algo" in tvmaze.CACHE_SERIES
