"""Unitarios de validators (entradas hostiles)."""

import pytest

from validators import nombre_archivo_seguro, texto_busqueda, timeout_valido


def test_texto_ok_recorta_espacios():
    assert texto_busqueda("  Dune  ", "El título") == "Dune"


@pytest.mark.parametrize("malo", ["", "   ", "x" * 201])
def test_texto_rechaza(malo):
    with pytest.raises(ValueError):
        texto_busqueda(malo, "El título")


def test_archivo_ok():
    assert nombre_archivo_seguro("datos") == "datos"


@pytest.mark.parametrize("malo", ["", "   ", "../secretos", "/abs/path", "a/b", ".."])
def test_archivo_rechaza(malo):
    with pytest.raises(ValueError):
        nombre_archivo_seguro(malo)


def test_timeout_ok():
    assert timeout_valido("10") == 10


@pytest.mark.parametrize("malo", ["abc", "", "0", "-5", "3.5"])
def test_timeout_rechaza(malo):
    with pytest.raises(ValueError):
        timeout_valido(malo)
