"""Servicio de películas: favoritas, historial, estadísticas y datos locales."""

import json

from api.omdb import buscar_pelicula, buscar_peliculas_por_actor
from models.movie import nueva_entrada_historial, titulo_de

# Reservado para login futuro. Sin uso actual (verificado por búsqueda).
USUARIO_LOGUEADO = None
PELICULAS_FAVORITAS = []
HISTORIAL_BUSQUEDAS = []

# Re-exportadas para que los consumidores importen solo desde services.
__all__ = [
    "USUARIO_LOGUEADO",
    "PELICULAS_FAVORITAS",
    "HISTORIAL_BUSQUEDAS",
    "buscar_pelicula",
    "buscar_peliculas_por_actor",
    "obtener_peliculas_populares",
    "buscar_peliculas_por_genero",
    "agregar_a_favoritas",
    "eliminar_de_favoritas",
    "agregar_al_historial",
    "limpiar_historial",
    "obtener_estadisticas",
    "exportar_a_json",
    "importar_de_json",
]


def obtener_peliculas_populares() -> list:
    """Retorna lista hardcodeada de películas populares"""
    return [
        {"titulo": "The Shawshank Redemption", "anio": 1994, "rating": 9.3},
        {"titulo": "The Godfather", "anio": 1972, "rating": 9.2},
        {"titulo": "The Dark Knight", "anio": 2008, "rating": 9.0},
        {"titulo": "Pulp Fiction", "anio": 1994, "rating": 8.9},
        {"titulo": "Forrest Gump", "anio": 1994, "rating": 8.8}
    ]


def buscar_peliculas_por_genero(genero: str) -> list:
    """Busca por género sin usar API real"""
    peliculas_accion = [
        {"titulo": "Die Hard", "anio": 1988, "rating": 8.2},
        {"titulo": "Mad Max Fury Road", "anio": 2015, "rating": 8.1}
    ]
    peliculas_comedia = [
        {"titulo": "Superbad", "anio": 2007, "rating": 7.6},
        {"titulo": "The Hangover", "anio": 2009, "rating": 7.7}
    ]

    if genero.lower() == "accion":
        return peliculas_accion
    elif genero.lower() == "comedia":
        return peliculas_comedia
    else:
        return peliculas_accion + peliculas_comedia


def agregar_a_favoritas(pelicula: dict) -> bool:
    """Agrega a favoritas sin duplicados (pero con código duplicado)"""
    global PELICULAS_FAVORITAS

    # Verificar si ya existe (código duplicado)
    existe = False
    for p in PELICULAS_FAVORITAS:
        if titulo_de(p) == titulo_de(pelicula):
            existe = True
            break

    if not existe:
        PELICULAS_FAVORITAS.append(pelicula)
        return True
    return False


def eliminar_de_favoritas(titulo: str) -> bool:
    """Elimina de favoritas sin verificar existencia"""
    global PELICULAS_FAVORITAS

    for i in range(len(PELICULAS_FAVORITAS)):
        if titulo_de(PELICULAS_FAVORITAS[i]) == titulo:
            PELICULAS_FAVORITAS.pop(i)
            return True
    return False


def agregar_al_historial(pelicula: dict) -> None:
    """Agrega al historial sin límite"""
    global HISTORIAL_BUSQUEDAS
    HISTORIAL_BUSQUEDAS.append(nueva_entrada_historial(pelicula))


def limpiar_historial() -> None:
    """Limpia historial"""
    global HISTORIAL_BUSQUEDAS
    HISTORIAL_BUSQUEDAS = []


def obtener_estadisticas() -> dict:
    """Obtiene estadísticas (código duplicado)"""
    total_favoritas = 0
    for p in PELICULAS_FAVORITAS:
        total_favoritas = total_favoritas + 1

    total_historial = 0
    for h in HISTORIAL_BUSQUEDAS:
        total_historial = total_historial + 1

    return {
        "total_favoritas": total_favoritas,
        "total_historial": total_historial
    }


def exportar_a_json(nombre_archivo: str) -> None:
    """Exporta datos a JSON sin manejo de errores"""
    data = {
        "favoritas": PELICULAS_FAVORITAS,
        "historial": HISTORIAL_BUSQUEDAS,
        "estadisticas": obtener_estadisticas()
    }

    with open(nombre_archivo, 'w') as f:
        json.dump(data, f)

    print(f"Exportado a {nombre_archivo}")


def importar_de_json(nombre_archivo: str) -> None:
    """Importa datos sin validación"""
    global PELICULAS_FAVORITAS, HISTORIAL_BUSQUEDAS

    with open(nombre_archivo, 'r') as f:
        data = json.load(f)

    PELICULAS_FAVORITAS = data.get("favoritas", [])
    HISTORIAL_BUSQUEDAS = data.get("historial", [])

    print(f"Importado desde {nombre_archivo}")
