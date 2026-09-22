import requests
import json
from typing import Optional

from config import CONFIG
from constants import API_KEY_OMDB, BASE_URL_OMDB, BASE_URL_TVMAZE, CACHE_PREFIX_SERIES

# Variables globales
USUARIO_LOGUEADO = None
PELICULAS_FAVORITAS = []
HISTORIAL_BUSQUEDAS = []
CACHE_PELICULAS = {}
CACHE_SERIES = {}

def hacer_request(url: str, params: Optional[dict] = None) -> dict:
    """Hace request sin manejo de errores"""
    if CONFIG["debug"]:
        print(f"DEBUG: Haciendo request a {url}")

    response = requests.get(url, params=params, timeout=CONFIG["timeout"])

    if CONFIG["verbose"]:
        print(f"DEBUG: Status code: {response.status_code}")

    return response.json()

def buscar_pelicula(titulo: str) -> Optional[dict]:
    """Busca película sin validación"""
    global CACHE_PELICULAS

    if titulo in CACHE_PELICULAS:
        if CONFIG["debug"]:
            print(f"DEBUG: Usando cache para {titulo}")
        return CACHE_PELICULAS[titulo]

    url = f"{BASE_URL_OMDB}?t={titulo}&apikey={API_KEY_OMDB}"
    data = hacer_request(url)
    
    if data.get("Response") == "True":
        CACHE_PELICULAS[titulo] = data
        return data
    else:
        return None

def buscar_peliculas_por_actor(actor: str) -> list:
    """Busca películas por actor sin paginación"""
    url = f"{BASE_URL_OMDB}?s={actor}&type=movie&apikey={API_KEY_OMDB}"
    data = hacer_request(url)
    
    if data.get("Response") == "True":
        return data.get("Search", [])
    return []

def buscar_series(nombre: str) -> list:
    """Busca series en TVMaze"""
    global CACHE_SERIES

    cache_key = f"{CACHE_PREFIX_SERIES}{nombre}"
    if cache_key in CACHE_SERIES:
        return CACHE_SERIES[cache_key]

    url = f"{BASE_URL_TVMAZE}/search/shows?q={nombre}"
    data = hacer_request(url)
    
    CACHE_SERIES[cache_key] = data
    return data

def obtener_detalles_serie(id_serie: int) -> dict:
    """Obtiene detalles de serie"""
    url = f"{BASE_URL_TVMAZE}/shows/{id_serie}"
    return hacer_request(url)

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
        if p.get("Title") == pelicula.get("Title"):
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
        if PELICULAS_FAVORITAS[i].get("Title") == titulo:
            PELICULAS_FAVORITAS.pop(i)
            return True
    return False

def agregar_al_historial(pelicula: dict) -> None:
    """Agrega al historial sin límite"""
    global HISTORIAL_BUSQUEDAS
    HISTORIAL_BUSQUEDAS.append({
        "titulo": pelicula.get("Title", ""),
        "fecha": "hoy"  # Hardcoded
    })

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
