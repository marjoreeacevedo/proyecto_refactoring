"""Flujos de ui.menu con input/servicios simulados (sin red ni archivos reales)."""

from unittest.mock import patch

from exceptions import ApiError, MovieNotFoundError
import ui.menu as menu


def _inputs(monkeypatch, valores):
    it = iter(valores)
    monkeypatch.setattr("builtins.input", lambda _: next(it))


def test_buscar_pelicula_ok_agrega_favorita(monkeypatch, pelicula_omdb):
    _inputs(monkeypatch, ["Matrix", "s", ""])
    with (
        patch("ui.menu.buscar_pelicula", return_value=pelicula_omdb),
        patch("ui.menu.mostrar_pelicula"),
        patch("ui.menu.agregar_al_historial") as hist,
        patch("ui.menu.agregar_a_favoritas", return_value=True) as fav,
    ):
        menu.funcion_buscar_pelicula()
    hist.assert_called_once_with(pelicula_omdb)
    fav.assert_called_once_with(pelicula_omdb)


def test_buscar_pelicula_entrada_vacia(monkeypatch, capsys):
    _inputs(monkeypatch, ["   ", ""])
    menu.funcion_buscar_pelicula()
    assert "no puede estar vac" in capsys.readouterr().out.lower()


def test_buscar_pelicula_no_encontrada(monkeypatch, capsys):
    _inputs(monkeypatch, ["Inexistente", ""])
    with (
        patch("ui.menu.buscar_pelicula", side_effect=MovieNotFoundError("x")),
        patch("ui.menu.mostrar_pelicula") as mostrar,
    ):
        menu.funcion_buscar_pelicula()
    mostrar.assert_called_once_with(None)
    assert "Error" in capsys.readouterr().out


def test_buscar_actor_con_detalle(monkeypatch):
    _inputs(monkeypatch, ["Tom", "1", ""])
    pelis = [{"Title": "T", "Year": "2000"}]
    with (
        patch("ui.menu.buscar_peliculas_por_actor", return_value=pelis),
        patch("ui.menu.buscar_pelicula", return_value={"Title": "T"}) as det,
        patch("ui.menu.mostrar_lista_peliculas"),
        patch("ui.menu.mostrar_pelicula"),
    ):
        menu.funcion_buscar_actor()
    det.assert_called_once_with("T")


def test_buscar_actor_sin_resultados(monkeypatch, capsys):
    _inputs(monkeypatch, ["Nadie", ""])
    with patch("ui.menu.buscar_peliculas_por_actor", return_value=[]):
        menu.funcion_buscar_actor()
    assert "No se encontraron" in capsys.readouterr().out


def test_buscar_series_ok(monkeypatch):
    _inputs(monkeypatch, ["Girls", "1", ""])
    series = [{"show": {"id": 1, "name": "Girls", "status": "Ended"}}]
    with (
        patch("ui.menu.buscar_series", return_value=series),
        patch("ui.menu.obtener_detalles_serie", return_value={"name": "Girls"}) as det,
        patch("ui.menu.mostrar_serie") as mostrar,
    ):
        menu.funcion_buscar_series()
    det.assert_called_once_with(1)
    mostrar.assert_called_once()


def test_buscar_series_error_red(monkeypatch, capsys):
    _inputs(monkeypatch, ["Girls", ""])
    with patch("ui.menu.buscar_series", side_effect=ApiError("caído")):
        menu.funcion_buscar_series()
    assert "No se encontraron series" in capsys.readouterr().out


def test_populares_estadisticas_y_listas(monkeypatch):
    _inputs(monkeypatch, [""])
    with (
        patch("ui.menu.obtener_peliculas_populares", return_value=[]),
        patch("ui.menu.mostrar_lista_peliculas"),
    ):
        menu.funcion_peliculas_populares()
    _inputs(monkeypatch, [""])
    with patch("ui.menu.obtener_estadisticas",
               return_value={"total_favoritas": 1, "total_historial": 2}):
        menu.funcion_estadisticas()


def test_favoritos_vacio_y_con_eliminacion(monkeypatch, capsys, pelicula_omdb):
    from services import movie_service as ms

    _inputs(monkeypatch, [""])
    ms.PELICULAS_FAVORITAS.clear()
    menu.funcion_ver_favoritos()
    assert "No tienes" in capsys.readouterr().out

    ms.PELICULAS_FAVORITAS.append(pelicula_omdb)
    _inputs(monkeypatch, ["1", ""])
    with patch("ui.menu.eliminar_de_favoritas", return_value=True) as elim:
        menu.funcion_ver_favoritos()
    elim.assert_called_once()


def test_historial_vacio_y_limpiar(monkeypatch, capsys):
    from services import movie_service as ms

    _inputs(monkeypatch, [""])
    ms.HISTORIAL_BUSQUEDAS.clear()
    menu.funcion_ver_historial()
    assert "No hay historial" in capsys.readouterr().out

    ms.HISTORIAL_BUSQUEDAS.append({"titulo": "T", "fecha": "hoy"})
    _inputs(monkeypatch, ["s", ""])
    menu.funcion_ver_historial()
    assert ms.HISTORIAL_BUSQUEDAS == []


def test_exportar_importar_ok_y_error(monkeypatch, tmp_path):
    _inputs(monkeypatch, ["datos", ""])
    with patch("ui.menu.exportar_a_json") as exp:
        menu.funcion_exportar()
    exp.assert_called_once_with("datos.json")

    _inputs(monkeypatch, ["datos", ""])
    with patch("ui.menu.importar_de_json") as imp:
        menu.funcion_importar()
    imp.assert_called_once_with("datos.json")

    _inputs(monkeypatch, ["../mal", ""])
    menu.funcion_exportar()  # path traversal -> ValueError interno, no raise


def test_configuracion_toggles(monkeypatch):
    _inputs(monkeypatch, ["1", ""])
    menu.funcion_configuracion()
    _inputs(monkeypatch, ["2", ""])
    menu.funcion_configuracion()
    _inputs(monkeypatch, ["3", "45", ""])
    menu.funcion_configuracion()
    _inputs(monkeypatch, ["3", "no-num", ""])
    menu.funcion_configuracion()
    _inputs(monkeypatch, ["0", ""])
    menu.funcion_configuracion()


def test_menu_principal_sale_y_opcion_invalida(monkeypatch, capsys):
    _inputs(monkeypatch, ["12"])
    with patch("ui.menu.clear_screen"):
        menu.menu_principal()
    assert "Hasta luego" in capsys.readouterr().out

    _inputs(monkeypatch, ["99", "12"])
    with patch("ui.menu.clear_screen"), patch("ui.menu.delay"):
        menu.menu_principal()
    assert "Opción inválida" in capsys.readouterr().out


def test_menu_principal_despacha_todo(monkeypatch):
    entradas = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
    _inputs(monkeypatch, entradas)
    objetivos = [
        "ui.menu.funcion_buscar_pelicula",
        "ui.menu.funcion_buscar_actor",
        "ui.menu.funcion_buscar_series",
        "ui.menu.funcion_peliculas_populares",
        "ui.menu.funcion_buscar_por_genero",
        "ui.menu.funcion_ver_favoritos",
        "ui.menu.funcion_ver_historial",
        "ui.menu.funcion_estadisticas",
        "ui.menu.funcion_exportar",
        "ui.menu.funcion_importar",
        "ui.menu.funcion_configuracion",
    ]
    with patch("ui.menu.clear_screen"):
        with patch.multiple("ui.menu", **{n.split(".")[-1]: __import__("unittest.mock", fromlist=["Mock"]).Mock() for n in objetivos}):
            menu.menu_principal()
