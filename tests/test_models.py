"""Unitarios de models (helpers puros, sin estado)."""

import models.movie as mm
import models.series as sm


def test_titulo_de_ambos_formatos():
    assert mm.titulo_de({"Title": "A"}) == "A"
    assert mm.titulo_de({"titulo": "B"}) == "B"
    assert mm.titulo_de({}) == ""


def test_formatos():
    assert mm.es_formato_omdb({"Title": "A"}) is True
    assert mm.es_formato_omdb({"titulo": "B"}) is False
    assert mm.es_formato_local({"titulo": "B"}) is True
    assert mm.es_formato_local({"Title": "A"}) is False


def test_nueva_entrada_historial():
    assert mm.nueva_entrada_historial({"Title": "T"}) == {"titulo": "T", "fecha": "hoy"}


def test_nombre_show():
    assert sm.nombre_show({"name": "S"}) == "S"
    assert sm.nombre_show({}) == ""


def test_resumen_corto():
    assert sm.resumen_corto({"summary": "abc"}) == "abc..."
    largo = "x" * 500
    resumen = sm.resumen_corto({"summary": largo})
    assert resumen == "x" * 200 + "..."
    assert sm.resumen_corto({}) == "N/A..."
