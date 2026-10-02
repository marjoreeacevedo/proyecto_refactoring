"""Unitarios de ui.menu: validación de género con input simulado."""

from unittest.mock import MagicMock, patch

import ui.menu as menu


def test_genero_invalido_muestra_error(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "terror")
    with patch("ui.menu.buscar_peliculas_por_genero") as servicio:
        menu.funcion_buscar_por_genero()
    assert "género no válido" in capsys.readouterr().out
    servicio.assert_not_called()


def test_genero_valido_llama_servicio(monkeypatch):
    respuestas = iter(["accion", ""])
    monkeypatch.setattr("builtins.input", lambda _: next(respuestas))
    with (
        patch("ui.menu.buscar_peliculas_por_genero", return_value=[]) as servicio,
        patch("ui.menu.mostrar_lista_peliculas") as mostrar,
    ):
        menu.funcion_buscar_por_genero()
    servicio.assert_called_once_with("accion")
    mostrar.assert_called_once_with([])
