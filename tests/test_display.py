"""Unitarios de ui.display (salida por pantalla con capsys)."""

from ui.display import mostrar_lista_peliculas, mostrar_pelicula, mostrar_serie


def test_pelicula_parcial_muestra_na(capsys, pelicula_omdb):
    del pelicula_omdb["Year"]
    mostrar_pelicula(pelicula_omdb)
    out = capsys.readouterr().out
    assert "Título: Test Movie" in out
    assert "Año: N/A" in out


def test_pelicula_none(capsys):
    mostrar_pelicula(None)
    assert "No se encontró" in capsys.readouterr().out


def test_serie_minima(capsys):
    mostrar_serie({"name": "S", "summary": "hola"})
    out = capsys.readouterr().out
    assert "Nombre: S" in out
    assert "Resumen: hola..." in out
    assert "Idioma: N/A" in out


def test_lista_ambos_formatos(capsys):
    mostrar_lista_peliculas([
        {"titulo": "T", "anio": 2000, "rating": 7.5},
        {"Title": "U", "Year": "2001"},
        {"raro": 1},
    ])
    out = capsys.readouterr().out
    assert "1. T (2000) - 7.5" in out
    assert "2. U (2001)" in out
    assert "3. Película desconocida" in out
