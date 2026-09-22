"""Unitarios de services.movie_service (sin red, sin archivos fuera de tmp_path)."""

import json

import pytest

from exceptions import StorageError
from services import movie_service as ms


def test_agregar_a_favoritas_ok(pelicula_omdb):
    assert ms.agregar_a_favoritas(pelicula_omdb) is True
    assert ms.PELICULAS_FAVORITAS == [pelicula_omdb]


def test_agregar_duplicado_rechazado(pelicula_omdb):
    assert ms.agregar_a_favoritas(pelicula_omdb) is True
    assert ms.agregar_a_favoritas(dict(pelicula_omdb)) is False
    assert len(ms.PELICULAS_FAVORITAS) == 1


def test_eliminar_existente(pelicula_omdb):
    ms.agregar_a_favoritas(pelicula_omdb)
    assert ms.eliminar_de_favoritas("Test Movie") is True
    assert ms.PELICULAS_FAVORITAS == []


def test_eliminar_inexistente():
    assert ms.eliminar_de_favoritas("No Existe") is False


def test_historial_anota_titulo_y_fecha(pelicula_omdb):
    ms.agregar_al_historial(pelicula_omdb)
    assert ms.HISTORIAL_BUSQUEDAS == [{"titulo": "Test Movie", "fecha": "hoy"}]


def test_estadisticas_cuentan(pelicula_omdb):
    ms.agregar_a_favoritas(pelicula_omdb)
    ms.agregar_al_historial(pelicula_omdb)
    assert ms.obtener_estadisticas() == {"total_favoritas": 1, "total_historial": 1}


def test_limpiar_historial(pelicula_omdb):
    ms.agregar_al_historial(pelicula_omdb)
    ms.limpiar_historial()
    assert ms.HISTORIAL_BUSQUEDAS == []


def test_export_import_roundtrip(pelicula_omdb, tmp_path):
    ms.agregar_a_favoritas(pelicula_omdb)
    ms.agregar_al_historial(pelicula_omdb)
    archivo = str(tmp_path / "datos.json")
    ms.exportar_a_json(archivo)
    guardado = json.loads((tmp_path / "datos.json").read_text())
    assert set(guardado) == {"favoritas", "historial", "estadisticas"}
    ms.limpiar_historial()
    ms.PELICULAS_FAVORITAS.clear()
    ms.importar_de_json(archivo)
    assert ms.PELICULAS_FAVORITAS == [pelicula_omdb]
    assert ms.HISTORIAL_BUSQUEDAS == [{"titulo": "Test Movie", "fecha": "hoy"}]


def test_importar_archivo_faltante():
    with pytest.raises(StorageError):
        ms.importar_de_json("/ruta/que/no/existe.json")


def test_importar_json_corrupto(tmp_path):
    archivo = tmp_path / "mal.json"
    archivo.write_text("{json roto")
    with pytest.raises(StorageError):
        ms.importar_de_json(str(archivo))


def test_importar_forma_invalida(tmp_path):
    archivo = tmp_path / "lista.json"
    archivo.write_text("[1, 2, 3]")
    with pytest.raises(StorageError):
        ms.importar_de_json(str(archivo))


def test_exportar_ruta_invalida():
    with pytest.raises(StorageError):
        ms.exportar_a_json("/ruta/que/no/existe.json")


def test_populares_y_genero():
    assert len(ms.obtener_peliculas_populares()) == 5
    assert len(ms.buscar_peliculas_por_genero("accion")) == 2
    assert len(ms.buscar_peliculas_por_genero("COMEDIA")) == 2
    assert len(ms.buscar_peliculas_por_genero("otro")) == 4
