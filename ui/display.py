"""Visualización: todo lo que pinta en pantalla."""

import os
from typing import Optional

from models.movie import es_formato_local, es_formato_omdb
from models.series import nombre_show, resumen_corto


def clear_screen() -> None:
    """Limpia pantalla de forma no portable"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_separator() -> None:
    """Imprime separador"""
    print("=" * 60)


def print_header(text: str) -> None:
    """Imprime header"""
    print_separator()
    print(text.upper().center(60))
    print_separator()


def mostrar_pelicula(pelicula: Optional[dict]) -> None:
    """Muestra película sin validación"""
    print_separator()
    if pelicula is None:
        print("No se encontró la película")
        return

    # Acceso con get() y valor por defecto
    print(f"Título: {pelicula.get('Title', 'N/A')}")
    print(f"Año: {pelicula.get('Year', 'N/A')}")
    print(f"Rating IMDB: {pelicula.get('imdbRating', 'N/A')}")
    print(f"Género: {pelicula.get('Genre', 'N/A')}")
    print(f"Director: {pelicula.get('Director', 'N/A')}")
    print(f"Actores: {pelicula.get('Actors', 'N/A')}")
    print(f"Trama: {pelicula.get('Plot', 'N/A')}")
    print(f"País: {pelicula.get('Country', 'N/A')}")
    print(f"Premios: {pelicula.get('Awards', 'N/A')}")

    print_separator()


def mostrar_serie(serie: dict) -> None:
    """Muestra serie"""
    print_separator()
    show = serie.get("show", serie)

    print(f"Nombre: {nombre_show(show) or 'N/A'}")
    print(f"Idioma: {show.get('language', 'N/A')}")
    print(f"Géneros: {show.get('genres', [])}")
    print(f"Rating: {show.get('rating', {}).get('average', 'N/A')}")
    print(f"Estado: {show.get('status', 'N/A')}")
    print(f"Estreno: {show.get('premiered', 'N/A')}")
    print(f"Final: {show.get('ended', 'N/A')}")
    print(f"Episodios: {show.get('runtime', 'N/A')}")
    print(f"Resumen: {resumen_corto(show)}")
    print_separator()


def mostrar_lista_peliculas(peliculas: list) -> None:
    """Muestra lista de películas"""
    i = 0
    while i < len(peliculas):
        if es_formato_local(peliculas[i]):
            print(f"{i + 1}. {peliculas[i]['titulo']} ({peliculas[i]['anio']}) - {peliculas[i]['rating']}")
        elif es_formato_omdb(peliculas[i]):
            print(f"{i + 1}. {peliculas[i]['Title']} ({peliculas[i].get('Year', 'N/A')})")
        else:
            print(f"{i + 1}. Película desconocida")
        i += 1
